# Meta-Agent-Protocol (MAP)

> **元智能体协议** — 为多智能体（Multi-Agent）与联邦单体仓库（Federated Monorepo）设计的开源行为规范与工作流套件。
>
> 如果 [MCP (Model Context Protocol)](https://modelcontextprotocol.io) 解决了 AI 工具调用的"硬件接口"，那么 **MAP 解决的是 AI 智能体协作行为的"软件协议"**。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](./CHANGELOG.md)

---

## 一句话

你的 AI 编码助手需要一个入职手册。MAP 就是那个手册——一套经过大规模联邦仓库实战验证的 AI Agent 行为宪法、TDD 循环规范和安全护栏。

## 问题 (Why MAP?)

使用 Claude Code、Aider、Cursor 等 AI 编码工具的团队都会遇到同样的痛点：

- **AI 幻觉越界**：Agent 修改了不该动的文件，跨系统乱 import
- **Prompt 碎片化**：每个人的 system prompt 都是散装的，没有系统级约束
- **TDD 形同虚设**：Agent 跳过测试直接改代码，"测试下次补" = 永远不会补
- **多仓库协作失控**：5 个子项目，10 个 Agent，没有统一的契约通信协议

MAP 将这些问题的解决方案打包为**一套可版本化、可迁移、可定制的规则 + 脚本体系**。

## 快速开始 (Quick Start)

```bash
# 1. 在你的 Meta 仓库中添加 MAP 作为 submodule
git submodule add https://github.com/rock913/Meta-Agent-Protocol.git conventions

# 2. 运行脚手架脚本
bash conventions/scripts/setup_map.sh

# 3. 编辑生成的占位符，填入你的项目信息
#   - AI_RULES.md 中的 {{PROJECT_NAME}}
#   - .aider.conf.yml 中的 PRD 路径映射
#   - .importlinter 中的 root_packages

# 4. 提交
git add -A && git commit -m "feat: bootstrap MAP conventions v1.0.0"
```

## 目录结构

```
Meta-Agent-Protocol/
├── README.md                       # 本文件
├── CHANGELOG.md                    # 语义化版本演进记录
├── LICENSE                         # MIT
├── THE_CODEX.md                    # 【核心】最高指导原则 — 9 法则
│
├── rules/                          # 分场景宪法
│   ├── arch-rules.md               # 架构级防污染红线 + Contract-First
│   └── agent-loop.md               # 双引擎微循环协作规范
│
├── templates/                      # 即插即用的配置模板
│   ├── AI_RULES.md.template        # 全局 Agent 行为宪法（含占位符）
│   ├── aider.conf.yml.template     # Aider + DeepSeek 全局配置模板
│   └── importlinter.ini.template   # 联邦架构物理隔离配置
│
├── scripts/                        # 自动化工具链
│   ├── setup_map.sh                # MAP 装载脚手架
│   └── heartbeat.sh                # Loop Engineering 自动化心跳
│
└── sub-project-conventions/        # 子项目 CONVENTIONS.md 参考模板
    ├── SROS-CONVENTIONS.md
    ├── ARC-Engine-CONVENTIONS.md
    ├── GraphMRI-Lite-CONVENTIONS.md
    ├── Hermes-Workflows-CONVENTIONS.md
    ├── AgenticOps-CONVENTIONS.md
    └── SXMU_MDD_Twin-CONVENTIONS.md
```

## 核心概念

### THE_CODEX → rules/ → templates/

```
THE_CODEX.md          ← 人类阅读的宪法原则（不可变）
    ↓
rules/                ← 场景化的规范文本（通用，直接复用）
    ↓
templates/            ← 参数化的配置文件（含 {{PLACEHOLDER}}，按需定制）
```

### 级联法规封地 (Cascading Conventions)

AI Agent 启动时按以下优先级加载规则：

```
1. THE_CODEX.md         ← 全局宪法 (MAP 提供)
2. AI_RULES.md          ← 联邦法律 (setup_map.sh 生成)
3. CONVENTIONS.md       ← 地方法规 (每个子项目自行维护)
```

## 适用场景

- ✅ 联邦单体仓库（5+ 子项目，多 Agent 协同）
- ✅ AI4S / 跨学科科研计算平台
- ✅ 使用 Aider + DeepSeek / Claude Code 双引擎的开发团队
- ✅ 需要 import-linter 物理隔离 + MCP 契约通信的微服务架构
- ⚠️ 单项目小仓库也可受益于 TDD 门禁和 Prompt 规范

## 与 MCP 的关系

| | MCP (Model Context Protocol) | MAP (Meta-Agent-Protocol) |
|:--|:--|:--|
| **解决什么** | AI 如何调用外部工具 | AI 如何规范地工作 |
| **层面** | 接口层 (Interface) | 行为层 (Behavior) |
| **形式** | JSON-RPC 协议 | Markdown 规则 + Shell 脚本 |
| **类比** | USB 接口标准 | 员工手册 + 操作流程 |

## 社区

- **Issues / PRs**: [github.com/rock913/Meta-Agent-Protocol](https://github.com/rock913/Meta-Agent-Protocol)
- **License**: MIT — 最大化社区采用率

---

> *"Don't Guess, Copy. Contract First, Code Second. Test is the Executable Contract."*
> — MAP THE_CODEX, Law II & Law VIII
