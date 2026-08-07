-- ============================================================
--  重命名 MySQL 表
--  执行前提：auto_efficiency_platform 数据库中已存在旧表
-- ============================================================

USE auto_efficiency_platform;

-- time_tracking → agent_time_tracking
RENAME TABLE time_tracking TO agent_time_tracking;

-- team_roster → agent_team_roster
RENAME TABLE team_roster TO agent_team_roster;

-- 验证
SHOW TABLES LIKE 'agent_%';
