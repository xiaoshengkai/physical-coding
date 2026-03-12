const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
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

async function main() {
  const config = loadConfig();
  const conn = new Client();

  console.log('🔌 正在连接树莓派...\n');

  await new Promise((resolve, reject) => {
    conn.on('ready', resolve);
    conn.on('error', reject);

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
  });

  console.log('✅ 已连接\n');

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
    console.log('✅ 同步完成\n');
  } catch (err) {
    console.error('❌ 同步失败:', err.message);
  }

  conn.end();

  const demoPath = `${config.remoteDir}/demos`;
  const sshArgs = [
    '-p', config.sshPort.toString(),
    `${config.sshUser}@${config.raspberryPiIp}`
  ];

  if (config.sshKeyPath) {
    sshArgs.push('-i', config.sshKeyPath);
  }

  console.log(`🚀 正在进入 demos 目录: ${demoPath}\n`);

  const fullArgs = [...sshArgs, `cd ${demoPath} && $SHELL -l`];

  if (config.sshPassword && !config.sshKeyPath) {
    const sshpass = spawn('sshpass', ['-p', config.sshPassword, 'ssh', ...fullArgs], {
      stdio: 'inherit'
    });
    sshpass.on('close', (code) => process.exit(code));
    return;
  }

  const ssh = spawn('ssh', fullArgs, {
    stdio: 'inherit'
  });

  ssh.on('close', (code) => {
    process.exit(code);
  });
}

main().catch(console.error);
