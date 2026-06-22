# MAP ROADMAP

> Meta-Agent-Protocol 版本演进与进度追踪
> 版本：v1.1.0-dev | 2026-06-22

## 里程碑

| 版本 | 目标 | 状态 | 交付日期 |
|------|------|:----:|----------|
| **v1.0.0** | 核心宪法 + 规则 + 模板 + 脚本 — 初始发布 | ✅ | 2026-06-16 |
| **v1.0.1** | INTEGRATION.md 接入指引 + 脚本路径修正 | ✅ | 2026-06-17 |
| **v1.1.0** | Self-Hosting — 分形骨架 + CLAUDE.md + ROADMAP + tests | 🔶 进行中 | 2026-06-22 |
| **v1.2.0** | 模板引擎增强 + Server B 反馈整合 | ❌ | 待定 |
| **v2.0.0** | MAP as Protocol Standard — JSON Schema + CI checker + 多语言 | ❌ | 远期 |

---

## v1.0.x — Foundation ✅

| M# | 交付物 |
|----|--------|
| M1 | `THE_CODEX.md` — 9 法则联邦宪法 (219 lines) |
| M2 | `rules/arch-rules.md` — 架构防污染红线 + Contract-First + 环境约束 + 子项目文档规范 |
| M3 | `rules/agent-loop.md` — 双引擎微循环节拍器 (L0-L3 任务粒度) |
| M4 | `templates/AI_RULES.md.template` — 全局 Agent 行为宪法模板 (5 占位符) |
| M5 | `templates/aider.conf.yml.template` — Aider + DeepSeek 配置模板 (4 占位符) |
| M6 | `templates/importlinter.ini.template` — 联邦架构物理隔离配置 (4 占位符) |
| M7 | `scripts/setup_map.sh` — 一键脚手架 (4 文件生成 + SKIP 逻辑) |
| M8 | `scripts/heartbeat.sh` — 定时心跳 (git status + test 检查) |
| M9 | `sub-project-conventions/` — 6 套子项目地方法规模板 |
| M10 | `INTEGRATION.md` — 宿主仓库接入指引 (v1.0.1, 256 lines) |
| M11 | `README.md` — 项目首页 + 定位说明 + Quick Start |

---

## v1.1.0 — Self-Hosting 🔶 (Current)

> MAP 自身成为一等子项目，具备完整的开发闭环。

| M# | 交付物 | 状态 |
|----|--------|:--:|
| M12 | `CLAUDE.md` — MAP 开发 AI Agent 行为规范 | ✅ |
| M13 | `ROADMAP.md` — 本文件 | ✅ |
| M14 | `VERSION` — 语义化版本号文件 | 📋 |
| M15 | `docs/PRD.md` — MAP 产品需求文档 | 📋 |
| M16 | `docs/CONVENTIONS.md` — MAP 自身开发规范 | 📋 |
| M17 | `docs/architecture.md` — MAP 模块拓扑图 | 📋 |
| M18 | `docs/proposals/` — 提案着陆区 (pending + consumed) | ✅ |
| M19 | `tests/test_templates.py` — 模板占位符完整性验证 | 📋 |
| M20 | `tests/test_scripts.sh` — 脚本语法检查 | 📋 |
| M21 | `tests/test_cross_consistency.py` — THE_CODEX ↔ rules ↔ templates 一致性 | 📋 |

---

## v1.2.0 — 模板引擎增强 ❌

| M# | 交付物 |
|----|--------|
| M22 | `setup_map.sh --validate` — 模板渲染后自动检查未替换占位符 |
| M23 | Server B (天文域) 反馈整合 — 通用性改进 |
| M24 | `sub-project-conventions/` 新增 OneAstronomy 模板 |
| M25 | `INTEGRATION.md` 增加 Troubleshooting 章节 |

---

## v2.0.0 — MAP as Protocol Standard ❌

| M# | 交付物 |
|----|--------|
| M26 | JSON Schema for MAP rules — 机器可消费的规则定义 |
| M27 | `map-compliance-checker` CI Action — 自动检查仓库是否遵循 MAP |
| M28 | 多语言模板 (EN/CN) — 国际化支持 |
| M29 | MAP 官网 / 文档站 (GitHub Pages) |
| M30 | 社区治理模型 (GOVERNANCE.md + CONTRIBUTING.md) |

---

## 风险

| 风险 | 缓解 |
|------|------|
| Server A/B 订阅者滞后升级 | `heartbeat.sh` 定时提醒 + INTEGRATION.md 清晰升级步骤 |
| THE_CODEX 法则变更导致下游行为断裂 | MAJOR 版本 + 迁移指南 + 至少 30 天过渡期 |
| 子项目 CONVENTIONS 模板与实际脱节 | 每次子项目 CONVENTIONS 更新时反向同步至 MAP |
| MAP repo 修改后 submodule 指针未更新 | Server A/B CLAUDE.md 中强调 `cd conventions && git pull` |
