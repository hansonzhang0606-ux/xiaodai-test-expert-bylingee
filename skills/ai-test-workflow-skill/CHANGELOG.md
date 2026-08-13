# CHANGELOG

## 2.8.0 — 2026-08-13
### Added
- agent_time_tracking 表新增字段：user_story_code（用户故事编号）、agent_start_time（智能体开始时间）、agent_end_time（智能体完成时间）、agent_duration_minutes（智能体实际耗时分钟，自动计算）
- record_time_saved.py 新增 --user-story-code、--agent-start、--agent-end 参数
- mysql_helper.py insert_record 支持新字段，含旧表兼容回退

### Changed
- init_mysql.sql 增加新字段定义和迁移 ALTER 语句
- time_tracking.md 更新数据格式、脚本用法、流程说明
- SKILL.md 脚本用法更新新参数

## 2.7.1 — 2026-08-12
### Fixed
- 将 config/ 目录迁移为 .time_tracking_config.yaml 隐藏文件（消除非标准目录 warn）
- 删除 config/ 中的重复模板文件（已存在于 references/config/）
- 更新所有脚本和文档中的配置文件路径引用

### Changed
- 精简 SKILL.md 正文（目录结构、知识库、项目配置等章节），降低 token 数

## 2.7.0 — 2026-08-12
### Added
- 新增强制约束#7：每步产出文件内容必须直接展示在对话中，使用 read 工具读取文件后输出到回复文本
- 支持文本文件(MD/JSON)全文展示、Excel 表格摘要展示、XMind 树形结构展示
- 用户无需访问 AI 沙箱文件系统即可在对话中直接审阅产出物

### Changed
- 产出物清单增加 📤 内容展示标记
- 使用示例增加 📤 read 展示文件内容步骤

## 2.6.0 — 2026-08-12
### Changed
- 将时间节省追踪从"脚本说明"提升为强制约束（步骤①②④⑥⑦完成后必须收集用户反馈并写入 MySQL agent_time_tracking 表）
- SKILL.md 新增强制约束 #5（每步完成后强制时间节省反馈）和 #6（时间节省分析报告）
- 核心流程表、产出物清单、用户指令识别表、使用示例中均增加时间追踪标记
- "采纳"规则从"取参考值上限"改为"取参考范围中间值"（如参考2~3小时则取2.5小时）
- 解析规则增加"3h""1天""1.2人天"等示例
- 脚本使用章节标注"⛔ 每步完成后强制调用"
- 详细文档索引更新 time_tracking.md 描述为 v5

## 2.5.0 — 2026-08-11
### Changed
- 将 prompts/、config/（模板文件）、templates/ 迁移到标准目录 references/ 下，使这些文件在平台提交时能正确上传
- 更新 SKILL.md 和脚本中所有路径引用（prompts/ → references/prompts/，config/ → references/config/，templates/ → references/templates/）
- config/time_tracking_config.yaml 保留在 config/ 目录（运行时配置，含敏感信息，不上传）

## 2.4.2 — 2026-08-11
### Fixed
- 模板化 `prompts/confluence_extract.md` 中的 Confluence 凭据，移除明文用户名密码，替换为占位符

### Changed
- 删除 `config/team_roster.yaml` 和 `record_time_saved.py` 中的 `load_team_roster()` 死代码，身份验证已全部走 MySQL `agent_team_roster` 表

## 2.4.1 — 2026-08-06
### Changed
- 技能名称从 ai-testcase-workflow-skill 修改为 ai-test-workflow-skill，同步更新目录名和 SKILL.md 正文引用

## 2.4.0 — 2026-06-23
### Changed
- 简化执行模式 3→2（原模式B合并到模式B单步），知识库默认轻量路径（仅读精华库），用户说"结合历史"时走完整路径
