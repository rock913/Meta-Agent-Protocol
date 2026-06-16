# ARC-Engine 局部开发法则

> 本文件是 ARC-Engine 子项目的"地方法规"。
> 全局宪法见根目录 `AI_RULES.md`。
> 功能规格见 `docs/PRD.md`。

## 技术栈
- Python 3.10+ + TypeScript (AST 解析器前端)
- Code-Wiki 编译器：Markdown 生成 + 知识图谱
- Data-Wiki Pipeline：DuckDB → Jinja2 模板 → Markdown 页面
- MCP Server：`arc_data_wiki_read` tool

## 架构红线 (Hard Boundaries)
1. **TDD mandatory**：每个核心模块 ≥ 1 个 pytest，先写 failing test 再实现
2. **核心签名冻结**：`emit_ok()` / `emit_error()` / `run_skill()` 不可变
3. **Code-Wiki 自主闭环**：`claw-graph-query` + `make update-wiki` 自动生成图谱
4. **Offline-First**：所有测试可在无网络环境运行

## 测试铁律
- 运行：`make test-arc` 或 `python3 -m pytest second-brain/tests/ -v`
- 当前基线：455 tests green (second-brain: 359 + core: 21 / 5 pre-existing network failures)
- 新增 Data-Wiki 功能必须含契约回归测试 (参考 M30 模式)

## 契约回归 CI (M30 模式)
`.github/workflows/sros-contract-test.yml` — sparse-checkout SROS `contracts/` 快照 → dry-run 验证兼容性

## 禁止行为
- ❌ 修改核心签名 (`emit_ok` / `emit_error` / `run_skill`)
- ❌ `import sros` / `import graphmri_lite` (import-linter 拦截)
- ❌ 提交未通过 Code-Wiki 更新的代码 (`make update-wiki` 未运行)
