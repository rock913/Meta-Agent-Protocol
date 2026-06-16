# Arch-Rules — 架构级防污染红线

> 版本：v1.0.0 | 2026-06-16
> 本文件定义联邦仓库中 AI Agent 必须遵守的架构级约束。
> 与 THE_CODEX.md 配套使用 — THE_CODEX 定义"如何思考"，本文件定义"如何构建"。

---

## 1. 依赖隔离红线 (Import Firewall)

### 核心原则

**独立子项目之间绝对禁止直接 import。跨系统通信必须通过 MCP (Model Context Protocol) 或 CLI `--raw` JSON 接口。**

### 被拦截的行为

- ❌ `from <project_a>.core import Model`（在 Project B 中）
- ❌ `import <project_a>`（在 Project B 中）
- ❌ 通过 `sys.path.append("../project_a")` 绕过
- ✅ `<project_b>` 通过 MCP Client 调用 `<project_a>` 暴露的工具
- ✅ `<project_b>` 通过 `subprocess.run(["project_a_cli", "--raw", json_input])` 调用

### 物理级城墙：import-linter

使用 [import-linter](https://github.com/seddonym/import-linter) 在 CI 层面强制拦截跨系统 import：

```ini
[importlinter]
root_packages =
    <your_package_1>
    <your_package_2>
    ...

[importlinter:contract:independence]
name = Core systems must be independently deployable
type = independence
modules =
    <your_package_1>
    <your_package_2>
    ...

[importlinter:contract:layers]
name = Layer discipline — cross-system communication via MCP/CLI only
type = layers
layers =
    <your_package_1>
    <your_package_2>
    ...
```

**CI 集成**：
```bash
lint-arch   # 单独检查架构边界（应在全局回归前运行）
test-all    # = lint-arch + <每个子项目的测试套件>
```

### 为什么需要物理级城墙

| 没有城墙 | 有城墙 |
|---------|--------|
| AI Agent 可能幻觉式 import | CI 自动拦截，红灯即停 |
| 依赖关系随时间腐烂 | 每次 commit 自动检查 |
| 新人不知道边界在哪 | 配置文件即文档 |

---

## 2. Contract-First Development (契约优先开发)

> 来源：Fable 5 架构哲学 — 从流程工程到契约工程

### 三层契约模型

```
Layer 1: Interface Contract (接口契约)
    └── 每个模块的输入/输出 JSON Schema + ErrorCode 枚举

Layer 2: Behavior Contract (行为契约)
    └── pytest 测试用例 = 可执行的行为契约

Layer 3: Cross-System Contract (跨系统契约)
    └── contracts/ 目录中的 JSON/DDL 快照 + CI 契约回归测试
```

### 核心铁律

1. **Interface First, Implementation Second**
   任何新功能的第一步是定义接口契约（JSON Schema / Pydantic model / ErrorCode enum），第二步才是实现。

2. **Test as Executable Contract**
   pytest 测试用例是行为契约的可执行形式。一个没有对应 failing test 的功能变更 = 无效交付。

3. **Contract over SOP**
   AI Agent 的行为规范应以"给定 X，期望 Y"的契约形式表达，而非"第一步做 A，第二步做 B"的 SOP 形式。步骤 >3 时，拆分为多个独立契约。

### Prompt 编写契约

任何给 AI Agent 的指令，必须包含以下三要素：

| 要素 | 含义 | 示例 |
|------|------|------|
| **Input Schema** | 输入的数据结构和约束 | `{bids_dir: string, nthreads: int (1-16)}` |
| **Output Schema** | 期望的输出格式 | `{job_id: UUID, status: "submitted"}` |
| **Error Contract** | 失败时的错误码和行为 | `磁盘不足 → ERR_RESOURCE_EXHAUSTED` |

**禁止**：在 Prompt 中写大于 3 步的 SOP 流程。

### 跨系统接口契约版本化

跨系统接口（MCP tool schema、共享 DDL、CLI `--raw` JSON 格式）的变更必须：

1. 更新 `contracts/` 目录中的契约快照
2. 在 commit message 中标注 `cross-system: <affected projects>`
3. 运行全局契约回归测试
4. 通知所有消费方项目

---

## 3. 环境约束

### 交互式终端 & 非交互式环境

- 严禁使用阻塞性交互命令 (`vim`, `nano`, `less`)
- 遇到询问默认加 `-y` 或等价参数
- 非交互式桥接环境（如飞书 Bot）下所有确认默认通过

### 静默优先

- 确定性的依赖安装、Linter 执行、文件覆盖直接执行，不索要确认
- 尽量减少向用户索要权限

---

## 4. 子项目 CLAUDE.md / CONVENTIONS.md 必须包含的章节

每个子项目的 AI Agent 配置文件应包含：

1. **Hard Guardrails (Red Lines)**：不可违反的硬约束列表
2. **Contract-First 章节**：本项目的三层契约（Interface / Behavior / Cross-System）
3. **关键文件索引**：表格（文件路径 → 用途）
4. **架构概览**：ASCII 目录树 + 关键模块说明
5. **常用命令**：开发/测试/构建命令
6. **开发流程**：TDD / Read PRD / Reference impl / Verify 闭环
7. **常见反模式 (Anti-Patterns Learned)**：记录重复性 Bug 模式

---

## 附录：快速检查清单

- [ ] 每个子项目有独立的 Python/JS 包名
- [ ] import-linter 配置已添加并 CI 集成
- [ ] contracts/ 目录中每个跨系统接口有契约快照
- [ ] 每个核心模块 ≥ 1 个 pytest
- [ ] 所有 Prompt 包含 Input/Output/Error 三要素
- [ ] 跨系统 import 被 import-linter 拦截（验证：在 Project A 中 `import Project_B` → CI 红灯）
