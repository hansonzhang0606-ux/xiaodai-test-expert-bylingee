---
name: ai-test-workflow-skill
description: |
  测试用例生成通用 Skill，支持从需求文档到测试用例入库的灵活流程。多项目复用、知识库驱动、AI核心推导、脚本辅助输出。

  支持 2 种执行模式：
  - 模式A（完整流程）：文档整理 → 评审 → 测试点 → 用例 → [可选落库]
  - 模式B（单步模式）：按需执行任意一步（整理/评审/测试点/用例/落库）

  ⚠️ 强制约束（最高优先级）：
  1. 每个阶段开始前，必须完整阅读对应 references/*.md 文档，禁止凭记忆执行
  2. ⛔ 禁止假设已读取 / 禁止简化 Todo / 禁止跳过步骤 / 禁止自行判断 / 禁止假设状态
  3. ⛔ 步骤①完成后不自动触发评审，必须等待用户指令
  4. ⛔ 步骤⑦在所有模式下都是可选的，用户说"入库"时才执行
  5. ⚠️ 进入任何主步骤时，第一步必须追加子流程 Todo（规划动作），禁止先执行操作再追加
  6. ⏱️ 步骤①②④⑥⑦后强制收集时间节省反馈并记录到 MySQL
  7. 📤 每步产出文件内容须直接展示在对话中供审阅，不只是给路径

  📖 规则在各 references/*.md 中。
---

# AI Testcase Workflow Skill

> **测试用例生成通用 Skill，从需求文档到测试用例入库的端到端流水线**

## ✨ 特性

- **多项目复用**：一套 Skill，每个项目独立 `.skill/` 配置和知识库
- **知识库驱动**：历史用例沉淀，精华库持续进化
- **AI 核心推导**：AI 分析需求、推导场景、细化用例，脚本辅助输出
- **灵活执行**：2 种模式适应不同场景
- **⏱️ 效能追踪**：每步完成后强制收集时间节省数据，写入 MySQL，支持分析报告

---

## 🎯 2 种执行模式

| 模式 | 适用场景 | 流程 |
|------|---------|------|
| **A 完整流程** | 新项目/新需求从零开始 | ①→②→③→④→⑤→⑥→[⑦可选] |
| **B 单步模式** | 按需执行任意一步（如已有评审后 XMind 直接生成用例） | 用户指定步骤→执行 |

> 💡 步骤①完成后**不自动触发评审** | 步骤⑦**可选**，用户说"入库"才执行
>
> ⏱️ **强制时间追踪**：步骤①②④⑥⑦完成后，**必须**强制收集用户时间节省反馈并调用 `record_time_saved.py` 写入 MySQL `agent_time_tracking` 表。用户说"查看时间统计"时调用 `generate_time_analytics.py` 生成 HTML 报告。详见 `references/time_tracking.md`

---

## 🔄 核心流程概览（7步）

```
① 文档整理 → ② 需求评审 → ③ 确认评审 → ④ 生成测试点 → ⑤ 评审XMind → ⑥ 生成用例 → [⑦入库知识库]
```

| 步骤 | 名称 | AI 参与 | 输入 | 输出 | 必读文档 | ⛔ 不读的风险 |
|------|------|---------|------|------|----------|-------------|
| ① | 文档整理 | 中 | 需求目录(源文件) | 整理版 MD + source/归档 + ⏱️时间反馈 | `references/document_consolidate.md` | 锚点格式错误、图片未分确定/不确定、增量识别失效、自动触发评审、流程图使用 Mermaid 而非步骤+缩进 |
| ② | 需求评审 | 高 | 整理版 MD + 精华库 | 评审报告 MD+JSON + ⏱️时间反馈 | `references/requirement_review.md` | 遗漏评审维度、JSON 格式错误、精华库未读取、评审了运维细节 |
| ③ | 确认评审 | - | - | - | - | 等待用户确认 |
| ④ | 生成测试点 | 高 | 整理版 MD+评审报告+精华库 | 测试点 JSON+XMind+报告 + ⏱️时间反馈 | `references/testpoint_generate.md` | 测试点格式错误、未去重、缺少处理决策解析、未生成测试点报告 |
| ⑤ | 评审XMind | - | - | {需求名}_测试点.xmind（用户直接在此文件上评审） | - | 用户人工评审 |
| ⑥ | 生成用例 | 高 | {需求名}_测试点.xmind + 整理版 MD | 测试用例 JSON+Excel + reviewed.json（仅模式A）+ ⏱️时间反馈 | `references/testcase_refine.md` | 步骤编号错误、数据未实例化、步骤与预期不对应、Excel 格式错误 |
| ⑦ | 入库知识库 | 中 | 全部产出物 | 知识库更新 + ⏱️时间反馈 | `references/knowledge_base_archive.md` | 命名不规范、重复入库、未提炼精华、进化日志未更新 |

> ⏱️ 步骤③（确认评审）和⑤（评审XMind）是人工操作环节，不追踪时间节省。

---

## 📁 目录结构

```
ai-test-workflow-skill/
├── references/                        # 参考文档与配置模板（上传到平台）
│   ├── document_consolidate.md       # ① 文档整理
│   ├── requirement_review.md         # ② 需求评审
│   ├── testpoint_generate.md         # ④ 测试点生成
│   ├── testcase_refine.md            # ⑥ 用例细化
│   ├── knowledge_base_archive.md     # ⑦ 入库知识库
│   ├── time_tracking.md              # 时间节省追踪
│   ├── config/                       # 配置模板
│   └── templates/                    # 项目配置+知识库模板
├── scripts/                          # Python 脚本
├── SKILL.md                          # 本文档
└── .time_tracking_config.yaml        # 运行时配置（隐藏文件，不上传）
```

---

## 🗂️ 多项目架构

AI 自动识别项目：用户提供任意路径 → 向上查找 `.skill/` (最多3层) → 定位项目根目录。每个项目独立 `.skill/` 配置和知识库。

---

## 🆕 新项目初始化

首次定位到项目时，检查 `{项目根}/.skill/project.yaml`：创建 `.skill/` + `knowledge-base/` 目录结构，复制模板，询问用户填写配置。已存在则跳过。

---

## ⚠️ 强制约束（最高优先级）

### 1. 前置检查流程

用户触发任何操作时，必须先执行：

```
1. 项目根目录 → 已缓存直接使用 / 未缓存则定位(向上查找 .skill/ 最多3层)
2. 初始化检查 → 仅首次定位时执行
3. 模式识别 → 判断用户意图(A/B)
4. 执行操作 → 先阅读对应 references/*.md 文档
```

> ❌ 禁止重复定位/初始化/整理后自动评审/Excel后自动入库

### 2. 每阶段必读对应文档

| 步骤 | 必读文档 | ⛔ 不读的风险 |
|------|----------|-------------|
| ① 文档整理 | `references/document_consolidate.md` | 锚点格式错误、图片未分确定/不确定、增量识别失效、自动触发评审 |
| ② 需求评审 | `references/requirement_review.md` | 遗漏评审维度、JSON 格式错误、精华库未读取、评审了运维细节 |
| ④ 生成测试点 | `references/testpoint_generate.md` | 测试点格式错误、未去重、缺少处理决策解析、未生成测试点报告 |
| ⑥ 生成用例 | `references/testcase_refine.md` | 步骤编号错误、数据未实例化、步骤与预期不对应、Excel 格式错误 |
| ⑦ 入库知识库 | `references/knowledge_base_archive.md` | 命名不规范、重复入库、未提炼精华、进化日志未更新 |

> ❌ 禁止凭记忆执行 | 禁止跳过阅读 | 禁止假设规则内容

### 3. 层级 Todo 管理

| 层级 | 内容 | 编号 | 状态管理 |
|------|------|------|---------|
| 一级(主流程) | 7步流程(①~⑦) | 0,1,2... | 始终保留，不替换 |
| 二级(子流程) | 当前步骤详细子步骤 | N-1,N-2... | 进入时追加，完成时移除 |

**执行规则**：进入主步骤 N → 第一步追加完整二级 Todo → 逐项执行 → 完成后移除二级，标记一级 completed

> ❌ 禁止先执行操作再追加 Todo | 禁止替换一级 Todo | 禁止省略二级 Todo

### 4. ⛔ 禁止 AI 擅自决策

| 禁止项 | 说明 |
|--------|------|
| 禁止假设已读取 | 不假设前置步骤已完成，必须实际执行每步读取 |
| 禁止简化 Todo | Todo 清单必须完整，不可省略强制检查项 |
| 禁止跳过步骤 | 强制项不可跳过，必须逐项执行并标记状态 |
| 禁止自行判断 | AI 不可自行判断「不重要」「已完成」「无需执行」 |
| 禁止假设状态 | 标记「已完成」前必须实际执行该操作 |
| 禁止修改路径 | 路径字符串原样复制，禁止添加/删除空格符号 |

### 5. ⏱️ 每步完成后强制时间节省反馈（不可跳过）

步骤 ①②④⑥⑦ 完成后，**必须**强制收集用户时间节省反馈，按以下流程执行：

1. **通报完成 + 展示参考时间 + 强制询问**（必做）
   - AI 自动记录 `agent_start_time`（开始执行时）和 `agent_end_time`（完成时）
   - 根据需求复杂度展示参考范围，如"本步骤节省时间约 2~3 小时，是否采纳？"
   - 用户可回复"采纳"或自行输入数值
2. **解析用户回复**
   - "采纳" → 取参考范围的**中间值**（如参考 2~3 小时则取 2.5 小时）
   - "3小时" / "3h" → 直接用，hours=3.0
   - "1天" / "1.2人天" → 按 1 人天=8 小时换算后存储
3. **二次确认**（展示数据等用户确认，不确认不保存）
4. **调用 `record_time_saved.py` 写入**（MySQL/腾讯+JSONL兜底）
5. **确认记录**（告知用户已记录，含 MySQL 同步状态）

> ❌ 禁止跳过时间反馈 | 禁止AI自行估算 | 禁止不确认就保存
> 📖 详细规则见 `references/time_tracking.md`

### 6. 📊 时间节省分析报告（用户触发）

用户说"查看时间统计"/"时间节省分析"/"效能统计"等指令时，调用 `generate_time_analytics.py` 生成 HTML 报告：
- 测试人员 → 个人报告（`--person "{姓名}" --mysql`）
- 管理员 → 业务线报告（`--mysql`）
- **必须**生成 HTML 文件 + 提供本地路径 + 展示关键数字

> 禁止编造数据——如果工具/API 未返回数据，返回明确提示，不得生成占位内容。

### 7. 📤 每步产出文件内容必须直接展示在对话中（不可跳过）

每个步骤完成后，**必须**将产出文件的内容直接展示在对话回复中，让用户可以直接审阅，**不只是告诉文件路径**。

| 文件类型 | 展示方式 |
|---------|---------|
| `.md` 文件 | `read` 工具读取全文展示 |
| `.json` 文件 | `read` 工具读取，格式化或表格展示 |
| `.xlsx` 文件 | `read` 工具读取，Markdown 表格摘要 |
| `.xmind` 文件 | 缩进列表展示树形结构 |

**执行规则**：
1. 文件保存后，**立即**使用 `read` 工具读取文件内容
2. 将读取到的内容整理后**直接输出在对话回复中**（不是只调用工具，而是把内容写在回复文本里）
3. 对于大文件（>200 行），展示前 100 行 + 末尾摘要，并提示"完整文件已保存至 {路径}"

> ❌ 禁止只给文件路径而不展示内容 | 禁止用"文件已生成"替代内容展示
> 💡 用户无法直接访问 AI 沙箱中的文件，必须将内容输出到对话中

---

## 📊 产出物清单

| 步骤 | 产出物 |
|------|--------|
| ① | `{目录名}_整理版_v{version}.md` + `source/.整理索引.yaml` + `source/` 归档 + ⏱️ 时间节省记录 + 📤 内容展示 |
| ② | `*_评审报告.md` + `*_评审数据.json` + ⏱️ 时间节省记录 + 📤 内容展示 |
| ④ | `*_测试点.xmind` + `*_测试点.json` + `*_测试点生成报告.md` + ⏱️ 时间节省记录 + 📤 内容展示 |
| ⑤ | `*_测试点.xmind`（用户直接在此文件上评审，覆盖原文件） |
| ⑥ | `*_测试用例.json` → `*_测试用例.xlsx` + `*_测试点_reviewed.json`（仅模式A）+ ⏱️ 时间节省记录 + 📤 内容展示 |
| ⑦ | 知识库 4 个目录更新 + INDEX.md + EVOLUTION_LOG.md + ⏱️ 时间节省记录 + 📤 内容展示 |

---

## 🔗 步骤依赖关系

```
① 文档整理 ──→ ② 需求评审 ──→ ③ 确认 ──→ ④ 生成测试点 ──→ ⑤ 评审XMind
                                                                │
⑦ 入库 ←── ⑥ 生成用例 ←────────────────────────────────────────┘
```

---

## 🎮 用户指令识别

| 用户指令 | AI 判断 | 必读文档 | ⛔ 不读的风险 |
|---------|--------|----------|-------------|
| "整理" / "处理这些文档" | 执行① | `references/document_consolidate.md` | 锚点格式错误、图片未分确定/不确定、自动触发评审、流程图使用 Mermaid 而非步骤+缩进 |
| "评审" / "评审这个需求" | 执行② | `references/requirement_review.md` | 遗漏评审维度、JSON 格式错误、评审了运维细节 |
| "生成测试点" / "转 XMind" | 执行④ | `references/testpoint_generate.md` | 测试点格式错误、未去重、缺少处理决策解析 |
| "生成用例" / "生成 Excel" | 执行⑥ | `references/testcase_refine.md` | 步骤编号错误、数据未实例化、Excel 格式错误 |
| "入库" / "归档" | 执行⑦ | `references/knowledge_base_archive.md` | 命名不规范、重复入库、未提炼精华 |
| "查看时间统计" / "效能统计" | 生成报告 | `references/time_tracking.md` | 未生成 HTML 报告、未提供文件路径 |

---

## 🔧 脚本使用

> 💡 **AI 在对话中按步骤直接调用各脚本**，依赖缺失时 Python 会提示安装命令。

### 单独脚本

```bash
python scripts/convert_to_md.py <文件> [--archive]  # 文档转换
python scripts/parse_xmind.py <xmind> -o <json>     # XMind 解析
python scripts/generate_xmind.py --input <json> --output <xmind>  # 测试点 JSON → XMind
python scripts/refine_testcases.py <json> [参数]    # 用例细化
python scripts/generate_excel.py <json> [参数]      # Excel 生成
python scripts/generate_review_report.py --input <json> --output <md>  # 评审报告
```

> ⚠️ 步骤⑦入库知识库**由 AI 按 `references/knowledge_base_archive.md` 规则手动操作**（复制文件、更新进化日志、提炼精华库），不调用脚本。

### 时间节省追踪脚本（⛔ 每步完成后强制调用）

> ⛔ **强制规则**：步骤 ①②④⑥⑦ 完成后，**必须**按 `references/time_tracking.md` 的完整流程执行：通报完成 → 展示参考时间 → 强制询问 → 解析回复 → 二次确认 → 调用脚本记录 → 确认结果。**不可跳过。**

```bash
# 每步完成后记录时间节省（统一存储为小时，支持二次确认）
python scripts/record_time_saved.py \
  --employee "{员工}" --user-story "{故事}" --user-story-code "{编号}" \
  --step "{步骤}" --step-code "{代码}" \
  --hours {小时数} --biz-line "{业务线}" \
  --agent-start "{开始时间}" --agent-end "{完成时间}" \
  [--remark "{备注}"]

# 也可用人天输入（1人天=8小时）
python scripts/record_time_saved.py \
  --employee "{员工}" --user-story "{故事}" \
  --step "{步骤}" --step-code "{代码}" \
  --person-days {人天数} --biz-line "{业务线}"

# 生成HTML分析报告（从 MySQL 读取）
python scripts/generate_time_analytics.py --biz-line "{业务线}" --mysql
python scripts/generate_time_analytics.py --biz-line "{业务线}" --person "{姓名}" --mysql  # 个人报告
```

> 📖 详细规则（身份验证、参考时间表、解析规则、报告生成、MySQL 初始化）见 `references/time_tracking.md`

---

## ⚙️ 项目配置

**位置**: `{项目根}/.skill/project.yaml` — 必填 `team`(项目组)、`product`(产品名称)、`modulePath`(模块路径)。

---

## 📚 知识库结构

```
knowledge-base/
├── INDEX.md / EVOLUTION_LOG.md    # 索引 / 进化日志(只在⑦入库时读写)
├── patterns/                      # 精华库(参与②④⑥生成，≤300 Token)
├── requirements/                  # 历史需求
├── review-reports/                 # 历史评审
├── tech-solutions/                 # 历史技术方案
└── testcases/                     # 历史测试点/用例
```

---

## 📖 详细文档索引

| 文件 | 内容 |
|------|------|
| `references/document_consolidate.md` | ① 文档整理：12步流程、锚点溯源、图片解析、增量识别 |
| `references/requirement_review.md` | ② 需求评审：13步流程、6维评审、JSON 格式、精华库 |
| `references/testpoint_generate.md` | ④ 测试点生成：10步流程、5大来源、去重合并 |
| `references/testcase_refine.md` | ⑥ 用例细化：10步流程、细化规则、Excel 格式 |
| `references/knowledge_base_archive.md` | ⑦ 入库知识库：12步流程、差异对比、精华提炼 |
| `references/time_tracking.md` | 时间追踪v5：强制反馈+MySQL同步+HTML报告 |

---

## 💡 使用示例

### 示例1：完整流程

```
用户：帮我处理 D:\项目A\2026\Q2\需求目录 下的需求文档

AI：
1. 定位项目 → 执行前置检查 → 创建 7 步 Todo
2. 阅读 references/document_consolidate.md → 执行① → 输出整理版 MD → 📤 read 展示文件内容 → ⏱️强制时间反馈 → 等待用户校验
3. 用户确认 → 阅读 references/requirement_review.md → 执行② → 输出评审报告 → 📤 read 展示文件内容 → ⏱️强制时间反馈
4. 用户确认 → 阅读 references/testpoint_generate.md → 执行④ → 输出 XMind → 📤 展示树形结构 → ⏱️强制时间反馈
5. 用户评审 XMind → 阅读 references/testcase_refine.md → 执行⑥ → 输出 Excel → 📤 read 展示用例表格 → ⏱️强制时间反馈
6. 用户确认入库 → 阅读 references/knowledge_base_archive.md → 执行⑦ → ⏱️强制时间反馈 → 完成
```

### 示例2：单步模式

```
用户：我有评审后的 XMind，帮我生成用例

AI：
1. 定位项目 → 识别模式B（单步执行⑥） → 创建 Todo
2. 阅读 references/testcase_refine.md → 执行⑥ → 输出 Excel → 📤 read 展示用例表格 → ⏱️强制时间反馈
3. 用户确认 → 流程结束 (如需入库请说"入库")
```

---

*版本：v2.9*
*更新日期：2026-08-13*
*更新：新增腾讯文档智能表格API直调（storage_mode=tencent），沙箱环境可直接写入公网API，无需内网通道*
