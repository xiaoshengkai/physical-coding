const fs = require('fs');
const path = require('path');
const { Client } = require('ssh2');
const chokidar = require('chokidar');

const CONFIG_PATH = path.join(__dirname, '../config/config.json');
const DEMOS_PATH = path.join(__dirname, '../demos');

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在，请先运行: npm run setup');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function syncToPi(conn, localPath, remotePath) {
  return new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }

      const readStream = fs.createReadStream(localPath);
      const writeStream = sftp.createWriteStream(remotePath);

      writeStream.on('close', () => resolve());
      writeStream.on('error', reject);

      readStream.pipe(writeStream);
    });
  });
}

function watch() {
  const config = loadConfig();
  const conn = new Client();

  conn.on('ready', async () => {
    console.log('✅ 已连接到树莓派');
    console.log('👀 监听代码变更中 (Ctrl+C 停止)...\n');

    const watcher = chokidar.watch(path.join(DEMOS_PATH, '**/*'), {
      ignored: /(^|[\/\\])\../,
      persistent: true,
      ignoreInitial: true
    });

    const handleChange = async (eventType, filePath) => {
      const relativePath = path.relative(DEMOS_PATH, filePath);
      const remotePath = `${config.remoteDir}/demos/${relativePath}`;

      console.log(`📝 ${eventType}: ${relativePath}`);

      try {
        const dirPath = path.dirname(remotePath);
        await new Promise((resolve, reject) => {
          conn.exec(`mkdir -p ${dirPath}`, (err) => {
            if (err) reject(err);
            else resolve();
          });
        });

        await syncToPi(conn, filePath, remotePath);
        console.log('  ✅ 已同步到树莓派\n');
      } catch (err) {
        console.error('  ❌ 同步失败:', err.message);
      }
    };

    watcher.on('change', (filePath) => handleChange('变更', filePath));
    watcher.on('add', (filePath) => handleChange('新增', filePath));
    watcher.on('unlink', (filePath) => {
      const relativePath = path.relative(DEMOS_PATH, filePath);
      const remotePath = `${config.remoteDir}/demos/${relativePath}`;
      console.log(`🗑️ 删除: ${relativePath}`);

      conn.exec(`rm -f ${remotePath}`, (err) => {
        if (err) console.error('  ❌ 删除失败:', err.message);
        else console.log('  ✅ 已删除\n');
      });
    });
  });

  conn.on('error', (err) => {
    console.error('❌ 连接失败:', err.message);
    process.exit(1);
  });

  const connectConfig = {
    host: config.raspberryPiIp,
    port: config.sshPort,
    username: config.sshUser
  };

  if (config.sshKeyPath && fs.existsSync(config.sshKeyPath)) {
    connectConfig.privateKey = fs.readFileSync(config.sshKeyPath);
  } else if (config.sshPassword) {
    connectConfig.password = config.sshPassword;
  } else {
    console.error('❌ 请配置 SSH 密钥或密码');
    process.exit(1);
  }

  conn.connect(connectConfig);
}

watch();
