-- ============================================================
--  效贷测试专家 — 时间追踪 MySQL 表结构
--  跨业务线共享：所有业务线的测试专家写入同一张表，
--  通过 biz_line（中文名）和 biz_line_code（编码）区分。
--
--  数据库名: testing_metrics（可改为现有数据库名）
--  表名: agent_time_tracking
--
--  业务线编码枚举：
--    XD    = 效贷
--    JWY   = 泾渭云
--    XR    = 效融
--    XXD   = 小贷
--    ZHJ   = 智慧记+运营系统
--    AIJXC = AI进销存
--    ZHJLS = 智慧记零售
-- ============================================================

CREATE TABLE IF NOT EXISTS agent_time_tracking (
    id               INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    timestamp        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
    date             DATE           NOT NULL                          COMMENT '日期',
    biz_line         VARCHAR(50)    NOT NULL                          COMMENT '业务线（中文名称）',
    biz_line_code    VARCHAR(10)    NOT NULL                          COMMENT '业务线编码（XD/JWY/XR/XXD/ZHJ/AIJXC/ZHJLS）',
    employee         VARCHAR(100)   NOT NULL                          COMMENT '员工姓名',
    user_story       VARCHAR(255)   NOT NULL                          COMMENT '用户故事名称',
    user_story_code  VARCHAR(50)    DEFAULT ''                        COMMENT '用户故事编号（如 US-001）',
    step             VARCHAR(50)    NOT NULL                          COMMENT '步骤名称',
    step_code        VARCHAR(10)    NOT NULL                          COMMENT '步骤编码',
    time_saved_hours DECIMAL(10,2)  NOT NULL                          COMMENT '节省小时数',
    time_saved_pd    DECIMAL(10,2)  NOT NULL                          COMMENT '节省人天数',
    total_hours      DECIMAL(10,2)  NOT NULL                          COMMENT '折算总小时',
    agent_start_time DATETIME       DEFAULT NULL                      COMMENT '智能体开始执行时间',
    agent_end_time   DATETIME       DEFAULT NULL                      COMMENT '智能体完成执行时间',
    agent_duration_minutes DECIMAL(10,2) DEFAULT NULL                COMMENT '智能体实际耗时（分钟，=end-start）',
    remark           TEXT                                             COMMENT '备注（可选）',

    INDEX idx_employee      (employee),
    INDEX idx_biz_line      (biz_line),
    INDEX idx_biz_line_code (biz_line_code),
    INDEX idx_step_code     (step_code),
    INDEX idx_date          (date),
    INDEX idx_user_story    (user_story),
    INDEX idx_user_story_code (user_story_code)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='测试专家时间节省追踪表（跨业务线共享）';

-- ============================================================
--  花名册表 — 测试人员身份验证
--  跨业务线共享：通过 biz_line 区分各业务线人员。
--  AI 会话启动时通过 verify_team_member.py 查询此表验证身份。
--  active=true 表示在职，false 表示离职（保留记录不删除）。
-- ============================================================

CREATE TABLE IF NOT EXISTS agent_team_roster (
    id               INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    biz_line         VARCHAR(50)    NOT NULL                          COMMENT '业务线（中文名称）',
    name             VARCHAR(100)   NOT NULL                          COMMENT '员工姓名',
    role             VARCHAR(50)    NOT NULL DEFAULT '功能测试'        COMMENT '岗位角色',
    employee_id      VARCHAR(50)    DEFAULT ''                        COMMENT '工号（选填）',
    active           TINYINT(1)     NOT NULL DEFAULT 1                 COMMENT '是否在职（1=在职, 0=离职）',
    created_at       DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at       DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    UNIQUE KEY uk_biz_name (biz_line, name),
    INDEX idx_biz_line (biz_line),
    INDEX idx_active   (active)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='测试人员花名册（身份验证用，跨业务线共享）';

-- 初始数据：效贷业务线测试人员
INSERT INTO agent_team_roster (biz_line, name, role, employee_id, active) VALUES
    ('效贷', '吴香康', '功能测试', '', 1),
    ('效贷', '周峰',   '功能测试', '', 1),
    ('效贷', '何甜',   '功能测试', '', 1),
    ('效贷', '张云星', '功能测试', '', 1)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- ============================================================
--  迁移语句：如果表已存在，手动执行以下 ALTER 添加新字段
-- ============================================================
-- ALTER TABLE agent_time_tracking
--   ADD COLUMN user_story_code VARCHAR(50) DEFAULT '' COMMENT '用户故事编号（如 US-001）' AFTER user_story,
--   ADD COLUMN agent_start_time DATETIME DEFAULT NULL COMMENT '智能体开始执行时间' AFTER total_hours,
--   ADD COLUMN agent_end_time DATETIME DEFAULT NULL COMMENT '智能体完成执行时间' AFTER agent_start_time,
--   ADD COLUMN agent_duration_minutes DECIMAL(10,2) DEFAULT NULL COMMENT '智能体实际耗时（分钟）' AFTER agent_end_time,
--   ADD INDEX idx_user_story_code (user_story_code);
