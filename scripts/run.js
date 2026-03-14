const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

const CONFIG_PATH = path.join(__dirname, '../config/config.json');

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在，请先运行: npm run setup');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function findDemoPath(input) {
  const demosDir = path.join(__dirname, '../demos');
  
  if (!fs.existsSync(demosDir)) {
    console.error('❌ demos 目录不存在');
    process.exit(1);
  }
  
  const entries = fs.readdirSync(demosDir, { withFileTypes: true });
  
  const exactPath = path.join(demosDir, input);
  if (fs.existsSync(exactPath) && fs.statSync(exactPath).isFile()) {
    return { fullPath: exactPath, demoName: path.basename(path.dirname(exactPath)) };
  }
  
  const matched = entries.find(e => e.name.startsWith(input) || e.name.startsWith('0' + input));
  if (matched) {
    const demoDir = path.join(demosDir, matched.name);
    const pyFiles = fs.readdirSync(demoDir).filter(f => f.endsWith('.py'));
    if (pyFiles.length > 0) {
      const fullPath = path.join(demoDir, pyFiles[0]);
      return { fullPath, demoName: matched.name };
    }
  }
  
  return null;
}

function syncWithSftp(config, localDir, remoteDir) {
  return new Promise((resolve, reject) => {
    const files = fs.readdirSync(localDir).filter(f => f.endsWith('.py') || f.endsWith('.md'));
    const sftpCommands = files.map(f => `put "${path.join(localDir, f)}" "${remoteDir}/${f}"`).join('\n');
    
    const proc = spawn('sshpass', [
      '-p', config.sshPassword,
      'sftp',
      '-o', 'StrictHostKeyChecking=no',
      '-P', config.sshPort.toString(),
      `${config.sshUser}@${config.raspberryPiIp}`
    ], {
      shell: true,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    let output = '';
    let error = '';
    
    proc.stdout.on('data', (data) => { output += data.toString(); });
    proc.stderr.on('data', (data) => { error += data.toString(); });
    
    proc.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(error || `sftp failed with code ${code}`));
    });
    
    proc.on('error', reject);
    
    proc.stdin.write(`mkdir -p ${remoteDir}\n`);
    proc.stdin.write(sftpCommands + '\n');
    proc.stdin.write('bye\n');
  });
}

function killRemoteProcess(config, demoName) {
  return new Promise((resolve) => {
    try {
      execSync(
        `sshpass -p "${config.sshPassword}" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p ${config.sshPort} ${config.sshUser}@${config.raspberryPiIp} "pkill -9 -f 'python3.*tft-display' || pkill -9 -f 'python3.*${demoName}' || killall -9 python3"`,
        { encoding: 'utf8', stdio: 'ignore' }
      );
    } catch (e) {
      console.log('⚠️  杀进程失败');
    }
    resolve();
  });
}

function runRemote(config, remoteScriptPath, demoName) {
  return new Promise((resolve, reject) => {
    console.log('='.repeat(50));
    
    const proc = spawn('sshpass', [
      '-p', config.sshPassword,
      'ssh',
      '-o', 'StrictHostKeyChecking=no',
      '-p', config.sshPort.toString(),
      `${config.sshUser}@${config.raspberryPiIp}`,
      `python3 ${remoteScriptPath}`
    ], {
      stdio: 'inherit'
    });
    
    const handleInterrupt = () => {
      console.log('\n\n🛑 正在停止远程进程...');
      killRemoteProcess(config, demoName).then(() => {
        console.log('✅ 远程进程已停止，GPIO 已重置');
        process.exit(0);
      });
    };
    
    proc.on('close', (code) => {
      console.log('='.repeat(50));
      console.log(`🔴 进程退出，代码: ${code}`);
      resolve(code);
    });
    
    proc.on('error', reject);
    
    process.on('SIGINT', handleInterrupt);
    process.on('SIGTERM', handleInterrupt);
  });
}

async function runDemo(input) {
  const config = loadConfig();
  
  console.log(`🔍 查找 Demo: ${input}\n`);
  
  const result = findDemoPath(input);
  if (!result) {
    console.error(`❌ 未找到 demo: ${input}`);
    console.log('📂 可用的 demos:');
    const demosDir = path.join(__dirname, '../demos');
    fs.readdirSync(demosDir, { withFileTypes: true })
      .filter(e => e.isDirectory())
      .forEach(e => console.log(`   - ${e.name}`));
    process.exit(1);
  }
  
  const { fullPath, demoName } = result;
  const relativePath = path.relative(path.join(__dirname, '..'), fullPath);
  console.log(`📍 找到: ${relativePath}\n`);
  
  console.log('✅ 已连接树莓派（通过 sshpass）\n');
  console.log('📦 正在同步代码...');
  
  const localDemosDir = path.join(__dirname, '../demos', demoName);
  const remoteDemosDir = `${config.remoteDir}/demos/${demoName}`;
  
  try {
    await syncWithSftp(config, localDemosDir, remoteDemosDir);
    console.log('✅ 同步完成\n');
  } catch (err) {
    console.error('❌ 同步失败:', err.message);
    process.exit(1);
  }

  const pyFiles = fs.readdirSync(path.dirname(fullPath)).filter(f => f.endsWith('.py'));
  const scriptName = pyFiles[0];
  const remoteScriptPath = `${config.remoteDir}/demos/${demoName}/${scriptName}`;
  
  console.log(`🚀 在树莓派上运行: python3 ${remoteScriptPath}\n`);
  
  await runRemote(config, remoteScriptPath, demoName);
}

const input = process.argv[2];
if (!input) {
  console.log('用法: npm run run <demo-path>');
  console.log('示例:');
  console.log('  npm run run 01-led-blink/led-blink.py');
  console.log('  npm run run 04-traffic-light');
  console.log('  npm run run 04');
  process.exit(1);
}

runDemo(input).catch(console.error);
