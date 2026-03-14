const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_PATH = path.join(__dirname, '../config/config.json');

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在，请先运行: npm run setup');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function syncDirectory(config, localDir, remoteDir) {
  const files = fs.readdirSync(localDir);
  
  for (const file of files) {
    // 跳过不需要同步的目录
    const skipDirs = ['.git', 'node_modules', '.ruff_cache'];
    if (skipDirs.includes(file)) continue;
    
    const localPath = path.join(localDir, file);
    const remotePath = `${remoteDir}/${file}`;
    const stat = fs.statSync(localPath);

    if (stat.isDirectory()) {
      try {
        execSync(
          `sshpass -p "${config.sshPassword}" ssh -o StrictHostKeyChecking=no -p ${config.sshPort} ${config.sshUser}@${config.raspberryPiIp} "mkdir -p ${remotePath}"`,
          { encoding: 'utf8', stdio: 'ignore' }
        );
      } catch (e) {}
      syncDirectory(config, localPath, remotePath);
    } else {
      console.log(`  📤 同步: ${file}`);
      try {
        execSync(
          `sshpass -p "${config.sshPassword}" scp -o StrictHostKeyChecking=no -P ${config.sshPort} "${localPath}" "${config.sshUser}@${config.raspberryPiIp}:${remotePath}"`,
          { encoding: 'utf8', stdio: 'ignore' }
        );
      } catch (e) {
        console.log(`  ❌ 同步失败: ${file}`);
      }
    }
  }
}

function sync() {
  const config = loadConfig();
  
  console.log('✅ 已连接到树莓派（通过 sshpass）\n');
  console.log('📦 正在同步代码...');

  try {
    execSync(
      `sshpass -p "${config.sshPassword}" ssh -o StrictHostKeyChecking=no -p ${config.sshPort} ${config.sshUser}@${config.raspberryPiIp} "mkdir -p ${config.remoteDir}"`,
      { encoding: 'utf8', stdio: 'ignore' }
    );

    const projectDir = path.join(__dirname, '..');
    syncDirectory(config, projectDir, config.remoteDir);
    console.log('\n✅ 同步完成！');
  } catch (err) {
    console.error('\n❌ 同步失败:', err.message);
    process.exit(1);
  }
}

sync();
