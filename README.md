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

## 二、在灵基中安装智能体

灵基平台需要通过内部注册才能识别智能体，仅手动复制文件不够。请通过灵基的「智能体开发」智能体来完成安装。

### 2.1 启动安装

1. 打开灵基桌面客户端
2. 点击左侧导航栏「开发」→「智能体开发」
3. 点击官方的**「智能体开发」**智能体，进入对话
4. 将以下内容复制粘贴发送给灵基 AI：

```
请帮我安装效贷测试专家智能体。操作步骤：
1. 从 GitHub 克隆：git clone https://github.com/hansonzhang0606-ux/xiaodai-test-expert-bylingee 到临时目录
2. 用 init-agent.js 创建智能体，名称 xiaodai-testing-expert，显示名"效贷测试专家"，domain 为 it
3. 把克隆下载的 skills 文件夹、agent.md、avatar.png 复制覆盖到创建的智能体目录中
4. 用 add-skill.js 绑定 skills/ai-test-workflow-skill 技能
```

### 2.2 等待安装完成

灵基 AI 会自动执行上述 4 个步骤（克隆代码、创建智能体、复制文件、绑定技能）。完成后效贷测试专家会出现在智能体列表中。

### 2.3 确认安装结果

1. 在灵基中点击「智能体开发」页面
2. 列表中应出现「效贷测试专家」
3. 点击进入后点击「测试」按钮验证是否可用

> 如果测试时报错「测试环境未找到技能」，等待几分钟后再次点击「测试」即可。

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

## 五、确认安装

安装完成后（第二步），在灵基中确认智能体可用：

1. 点击左侧导航栏「开发」→「智能体开发」
2. 列表中应出现「效贷测试专家」
3. 点击进入后点击「测试」按钮
4. 系统会自动打开浏览器进入测试会话页面

> 如果报错「测试环境未找到技能」，等待几分钟后再次点击「测试」即可。

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

当管理员更新了智能体后，GitHub 仓库会有新版本。

### 更新方式

在灵基中打开「智能体开发」智能体对话，发送：

```
https://github.com/hansonzhang0606-ux/xiaodai-test-expert-bylingee 有更新，请重新同步更新下。
```

> `time_tracking_config.yaml` 已被 .gitignore 排除，更新不会覆盖你的 MySQL 配置。

### 更新后如何生效

**必须打开一个新会话**才能让更新生效。灵基在启动新会话时才会重新读取智能体配置和技能文件，旧会话使用的是缓存的旧版本。

1. 在灵基 web 页面中，不要继续旧对话
2. 新建一个对话，选择效贷测试专家
3. 新会话中自动使用最新配置和技能文件

> 如果更新后仍使用旧版本，回到灵基桌面客户端的智能体编辑页面点击「保存」，强制平台重新加载配置，再开新会话。
