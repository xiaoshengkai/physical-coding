const fs = require('fs');
const path = require('path');
const inquirer = require('inquirer').default;

const CONFIG_PATH = path.join(__dirname, '../config/config.json');

async function setup() {
  console.log('\n=== Physical Coding 配置向导 ===\n');

  let existingConfig = {};
  if (fs.existsSync(CONFIG_PATH)) {
    existingConfig = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    console.log('已找到配置文件，是否要更新？\n');
  }

  const questions = [
    {
      type: 'input',
      name: 'raspberryPiIp',
      message: '树莓派 IP 地址:',
      default: existingConfig.raspberryPiIp || '192.168.1.100',
      validate: (input) => {
        const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
        const domainRegex = /^[a-zA-Z0-9][-a-zA-Z0-9]*(\.[a-zA-Z0-9][-a-zA-Z0-9]*)+$/;
        return ipRegex.test(input) || domainRegex.test(input) || '请输入有效的 IP 地址或域名';
      }
    },
    {
      type: 'input',
      name: 'sshUser',
      message: 'SSH 用户名:',
      default: existingConfig.sshUser || 'pi'
    },
    {
      type: 'input',
      name: 'sshPort',
      message: 'SSH 端口:',
      default: existingConfig.sshPort || 22,
      validate: (input) => {
        return !isNaN(input) && input > 0 && input < 65536 || '请输入有效的端口号';
      }
    },
    {
      type: 'input',
      name: 'remoteDir',
      message: '代码同步目标目录:',
      default: existingConfig.remoteDir || '/home/pi/PhysicalCoding'
    },
    {
      type: 'input',
      name: 'sshKeyPath',
      message: 'SSH 密钥路径 (可选，直接回车使用密码):',
      default: existingConfig.sshKeyPath || ''
    },
    {
      type: 'input',
      name: 'sshPassword',
      message: 'SSH 密码 (如果未使用密钥):',
      default: existingConfig.sshPassword || ''
    }
  ];

  const answers = await inquirer.prompt(questions);

  const config = {
    raspberryPiIp: answers.raspberryPiIp,
    sshUser: answers.sshUser,
    sshPort: parseInt(answers.sshPort),
    remoteDir: answers.remoteDir,
    sshKeyPath: answers.sshKeyPath || null,
    sshPassword: answers.sshPassword || null
  };

  const configDir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }

  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  console.log('\n✅ 配置已保存!\n');
  console.log('接下来可以运行:');
  console.log('  npm run connect  - 连接树莓派');
  console.log('  npm run watch    - 监听代码变更\n');
}

setup().catch(console.error);
