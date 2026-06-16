# GraphMRI-Lite 局部开发法则

> 本文件是 GraphMRI-Lite 子项目的"地方法规"。Aider 在修改本目录下文件时自动读取。
> 全局宪法见根目录 `AI_RULES.md`。

## 技术栈
- 前端：Vue 3 Composition API + Tailwind CSS + Element Plus + Pinia + vue-i18n
- 后端：Python 3.10+ + FastAPI + SQLite WAL + SQLAlchemy
- CLI：Click + `--raw` JSON stdout
- 测试：pytest (后端) + Playwright (前端 E2E)

## 调度法则 (Scheduler Law)
- **必须且只能**调用 `GPUPoolScheduler`（`scheduler.py`）
- **绝对禁止** Celery 或任何外部任务队列
- Docker 仅限于 preprocess 模式（fMRIPrep/QSIPrep 容器）
- network/predict/visualize 模式使用原生 Python CLI（`graphmri --raw <command>`）

## 交互契约 (Interaction Contract)
- 任何与 SROS 的通信必须通过 **MCP 或 CLI `--raw` JSON**
- 禁止直接 HTTP 请求 SROS Gateway
- **禁止** `import sros` / `import arc_engine` (import-linter 拦截)
- 前端与后端通信：通过 `webui/src/api/index.js` 的 Axios 封装

## 前端规范
- 所有新 UI 组件放在 `webui/src/components/`
- 表单：使用 `DynamicForm.vue`（Schema-Driven 万能动态表单）
- 暗色主题：使用 CSS 变量，**禁止硬编码颜色**
- i18n：所有用户可见文本必须通过 `$t('...')` 或 `t('...')`
- 布局：使用 Splitpanes 可拖拽布局（`SessionWorkbench.vue`）

## 后端规范
- stdout=JSON (CLI 模式)：`graphmri --raw` 所有输出为合法 JSON
- 无状态 CLI：CLI 命令不依赖任何运行中的服务
- 零容器感知 UI：前端绝不暴露 Docker/Apptainer/Mount 等概念
- WAL 模式：SQLite 必须开启 `PRAGMA journal_mode=WAL`

## 测试铁律
- **TDD 强制**：先写 failing test → 实现 → pytest 绿灯
- 后端：`make test-graphmri` 或 `python3 -m pytest tests/ -v`
- 前端：`cd webui && npm run build`（构建成功 = 通过）
- E2E：Playwright 测试 (`tests/e2e/`)
- 当前基线：216+ tests green

## 禁止行为
- ❌ Celery 或任何外部任务队列
- ❌ `import sros` / `import arc_engine` (import-linter 拦截)
- ❌ 硬编码 API 路径、颜色值、端口号
- ❌ 在前端暴露 Docker/Apptainer/Mount 容器概念
- ❌ push main 分支 (SLAIB)

## 关键文件速查
| 文件 | 用途 |
|------|------|
| `graphmri_lite/server.py` | FastAPI 服务入口 |
| `graphmri_lite/cli/main.py` | Click CLI |
| `graphmri_lite/scheduler.py` | HybridResourceScheduler |
| `graphmri_lite/core/errors.py` | 10 ErrorCode + SUGGESTED_ACTIONS |
| `webui/src/components/DynamicForm.vue` | Schema-Driven 万能动态表单 |
| `webui/src/components/Omnibar.vue` | Cmd+K 自然语言指令栏 |
| `docs/PRD.md` | 主 PRD (v8.6) |
