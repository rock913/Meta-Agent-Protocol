# MAP Architecture — Module Topology

> 地方解剖图：MAP 模块的层级依赖与分发拓扑
> MAP 位于 L0.0 — 高于所有子项目，通过 Git Submodule 分发给订阅者

## 层级定位

```
L0.0: MAP (Meta-Agent-Protocol)    ← 本仓库
      联邦宪法 + 规则 + 模板 + 脚本
      ↓ (git submodule)
L0-L4: Server A / Server B          ← 订阅者（宿主仓库）
      AI_RULES.md  ← setup_map.sh 从模板生成
      .aider.conf.yml
      .importlinter
      CONVENTIONS.md ← 从 sub-project-conventions/ 复制
```

## 模块拓扑

```
┌─────────────────────────────────────────────────┐
│  Layer 0: 宪法层 (Read-Only for Subscribers)     │
│  THE_CODEX.md — 9 法则最高宪法                    │
│  Fan-out: 被所有订阅者 Agent 在启动时读取          │
├─────────────────────────────────────────────────┤
│  Layer 1: 规则库 (Reusable Rules)                 │
│  rules/arch-rules.md    — 架构防污染红线          │
│  rules/agent-loop.md    — 双引擎协作节拍器        │
│  Fan-out: 被 AI_RULES.md 引用，被 CLAUDE.md 内嵌  │
├─────────────────────────────────────────────────┤
│  Layer 2: 模板引擎 (Instantiable Templates)       │
│  templates/AI_RULES.md.template                   │
│  templates/aider.conf.yml.template                │
│  templates/importlinter.ini.template              │
│  Fan-in: setup_map.sh                            │
│  Fan-out: 生成 AI_RULES.md + .aider + .importlinter│
├─────────────────────────────────────────────────┤
│  Layer 3: 自动化工具 (Executable Scripts)         │
│  scripts/setup_map.sh    — 脚手架（模板→实例）     │
│  scripts/heartbeat.sh    — 定时心跳               │
│  Fan-in: templates/                              │
│  Fan-out: 生成文件到宿主仓库根目录                 │
├─────────────────────────────────────────────────┤
│  Layer 4: 参考实现 (Reference Conventions)        │
│  sub-project-conventions/ — 6 套地方法规模板       │
│  Fan-out: 被订阅者复制到 <子项目>/docs/CONVENTIONS.md│
├─────────────────────────────────────────────────┤
│  Layer 5: 自举层 (Self-Hosting) 🆕 v1.1           │
│  docs/           — 分形文献库 (PRD+CONVENTIONS+arch)│
│  ROADMAP.md      — MAP 自身版本演进                │
│  CLAUDE.md       — MAP 开发 AI Agent 行为规范      │
│  tests/          — 模板/脚本/一致性自动化验证       │
│  VERSION + CHANGELOG.md — 版本管理                │
└─────────────────────────────────────────────────┘
```

## 分发拓扑

```
rock913/Meta-Agent-Protocol (GitHub)
        │
        ├──→ Server A: SROS-Workspace-Setup/conventions/ (submodule)
        │        5 子项目，800+ tests
        │
        └──→ Server B: SROS-Workspace-Astro/conventions/ (submodule)
                 天文域，共享 SROS/ARC/Hermes 上游

订阅者升级流程:
  cd conventions && git pull origin main && cd .. && git add conventions
```

## 关键契约

- **9 法则编号不变**：MAJOR 版本递增，提供迁移指南
- **占位符名称不变**：`{{PLACEHOLDER}}` 名称 = 公共 API
- **`setup_map.sh` 文件路径不变**：生成的目标文件路径是 MAP 的 Interface Contract
- **POSIX 兼容**：scripts/ 零外部依赖
