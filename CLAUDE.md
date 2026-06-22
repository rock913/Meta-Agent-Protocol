# CLAUDE.md — Meta-Agent-Protocol (MAP)

> MAP (L0.0 元宪法) 独立项目的 AI Agent 行为规范。
> MAP 是 Server A (脑影像) 和 Server B (天文) 的共享宪法仓库，所有变更需考虑向下兼容性。
> 联邦宪法：`THE_CODEX.md`（9 法则，本文件也受其约束）。

## 1. 操作边界 (Modification Boundary)

| 路径 | 允许操作 | 约束 |
|------|:--:|------|
| `THE_CODEX.md` | ⚠️ 谨慎修改 | 9 法则可新增不可删除；法则编号永不改变；修改需 MAJOR 版本号递增 |
| `rules/` | ✅ 读/写 | 追加新规则 = MINOR；修改已有规则 = MAJOR |
| `templates/` | ✅ 读/写 | 追加占位符 = MINOR；修改已有结构 = 需评估下游影响 |
| `sub-project-conventions/` | ✅ 读/写 | 与对应子项目实际 CONVENTIONS.md 保持同步 |
| `scripts/` | ✅ 读/写 | 修改后必须通过 `tests/test_scripts.sh` |
| `docs/` | ✅ 读/写 | 分形文献库标准骨架 |
| `CLAUDE.md` | ✅ 读/写 | 本文件 |
| `ROADMAP.md` | ✅ 读/写 | 版本演进追踪 |
| `INTEGRATION.md` | ✅ 读/写 | 接入指引 — 修改后通知所有订阅者 |
| `README.md` | ✅ 读/写 | 项目首页 |

## 2. TDD 门禁

```
修改模板 → 运行 python3 -m pytest tests/test_templates.py
修改脚本 → 运行 bash tests/test_scripts.sh
修改 THE_CODEX → 运行 python3 -m pytest tests/test_cross_consistency.py
发布前   → 运行全部 3 个测试
```

## 3. 版本号语义 (Semantic Versioning for MAP)

| 级别 | 触发条件 | 示例 |
|:--:|------|------|
| **MAJOR** | THE_CODEX 法则增删改；法则编号改变 | v1.x → v2.0 |
| **MINOR** | 新 rules/；新 templates/；新 scripts/；新 sub-project-conventions/ | v1.1 → v1.2 |
| **PATCH** | 文档修正；占位符说明改进；typo fix | v1.1.0 → v1.1.1 |

## 4. 向下兼容铁律

- **9 法则可新增不可删除**（新增 = MINOR）
- **法则编号永不改变**（改变 = MAJOR + 迁移指南）
- **templates/ 占位符可新增不可删除**（删除 = MAJOR）
- **子项目 CONVENTIONS 模板变更需同步通知所有订阅者**
- **`setup_map.sh` 生成的文件路径不可改变**

## 5. 发布流程

```
1. 修改 → TDD 门禁通过 → git commit
2. 更新 CHANGELOG.md（按版本号分段）
3. 更新 VERSION 文件
4. git tag vX.Y.Z
5. git push origin main --tags
6. 通知订阅者：
   - Server A: cd conventions && git pull origin main
   - Server B: (同上)
```

## 6. 关键文件索引

| 文件 | 用途 |
|------|------|
| `THE_CODEX.md` | 联邦宪法 — 9 法则全文 |
| `INTEGRATION.md` | 宿主仓库接入指引 (Greenfield + Migration) |
| `README.md` | 项目首页 — 定位/Quick Start/目录结构 |
| `CHANGELOG.md` | 版本演进记录 |
| `VERSION` | 当前语义化版本号 |
| `ROADMAP.md` | 里程碑与进度追踪 |
| `rules/arch-rules.md` | 架构防污染红线 + Contract-First |
| `rules/agent-loop.md` | Claude Code → Aider 微循环节拍器 |
| `templates/` | AI_RULES / aider / importlinter 配置模板 |
| `scripts/setup_map.sh` | 一键脚手架脚本 |
| `scripts/heartbeat.sh` | 定时心跳 (git status + test) |
| `sub-project-conventions/` | 6 套子项目地方法规模板 |
| `tests/` | 模板/脚本/一致性自动化验证 |
