# THE_CODEX.md — 智能体行为最高宪法

> 版本：v1.0.0 | 2026-06-16
> 本文件是 Meta-Agent-Protocol (MAP) 的核心宪法。
> 所有引入 MAP 的宿主仓库中运行的 AI Agent（Claude Code、Aider、Cursor 等）必须遵守以下 9 条法则。
> 这 9 条法则经过 AI4S 联邦仓库（5 子项目、800+ tests）实战验证。

---

## 法则一：人格切换 (Persona Shifting)

**AI Agent 在不同上下文中必须切换语言风格：**

| 上下文 | 人格 | 语言风格 |
|--------|:--:|------|
| 架构文档 / 进度聚合 / PRD 提案 | 架构师 | 允许隐喻和游戏化表达 |
| 源代码（`.py` / `.ts` / `.vue`） | IEEE 工程师 | **绝对严谨**，禁止游戏化词汇、emoji 修饰、拟人化表达 |
| Git Commit Message | IEEE 工程师 | **绝对无菌**，Conventional Commits 格式 |
| 测试代码 / 错误日志 | IEEE 工程师 | 保留原汁原味的堆栈跟踪，禁止 paraphrase |

**违规示例**：
- ❌ 在源代码注释中写 "反应堆核心熔毁"
- ❌ 在 Git commit 中写 "🧪 合成车间升级完毕"
- ✅ `feat(gateway): add MCP-to-OpenAI adapter`

---

## 法则二：TDD 门禁 (The TDD Gate)

**对任何源代码文件（`.py` / `.ts` / `.vue` / `.rs` / `.go`）的修改，必须通过 TDD 门禁：**

```
1. 修改前：确认存在对应的 failing test（或先写 test）
2. 修改代码
3. 立即运行该模块的测试套件
4. 红灯 → 分析失败原因 → 修正 → 回到步骤 3
5. 绿灯 → 声明完成
```

**豁免**：纯文档修改（`.md` 文件）、配置修改（`.yaml` / `.json` / `.sql` / `.toml`）不需要 TDD 门禁。

---

## 法则三：红线禁区 (No-Go Zones)

**以下文件类型绝对禁止修改（除非用户明确授权）：**

- 任何顶层的 `CLAUDE.md`（AI Agent 自身的行为规范定义）
- 任何 `ROADMAP.md`（项目进度追踪，只能由架构师层更新）
- 任何 `GUARDRAILS.md` 或 `CONVENTIONS.md`（规则定义文件）
- 任何 `contracts/` 目录下的快照文件（跨系统接口契约，变更需对应子项目已实现）

**对 `contracts/` 的修改必须**：确认对应子项目已实现该契约 → 运行全局回归测试 → 标注 cross-system commit。

---

## 法则四：跨系统修改申报 (Cross-System Change Declaration)

**如果一次修改同时涉及两个或更多独立子项目，必须：**

1. 在 commit message 中标注 `cross-system: <affected projects>`
2. 在 PR body 中说明跨系统影响范围
3. 运行全局回归测试套件

**示例**：
```
feat(sros,graphmri): add submit_job MCP tool

cross-system: SROS + GraphMRI-Lite
- SROS: new MCP tool sros_submit_job in gateway
- GraphMRI: cli.py parses new tool call format
- Contract: updated contracts/mcp/sros_tools.json
```

---

## 法则五：Git 工作流 (SLAIB) + Push 频率策略

### SLAIB 短期分支流
1. 任何修改前 `git checkout -b <type>/<desc>`
2. 修改完成后 push 分支
3. 通过 `gh pr create --fill` 发起 PR
4. **严禁**直接 push main（main 应写保护）
5. PR Merge 后 `git fetch --prune` 清理
6. **严禁** `git push --force` 任何分支

**分支类型前缀**：`feat/` (功能), `fix/` (修复), `refactor/` (重构), `docs/` (文档)

### Push 频率策略

**每完成一个独立任务后，必须立即 push，不得让代码在本地堆积：**

| 时机 | 操作 |
|------|------|
| 任务完成 (tests 绿灯, ROADMAP ✅) | `git commit` + `git push origin <branch>` |
| 每完成 1-3 个相关任务 | `gh pr create --fill` |
| Session 结束前 | push 所有未推送分支 |
| 跨天任务 | 每日结束前至少 push 一次 |

**禁止**：任务完成后不 push，让代码在本地堆积（"等一下一起 push" = 永远不会 push）。

---

## 法则六：全局测试编排 + PRD 同步铁律

### 全局回归
修改跨系统接口（contracts/、MCP schema、共享 DDL）后，必须运行全局回归，包括架构边界检查（import-linter）。

### PRD 同步铁律

**任何功能开发完成后，必须同时更新两个文件：**

| 更新目标 | 更新内容 |
|---------|---------|
| **ROADMAP.md** | 对应任务 ID → ✅ |
| **主 PRD** | 新增/修改本功能对应的功能章节 |

⚠️ **禁止只改 ROADMAP 不改 PRD**。"下次再更新 PRD" = 永远不会更新 = PRD 变成僵尸文档。

---

## 法则七：级联法规封地 (Cascading Conventions)

**AI Agent 在不同项目目录下必须遵守不同的"地方法规"：**

| 规则文件 | 层级 | 何时读取 |
|---------|:--:|---------|
| `THE_CODEX.md` (本文件) | 联邦宪法 | 启动时 |
| `AI_RULES.md` | 宿主仓库行为法 | 启动时 |
| `<子项目>/CONVENTIONS.md` | 地方法规 | 修改该子项目文件前 |

**Aider 会自动读取目标文件所在目录及上级目录的 `CONVENTIONS.md`**。Claude Code 用户需手动 `/read`。

---

## 法则八：Contract-First Prompting (契约优先指令)

**在给 AI Agent 下达跨系统指令时，使用"契约握手指令"，而非"端到端模糊指令"。**

### ❌ 禁止
```
"给系统 A 和系统 B 加上联调功能，你看着改。"
```

### ✅ 正确
```
"跨系统开发任务：<简短描述>。

Step 1 (<系统A> — 契约提供方)：
查阅 <系统A>/CONVENTIONS.md。
更新接口契约（JSON Schema），加入 <新字段>。
完成后运行 <系统A 测试命令>。

Step 2 (<系统B> — 契约消费方)：
根据 Step 1 确定的 Schema，在 <系统B> 中实现调用。
禁止跨系统 import，使用 MCP/CLI 接口。
完成后运行 <系统B 测试命令>。

Step 3 (全局联调)：
运行全局回归。如遇 lint-arch 报错 → 自行回退并改用 MCP/CLI 接口。"
```

### 契约指令三要素

| 要素 | 含义 | 示例 |
|------|------|------|
| **领域声明** | 明确当前步骤的目标项目 | "Step 1 (SROS — 契约提供方)" |
| **契约定义** | 该步骤的输入/输出 Schema | `{age_range: {min: int, max: int}}` |
| **验收命令** | 该步骤完成后运行的测试 | "运行 make test-sros" |

---

## 法则九：微循环节拍器 (Micro-loop Metronome)

> 适用于：Claude Code（架构师）唤醒 Aider（执行者）执行编码任务时

### 核心原则

**架构师是节拍器，执行者是执行器。架构师不能把 7 个步骤一次性甩给执行者。**

### 执行规则

1. **原子化拆解**：把任务拆成 L0-L2 级别的小步。一次 Aider 调用 = 一个文件（默认 L1）
2. **Task 文件**：每次调用前生成 task 描述文件，包含 Context、Files、Contract、Do NOT
3. **架构师跑测试**：Aider 退出后，由 Claude Code 运行 pylint/pytest。Aider 不跑测试
4. **纠错循环**：红灯 → 架构师读报错 → 更新 task 文件 → 重唤 Aider → 直到绿灯
5. **文件限定**：指定 Aider 可以修改的文件列表，防止越界修改
6. **超时控制**：执行超过 2 分钟无响应 → 停止进程 → 检查日志 → 拆分更小步骤

### 任务粒度控制

| 级别 | 范围 | 适用场景 |
|:--:|------|------|
| L0 | 单个函数 | Bug fix |
| **L1 (默认)** | **单个文件** | **新模块** |
| L2 | 2-3 相关文件 | 模块 + 测试 |
| L3 | 跨目录 | 后端 + 前端（必须拆分） |

**铁律**：默认 L1。一次 Aider 调用 = 一个文件。绝不超过 L2。

---

> ⚠️ 违反以上任何法则的修改，在 PR Review 时将被拒绝。

---

## 附录：9 法则速查卡

| 法则 | 一句话 | 违反后果 |
|:--:|------|------|
| 一 | 代码注释 ≠ RPG 剧本 | PR Review 拒绝 |
| 二 | 没测试 = 没功能 | 不允许合并 |
| 三 | 红线文件碰不得 | 回退修改 |
| 四 | 跨系统改代码要申报 | CI 全局回归拦截 |
| 五 | 做完就 push，别堆积 | 分叉风险 |
| 六 | 改代码 ≠ 改 PRD+ROADMAP | PRD 僵尸化 |
| 七 | 入乡随俗读 CONVENTIONS | 架构破坏 |
| 八 | 模糊指令是毒药 | 越界 import |
| 九 | 一次只做一件事 | TDD 循环卡死 |
