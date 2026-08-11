# CHANGELOG

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
