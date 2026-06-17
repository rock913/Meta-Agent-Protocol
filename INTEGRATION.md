# MAP Integration Guide — 宿主仓库接入指引

> 版本：v1.0.1 | 2026-06-17
> 适用对象：任何想要引入 Meta-Agent-Protocol 的 AI 辅助开发仓库

---

## 快速判断：你需要哪种路径？

| 你的仓库现状 | 走哪条路径 |
|-------------|:--:|
| 全新仓库，从未有过 AI Agent 规范 | [**路径 A：全新安装**](#路径-a全新安装-greenfield) |
| 已有嵌入的 `conventions/` 或类似 AI 规范目录（如从旧 AI4S 同步而来） | [**路径 B：迁移升级**](#路径-b迁移升级-migration) |

---

## 路径 A：全新安装 (Greenfield)

### A1. 添加 MAP submodule

```bash
cd /path/to/your/repo
git submodule add https://github.com/rock913/Meta-Agent-Protocol.git conventions
git commit -m "feat: add MAP (Meta-Agent-Protocol) as conventions/ submodule"
```

> ⚠️ 如果你偏好 SSH：`git@github.com:rock913/Meta-Agent-Protocol.git`

### A2. 运行脚手架

```bash
bash conventions/scripts/setup_map.sh
```

这会自动生成 4 个文件（如果已存在则 SKIP）：

| 生成的文件 | 用途 |
|-----------|------|
| `AI_RULES.md` | 全局 Agent 行为宪法（9 法则） |
| `.aider.conf.yml` | Aider / 执行引擎全局配置 |
| `.importlinter` | 跨系统 import 物理防火墙 |
| `delegate_to_aider.sh` | 架构师 → 执行引擎委派桥接 |

### A3. 编辑占位符

**所有生成的文件都包含 `{{PLACEHOLDER}}` 标记**。用编辑器搜索 `{{` 并逐一替换。

#### AI_RULES.md 占位符

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{TEST_COMMANDS}}` | 每个子项目的 pytest 命令 | `cd ProjectA && python3 -m pytest tests/ -v` |
| `{{REDLINE_EXTRA}}` | 额外的红线文件（没有则删除此占位符） | `ProjectA/CONVENTIONS.md` |
| `{{TEST_TARGETS}}` | make 全局回归 targets | `test-project-a test-project-b` |
| `{{PRD_PATH_MAP}}` | 子项目 → 主 PRD 路径映射 | `ProjectA: docs/PRD.md` |
| `{{LOCAL_CONVENTIONS_SUMMARY}}` | 各子项目 CONVENTIONS 一句话摘要 | `ProjectA: 禁用 Celery, Vue 3 Composition API` |

#### .aider.conf.yml 占位符

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{WORKSPACE_NAME}}` | 你的工作空间名称 | `MyProject Workspace` |
| `{{PRD_DOC_MAP}}` | 子项目 PRD 文档路径列表 | `- ProjectA: docs/PRD.md` |
| `{{ROADMAP_PATH_MAP}}` | 子项目 ROADMAP 路径列表 | `- ProjectA: ProjectA/ROADMAP.md` |
| `{{PRD_PATH_MAP}}` | 主 PRD 路径映射（与 AI_RULES.md 一致） | `- ProjectA: docs/PRD.md` |

#### .importlinter 占位符

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{PACKAGE_LIST}}` | 所有独立 Python 包名（每行一个） | `project_a` |
| `{{MODULE_LIST}}` | 同上（模块列表） | `project_a` |
| `{{IGNORE_IMPORTS}}` | 自引用规则 | `project_a -> project_a.*` |
| `{{LAYER_LIST}}` | 层列表 | `project_a` |

> 📋 **参考实现**：查看 MAP 的 `sub-project-conventions/` 目录获取 CONVENTIONS.md 模板，查看 `templates/` 目录获取完整模板。

### A4. 创建域特定文件

```bash
# 全局坐标系（必需 — AI Agent 启动时读取）
touch WORKSPACE_MAP.md

# 目录结构约定（建议 — 记录你的项目拓扑）
mkdir -p meta-docs
touch meta-docs/workspace-structure.md
```

`WORKSPACE_MAP.md` 最少应包含：
```markdown
# WORKSPACE_MAP — 全局项目拓扑

## 子项目列表
- `<ProjectA>`: <一句话角色> (`<path>/`)
- `<ProjectB>`: <一句话角色> (`<path>/`)

## 共享基础设施
- <列出共享的中间件/DB/MQ>

## 依赖隔离规则
- 跨系统通信: MCP / CLI --raw JSON
- import-linter 在 CI 中强制拦截跨系统 import
```

### A5. 创建 Makefile（如尚未存在）

```makefile
.PHONY: test-all lint-arch

lint-arch:
	python3 -m importlinter lint

test-<project-a>:
	cd <ProjectA> && python3 -m pytest tests/ -v

test-all: lint-arch test-<project-a> test-<project-b>
	@echo "All tests passed"
```

### A6. 验证

```bash
# 验证 MAP 文件结构
ls conventions/THE_CODEX.md conventions/rules/ conventions/templates/ conventions/scripts/

# 验证脚本语法
bash -n conventions/scripts/setup_map.sh
bash -n conventions/scripts/heartbeat.sh

# 验证 import-linter 配置（需先 pip install import-linter）
python3 -m importlinter lint 2>&1 || echo "请先配置 .importlinter"

# 验证 AI_RULES.md 无未替换的占位符
grep -n '{{' AI_RULES.md && echo "⚠️ 有未替换的占位符" || echo "✅ 占位符全部替换"
```

### A7. 提交

```bash
git add -A
git commit -m "feat: bootstrap MAP (Meta-Agent-Protocol) v1.0.1

- conventions/ submodule → rock913/Meta-Agent-Protocol
- AI_RULES.md (9 法则行为宪法)
- .aider.conf.yml (执行引擎配置)
- .importlinter (跨系统 import 防火墙)
- delegate_to_aider.sh (委派桥接)
- WORKSPACE_MAP.md (全局坐标系)
- meta-docs/workspace-structure.md (目录拓扑)

Note: clone 时需 git submodule update --init"
git push origin main
```

---

## 路径 B：迁移升级 (Migration)

> 适用场景：你的仓库已有一个嵌入的 `conventions/` 目录（从旧 AI4S 同步而来），需要替换为 MAP submodule。

### B1. 备份

```bash
cd /path/to/your/repo

# 备份旧 conventions/（保留你的自定义内容）
cp -r conventions/ /tmp/conventions-backup-$(date +%Y%m%d)/
```

### B2. 删除旧目录

```bash
git rm -r conventions/
git commit -m "refactor: remove embedded conventions/ — migrating to MAP submodule"
```

### B3-B7: 同路径 A

执行 [A1 添加 MAP submodule](#a1-添加-map-submodule) 到 [A7 提交](#a7-提交) 的全部步骤。

> ⚠️ 如果 `setup_map.sh` 提示文件已存在并 SKIP，那是因为你的旧配置还在。使用 `--force` 覆盖，或手动对比新旧版本后合并。

---

## 首次 clone（团队成员）

团队成员 clone 你的仓库后，需要额外一步拉取 MAP submodule：

```bash
git clone <your-repo-url>
cd <your-repo>
git submodule update --init --recursive   # 拉取 MAP submodule
```

---

## 日常操作

### 升级 MAP 版本

当 MAP 发布新版本时：

```bash
cd conventions
git pull origin main          # 拉取 MAP 最新版本
cd ..
git add conventions            # 锁定新版本指针
git commit -m "chore: bump MAP submodule to vX.Y.Z"
git push origin main
```

### 向 MAP 贡献

MAP 是开源项目，欢迎 PR：

1. Fork [rock913/Meta-Agent-Protocol](https://github.com/rock913/Meta-Agent-Protocol)
2. 在 fork 中修改 → 向 MAP 主仓库提 PR
3. PR 合入后 → 所有订阅者各自 `cd conventions && git pull origin main`

### 定时心跳

```bash
# 添加到 cron（每 30 分钟检查 git 状态 + 运行测试）
*/30 * * * * /path/to/your/repo/conventions/scripts/heartbeat.sh >> /tmp/map_heartbeat.log 2>&1
```

---

## 占位符速查卡片

```
┌─────────────────────────────────────────────────────────┐
│  AI_RULES.md 占位符                                       │
│  {{TEST_COMMANDS}}      每个子项目的 pytest 命令           │
│  {{REDLINE_EXTRA}}      额外红线文件（可删除）               │
│  {{TEST_TARGETS}}       make test-all 子目标               │
│  {{PRD_PATH_MAP}}       子项目→PRD 路径                     │
│  {{LOCAL_CONVENTIONS_SUMMARY}}  一句话约束                  │
├─────────────────────────────────────────────────────────┤
│  .aider.conf.yml 占位符                                    │
│  {{WORKSPACE_NAME}}     工作空间名称                        │
│  {{PRD_DOC_MAP}}        子项目 PRD 文档路径                 │
│  {{ROADMAP_PATH_MAP}}   子项目 ROADMAP 路径                 │
│  {{PRD_PATH_MAP}}       主 PRD 路径映射                     │
├─────────────────────────────────────────────────────────┤
│  .importlinter 占位符                                      │
│  {{PACKAGE_LIST}}       所有 Python 包名                   │
│  {{MODULE_LIST}}        同上                               │
│  {{IGNORE_IMPORTS}}     自引用豁免                          │
│  {{LAYER_LIST}}         分层列表                            │
└─────────────────────────────────────────────────────────┘
```

---

> **下一步**：阅读 `THE_CODEX.md` 了解 9 法则全文，阅读 `rules/arch-rules.md` 了解架构约束，阅读 `rules/agent-loop.md` 了解双引擎协作。
