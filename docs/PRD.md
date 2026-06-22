# MAP PRD — Meta-Agent-Protocol Product Requirements

> 版本：v1.1.0-dev | 2026-06-22
> 定位：多智能体联邦仓库的行为协议标准 — AI Agent 的"入职手册"

## 1. 产品定位

MAP 解决的是 AI 编码助手（Claude Code、Aider、Cursor 等）在**联邦单体仓库**中的协作行为规范问题：

| MCP 解决 | MAP 解决 |
|---------|---------|
| AI 如何调用外部工具（接口层） | AI 如何规范地工作（行为层） |
| JSON-RPC 协议 | Markdown 规则 + Shell 脚本 + CI 配置 |

## 2. 核心能力

### 2.1 联邦宪法 (THE_CODEX)

9 条经过大规模联邦仓库（5 子项目，800+ tests）实战验证的最高法则：
1. 人格切换 — 代码注释与架构文档的语言隔离
2. TDD 门禁 — 无 failing test = 无效修改
3. 红线禁区 — 架构师专属文件列表
4. 跨系统修改申报 — 多子项目变更声明
5. Git 工作流 (SLAIB) + Push 频率策略
6. 全局测试编排 + PRD 同步铁律
7. 级联法规封地 — 宪法→联邦法→地方法
8. Contract-First Prompting — 契约握手指令
9. 微循环节拍器 — 架构师是节拍器，执行器是执行器

### 2.2 规则库 (rules/)

- **arch-rules.md**：架构级防污染红线 — import-linter 物理城墙、三层契约模型、环境约束、子项目文档规范
- **agent-loop.md**：双引擎微循环协作规范 — L0-L3 任务粒度、Task 文件格式、超时控制

### 2.3 模板引擎 (templates/)

- **AI_RULES.md.template**：5 占位符 → 生成实例化后的 Agent 行为宪法
- **aider.conf.yml.template**：4 占位符 → 生成 Aider + DeepSeek 配置
- **importlinter.ini.template**：4 占位符 → 生成跨系统 import 防火墙

### 2.4 自动化工具链 (scripts/)

- **setup_map.sh**：一键脚手架 — 从模板生成 AI_RULES.md + .aider.conf.yml + .importlinter + delegate_to_aider.sh
- **heartbeat.sh**：定时心跳 — git status + test 检查，适用于 cron

### 2.5 子项目地方法规模板 (sub-project-conventions/)

6 套经过实战验证的子项目 CONVENTIONS.md 参考模板，覆盖 SROS / ARC / GraphMRI-Lite / Hermes / AgenticOps / SXMU_MDD_Twin。

## 3. 验收标准

- [ ] 所有模板占位符可被 `setup_map.sh` 正确替换
- [ ] AI_RULES.md 的 9 条法则与 THE_CODEX 一一对应
- [ ] importlinter 模板语法有效
- [ ] 脚本通过 `bash -n` 语法检查
- [ ] CHANGELOG.md 记录每次版本变更
- [ ] INTEGRATION.md 覆盖全新安装和迁移两种路径
