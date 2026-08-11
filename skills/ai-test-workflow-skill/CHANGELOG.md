# CHANGELOG

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
