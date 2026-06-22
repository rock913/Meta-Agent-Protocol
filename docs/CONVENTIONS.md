# MAP 局部开发法则

> 本文件是 MAP (Meta-Agent-Protocol) 项目的"地方法规"。
> 联邦宪法见 `THE_CODEX.md`。功能规格见 `docs/PRD.md`。

## 技术栈
- Markdown（规则文本格式）
- Bash（脚本语言，POSIX 兼容）
- Python 3.10+（测试框架，pytest）
- Git Submodule（分发机制）

## 架构红线 (Hard Boundaries)
1. **9 法则不可变编号**：THE_CODEX 中的法则编号 (一~九) 永不变更
2. **占位符向后兼容**：templates/ 中的 `{{PLACEHOLDER}}` 可新增不可删除
3. **脚本零依赖**：scripts/ 中的 Bash 脚本仅依赖 POSIX 工具 (git, grep, sed)
4. **MIT 许可证**：所有代码和模板采用 MIT，最大化采用率

## 修改后强制操作
1. 运行 `python3 -m pytest tests/ -v`（模板/一致性检查）
2. 运行 `bash tests/test_scripts.sh`（脚本语法检查）
3. 更新 `CHANGELOG.md`（按版本号分段）
4. 更新 `VERSION` 文件（如涉及 MAJOR/MINOR）
5. 如涉及 MAJOR 变更：在 `INTEGRATION.md` 中添加迁移指南

## 测试铁律
- 修改模板 → `tests/test_templates.py`
- 修改脚本 → `tests/test_scripts.sh`
- 修改 THE_CODEX → `tests/test_cross_consistency.py`
- 发布前 → 全部 3 个测试

## 禁止行为
- ❌ 删除或重编号 THE_CODEX 法则
- ❌ 删除 templates/ 中的现有占位符
- ❌ 在 scripts/ 中引入非 POSIX 依赖（如 python, jq）
- ❌ 修改 `setup_map.sh` 生成的文件路径
- ❌ 跳过测试直接发布新版本

## 关键文件速查
| 文件 | 用途 |
|------|------|
| `THE_CODEX.md` | 联邦宪法 (9 法则) |
| `INTEGRATION.md` | 宿主仓库接入指引 |
| `templates/` | 可实例化的配置模板 |
| `scripts/setup_map.sh` | 一键脚手架 |
| `sub-project-conventions/` | 子项目 CONVENTIONS 参考模板 |
| `tests/` | 自动化验证 |
