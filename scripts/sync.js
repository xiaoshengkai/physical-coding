const fs = require('fs');
const path = require('path');
const { Client } = require('ssh2');

const CONFIG_PATH = path.join(__dirname, '../config/config.json');

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

async function syncDirectory(conn, localDir, remoteDir) {
  const files = fs.readdirSync(localDir);

  for (const file of files) {
    const localPath = path.join(localDir, file);
    const remotePath = `${remoteDir}/${file}`;
    const stat = fs.statSync(localPath);

    if (stat.isDirectory()) {
      await new Promise((resolve, reject) => {
        conn.exec(`mkdir -p ${remotePath}`, (err) => {
          if (err) reject(err);
          else resolve();
        });
      });
      await syncDirectory(conn, localPath, remotePath);
    } else {
      console.log(`  📤 同步: ${file}`);
      await syncToPi(conn, localPath, remotePath);
    }
  }
}

function sync() {
  const config = loadConfig();
  const conn = new Client();

  conn.on('ready', async () => {
    console.log('✅ 已连接到树莓派\n');
    console.log('📦 正在同步代码...');

    try {
      await new Promise((resolve, reject) => {
        conn.exec(`mkdir -p ${config.remoteDir}`, (err) => {
          if (err) reject(err);
          else resolve();
        });
      });

      const projectDir = path.join(__dirname, '..');
      await syncDirectory(conn, projectDir, config.remoteDir);
      console.log('✅ 同步完成！');
    } catch (err) {
      console.error('❌ 同步失败:', err.message);
    }

    conn.end();
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

sync();
