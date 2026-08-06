# 效贷测试专家 — 安装指南

> 灵基智能体 | 效贷业务线功能测试专家
> 仓库地址：https://github.com/hansonzhang0606-ux/xiaodai-test-expert-bylingee

## 一、环境准备

如果以下软件已安装可跳过对应步骤。打开命令提示符（Win+R 输入 `cmd`）逐一验证。

### 1.1 Git（用于 clone 仓库）

验证：`git --version`，显示版本号即可。

未安装则下载安装：https://git-scm.com/download/win，一路 Next 默认安装即可（自带 Git Credential Manager，首次 push 会弹出浏览器登录 GitHub）。

> 如果不想安装 Git，也可以直接在浏览器打开仓库页面，点击绿色「Code」按钮 → 「Download ZIP」下载压缩包，解压即可。

### 1.2 Python 3.8+（运行测试脚本和 MySQL 同步）

验证：`python --version`，显示 3.8 以上即可。

未安装则下载安装：https://www.python.org/downloads/

**安装时注意**：勾选底部「Add Python to PATH」选项，否则后续命令找不到 python。

安装完成后打开**新的**命令提示符，执行：

```bash
pip install pymysql pyyaml
```

### 1.3 Node.js 18+（仅 Confluence 功能需要）

验证：`node --version`，显示 v18 以上即可。

未安装则下载安装：https://nodejs.org/ 选择 LTS 版本。

> Node.js 仅在使用 Confluence 页面提取功能时需要。不需要 Confluence 功能可跳过。

### 1.4 灵基桌面客户端

从 https://lingee.kingdee.com 下载安装并登录。

---

## 二、下载智能体

### 方式 A：Git Clone（推荐）

打开本地命令提示窗口，执行：

```bash
cd C:\Users\kingdee\.lingeebuild\ai-partners
```

（若没有 ai-partners 文件夹，先手动新建）

然后再执行：

```bash
git clone https://github.com/hansonzhang0606-ux/xiaodai-test-expert-bylingee xiaodai-testing-expert
```

### 方式 B：下载 ZIP（无需安装 Git）

1. 浏览器打开 https://github.com/hansonzhang0606-ux/xiaodai-test-expert-bylingee
2. 点击绿色「Code」按钮 → 「Download ZIP」
3. 解压 ZIP 文件
4. 将解压出的文件夹重命名为 `xiaodai-testing-expert`
5. 移动到 `%USERPROFILE%\.lingeebuild\ai-partners\xiaodai-testing-expert`

> 如果 `.lingeebuild\ai-partners` 目录不存在，手动创建即可。
> 快捷打开：Win+R 输入 `%USERPROFILE%\.lingeebuild` 回车。

最终目录结构应为：

```
C:\Users\<你的用户名>\.lingeebuild\ai-partners\xiaodai-testing-expert\
├── assistant.json
├── agent.md
├── avatar.png
├── README.md
├── .gitignore
└── skills\
    └── ai-test-workflow-skill\
        ├── SKILL.md
        ├── config\
        ├── prompts\
        ├── scripts\
        └── templates\
```

---

## 三、配置 MySQL 连接

时间追踪功能需要连接共享 MySQL 数据库（向管理员获取连接信息）。

### 3.1 复制配置模板

手动将 `skills\ai-test-workflow-skill\config\` 目录下的 `time_tracking_config.yaml.template` 文件复制一份，重命名为 `time_tracking_config.yaml`。

### 3.2 填写连接信息

用记事本打开 `time_tracking_config.yaml`，找到 `mysql:` 段，替换为管理员提供的值：

```yaml
mysql:
  host: "管理员提供的地址"
  port: 3306
  user: "管理员提供的用户名"
  password: "管理员提供的密码"
  database: "管理员提供的数据库名"
  table: "time_tracking"
  charset: "utf8mb4"
```

保存文件。此文件已被 `.gitignore` 排除，不会泄露到 GitHub。

---

## 四、安装 Python 依赖

```bash
pip install pymysql pyyaml
```

验证安装成功：

```bash
python -c "import pymysql; import yaml; print('OK')"
```

> 如果报错 `No module named pymysql`，确认 Python 安装时勾选了「Add Python to PATH」，重新打开命令提示符再试。

---

## 五、在灵基中导入智能体

### 5.1 确认文件位置正确

打开文件资源管理器，确认以下路径存在 `assistant.json` 文件：

```
C:\Users\kingdee\.lingeebuild\ai-partners\xiaodai-testing-expert\assistant.json
```

> 快捷打开：Win+R 输入 `%USERPROFILE%\.lingeebuild\ai-partners` 回车。

### 5.2 重启灵基客户端

如果灵基客户端正在运行，先完全关闭（右键托盘图标 → 退出），然后重新打开。

### 5.3 查找智能体

1. 打开灵基桌面客户端
2. 进入「智能体开发」页面
3. 效贷测试专家应出现在列表中

### 5.4 如果列表中仍看不到

依次尝试以下方法：

1. **点击右上角刷新按钮**刷新智能体列表
2. **完全退出灵基**（右键系统托盘图标 → 退出），重新打开
3. 检查目录名是否正确：必须是 `xiaodai-testing-expert`（不是 `xiaodai-test-expert-bylingee`）
4. 检查 `assistant.json` 是否在该目录下且内容不为空

### 5.5 测试智能体

1. 点击进入效贷测试专家
2. 点击「测试」按钮验证是否可用

> 如果报错「测试环境未找到技能」，检查目录名是否为 `xiaodai-testing-expert`（不是 `xiaodai-test-expert-bylingee`），确认放在 `ai-partners\` 目录下。

---

## 六、配置 Confluence MCP（可选）

> 此功能为可选项。不配置也能正常使用本地文档整理、需求评审、测试点生成、用例细化、知识入库等全部核心功能。仅当需要从 Confluence 在线页面提取需求文档时才需要。

### 6.1 安装桥接工具

```bash
npm install -g supergateway
```

### 6.2 创建启动脚本

在 `%USERPROFILE%\.lingeebuild\` 目录下创建 `start-confluence-mcp.bat`，内容向管理员获取。

### 6.3 运行桥接服务

双击 `start-confluence-mcp.bat`，保持窗口开启。

### 6.4 在灵基中配置 MCP

1. 灵基中打开效贷测试专家的「开发配置」→「MCP」选项卡
2. 点击「+ 添加 MCP」
3. 填写：
   - 名称：`atlassian-confluence-mcp-server`
   - 类型：远程
   - URL：`http://localhost:8000/mcp`
   - 启用：是
4. 保存，刷新列表，状态应显示已连接

---

## 七、验证安装

启动效贷测试专家会话，进行以下验证：

| 验证项 | 操作 | 预期结果 |
|--------|------|---------|
| 身份验证 | 输入你的姓名（花名册中的名字） | 验证通过，开始服务 |
| 身份拒绝 | 输入不在花名册的名字 | 拒绝服务 |
| 本地文档整理 | 提供一个本地需求文档目录 | 生成整理版 MD |
| MySQL 连接 | 完成任一步骤后反馈时间节省 | 数据写入 MySQL |
| 查看统计 | 输入「查看时间节省统计」 | 生成 HTML 报告并提供路径 |

---

## 八、常见问题

**Q: 安装后灵基中看不到效贷测试专家？**
A: 检查目录路径是否为 `%USERPROFILE%\.lingeebuild\ai-partners\xiaodai-testing-expert\`（注意目录名是 `xiaodai-testing-expert` 不是 `xiaodai-test-expert-bylingee`）。确认 `assistant.json` 文件在该目录下。

**Q: 报错「测试环境未找到技能」？**
A: 同上，检查目录名和路径是否正确。确保从 ZIP 解压后已将文件夹重命名为 `xiaodai-testing-expert`。

**Q: MySQL 连接失败？**
A: 1) 检查 `time_tracking_config.yaml` 中的连接信息是否正确；2) 确认网络能访问 MySQL 服务器（`ping 管理员提供的IP`）；3) 运行 `python -c "import pymysql; print('OK')"` 确认驱动已安装。

**Q: pip install 报错？**
A: 可能是 Python 未加入 PATH。重新运行 Python 安装程序，勾选「Add Python to PATH」，或手动将 Python 安装目录和 Scripts 目录添加到系统环境变量 PATH 中。

**Q: Confluence 提取不可用？**
A: 参见第六步。确认桥接服务窗口在运行中（不要关闭）。如不需要 Confluence 功能可跳过。

**Q: 时间追踪数据写入了本地但没有同步到 MySQL？**
A: 检查 `time_tracking_config.yaml` 中 `storage_mode` 是否为 `"mysql"`。查看 AI 输出中是否有 `MYSQL_SYNC: success` 或 `MYSQL_SYNC: failed` 信息。

---

## 九、目录结构

```
xiaodai-testing-expert/
├── assistant.json          # 智能体配置（灵基读取）
├── agent.md                # 角色提示词
├── avatar.png              # 头像
├── README.md               # 本文件
├── .gitignore              # Git 忽略规则
└── skills/
    └── ai-test-workflow-skill/
        ├── SKILL.md        # 技能说明
        ├── manifest.yaml   # 技能清单
        ├── config/
        │   ├── time_tracking_config.yaml.template  # ← 复制为 .yaml 并填写
        │   ├── time_tracking_config.yaml           # ← 你的实际配置（不入 Git）
        │   ├── team_roster.yaml                    # 花名册（效贷4人）
        │   ├── defaults.yaml                       # 默认配置
        │   └── smartsheet_template.yaml            # 表格模板
        ├── prompts/        # 7个步骤的执行规则文档
        ├── scripts/        # 10个 Python 脚本 + MySQL 工具
        └── templates/      # 用例模板和知识库模板
```

---

## 十、后续更新

当管理员更新了智能体后，GitHub 仓库会有新版本。更新方式：

**Git 方式：**
```bash
cd %USERPROFILE%\.lingeebuild\ai-partners\xiaodai-testing-expert
git pull origin main
```

> `time_tracking_config.yaml` 已被 .gitignore 排除，git pull 不会覆盖你的配置。

**ZIP 方式：**
重新下载 ZIP，解压覆盖目录（注意不要覆盖 `time_tracking_config.yaml`）。
