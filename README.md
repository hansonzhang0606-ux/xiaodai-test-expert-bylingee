# 效贷测试专家 — 安装指南

## 前置条件

- 已安装 [灵基](https://lingee.kingdee.com) 桌面客户端并登录
- 本机已安装 Python 3.8+ 和 pip
- 本机已安装 Node.js 18+（Confluence 功能需要）

## 安装步骤

### 第 1 步：下载智能体文件

```bash
git clone <仓库地址> xiaodai-testing-expert
```

或直接下载 ZIP 压缩包并解压。

### 第 2 步：放入灵基智能体目录

将 `xiaodai-testing-expert` 目录复制到灵基的 `ai-partners/` 目录下：

```
C:\Users\<你的用户名>\.lingeebuild\ai-partners\xiaodai-testing-expert\
```

> 如果 `ai-partners/` 目录不存在，手动创建即可。

### 第 3 步：配置 MySQL 连接

```bash
cd skills\ai-test-workflow-skill\config
copy time_tracking_config.yaml.template time_tracking_config.yaml
```

编辑 `time_tracking_config.yaml`，填写 MySQL 连接信息（向管理员获取）：

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

### 第 4 步：安装 Python 依赖

```bash
pip install pymysql pyyaml
```

### 第 5 步：在灵基中导入智能体

1. 打开灵基客户端
2. 进入「智能体开发」页面
3. 智能体应自动出现在列表中（如未出现，尝试刷新）
4. 点击进入效贷测试专家 → 点击「测试」验证是否可用

### 第 6 步（可选）：配置 Confluence MCP

如果你需要使用 Confluence 页面提取功能，需要额外配置 MCP 桥接服务：

1. 安装桥接工具：`npm install -g supergateway`
2. 创建启动脚本（向管理员获取 `start-confluence-mcp.bat`）
3. 运行启动脚本，保持窗口开启
4. 在灵基「开发配置」→「MCP」中添加 MCP 服务器：
   - 名称：`atlassian-confluence-mcp-server`
   - 类型：远程
   - URL：`http://localhost:8000/mcp`
   - 启用：是

> Confluence 功能为可选项。不配置也能正常使用本地文档整理、需求评审、测试点生成、用例细化、知识入库等全部核心功能。

## 验证安装

启动效贷测试专家会话，进行以下验证：

| 验证项 | 操作 | 预期结果 |
|--------|------|---------|
| 身份验证 | 输入你的姓名 | 验证通过，开始服务 |
| MySQL 连接 | 完成任一步骤后反馈时间 | 数据写入 MySQL |
| 查看统计 | 输入「查看时间节省统计」 | 生成 HTML 报告 |

## 目录结构

```
xiaodai-testing-expert/
├── assistant.json          # 智能体配置
├── agent.md                # 角色提示词
├── avatar.png              # 头像
├── .gitignore              # Git 忽略规则
└── skills/
    └── ai-test-workflow-skill/
        ├── SKILL.md        # 技能说明
        ├── config/
        │   ├── time_tracking_config.yaml.template  # ← 复制并填写
        │   ├── time_tracking_config.yaml           # ← 你的实际配置（不提交 Git）
        │   ├── team_roster.yaml                    # 花名册
        │   └── defaults.yaml                       # 默认配置
        ├── prompts/        # 各步骤执行规则
        ├── scripts/        # Python 脚本
        └── templates/       # 用例模板和知识库模板
```

## 常见问题

**Q: 启动时报「测试环境未找到技能」？**
A: 确保目录放在 `.lingeebuild/ai-partners/` 下，且目录名为 `xiaodai-testing-expert`。在灵基 UI 中刷新智能体列表。

**Q: MySQL 连接失败？**
A: 检查 `time_tracking_config.yaml` 中的连接信息是否正确，网络是否能访问 MySQL 服务器。运行 `python -c "import pymysql; print(pymysql.install_as_MySQLdb())"` 验证驱动已安装。

**Q: Confluence 提取不可用？**
A: 参见第 6 步配置 MCP 桥接服务。如不需要 Confluence 功能可跳过。
