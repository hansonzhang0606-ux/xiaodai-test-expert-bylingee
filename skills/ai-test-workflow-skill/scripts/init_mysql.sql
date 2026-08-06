-- ============================================================
--  效贷测试专家 — 时间追踪 MySQL 表结构
--  跨业务线共享：所有业务线的测试专家写入同一张表，
--  通过 biz_line（中文名）和 biz_line_code（编码）区分。
--
--  数据库名: testing_metrics（可改为现有数据库名）
--  表名: time_tracking
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

CREATE TABLE IF NOT EXISTS time_tracking (
    id               INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    timestamp        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
    date             DATE           NOT NULL                          COMMENT '日期',
    biz_line         VARCHAR(50)    NOT NULL                          COMMENT '业务线（中文名称）',
    biz_line_code    VARCHAR(10)    NOT NULL                          COMMENT '业务线编码（XD/JWY/XR/XXD/ZHJ/AIJXC/ZHJLS）',
    employee         VARCHAR(100)   NOT NULL                          COMMENT '员工姓名',
    user_story       VARCHAR(255)   NOT NULL                          COMMENT '用户故事',
    step             VARCHAR(50)    NOT NULL                          COMMENT '步骤名称',
    step_code        VARCHAR(10)    NOT NULL                          COMMENT '步骤编码',
    time_saved_hours DECIMAL(10,2)  NOT NULL                          COMMENT '节省小时数',
    time_saved_pd    DECIMAL(10,2)  NOT NULL                          COMMENT '节省人天数',
    total_hours      DECIMAL(10,2)  NOT NULL                          COMMENT '折算总小时',
    remark           TEXT                                             COMMENT '备注（可选）',

    INDEX idx_employee      (employee),
    INDEX idx_biz_line      (biz_line),
    INDEX idx_biz_line_code (biz_line_code),
    INDEX idx_step_code     (step_code),
    INDEX idx_date          (date),
    INDEX idx_user_story    (user_story)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='测试专家时间节省追踪表（跨业务线共享）';
