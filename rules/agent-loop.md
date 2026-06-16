# Agent Loop — 双引擎微循环协作规范

> 版本：v1.0.0 | 2026-06-16
> 本文件定义 Claude Code（架构师）+ Aider/执行引擎（执行者）的协作模式、Task 文件格式和标准执行循环。
> 与 THE_CODEX.md 法则九配套使用。

---

## 1. 双引擎架构

```
Claude Code (架构师/Tech Lead)     执行引擎 (Executor/Dev)
──────────────────────────────     ──────────────────────────
✅ 读 PRD、分析架构                  ✅ 精准修改指定文件
✅ 原子化拆解任务                    ✅ 严格按 task 文件范围工作
✅ 生成 .aider_task.md              ❌ 不读 PRD、不做架构决策
✅ 运行 pytest / lint、读报错         ❌ 不运行测试
✅ 纠错循环 (更新 task → 重唤执行)    ❌ 不主动扩大修改范围
❌ 不写大量业务代码
❌ 不一次性把 7 步全给执行引擎
```

## 2. 原子 Task 文件格式

每次唤醒执行引擎前，生成 task 描述文件：

```markdown
# Task: <简短描述>
> Proposal: <PRD proposal 路径> | Step: <N>/<Total>

## Context
<从 PRD 提取的 ≤5 行上下文>

## Files to Modify
- <文件路径> — <改什么>

## Contract
- Input: <结构>
- Output: <结构>

## Do NOT
- ❌ 不要修改 <文件>
- ❌ 不要运行测试
```

## 3. 标准执行循环

```bash
# 1. 架构师生成 task 文件
# 2. 架构师唤醒执行引擎（指定文件，限定范围）
./delegate_to_aider.sh /tmp/.aider_task.md <target_file.py>

# 3. 执行引擎退出 → 架构师跑测试
cd <project> && python3 -m pytest tests/unit/test_<module>.py -v

# 4. 红灯 → 架构师读报错 → 更新 task 文件 → 回到步骤 2
#    绿灯 → 下一步
```

## 4. 任务粒度控制

| 级别 | 范围 | 适用场景 | 示例 |
|:--:|------|------|------|
| L0 | 单个函数 | Bug fix | 修复 `parse_date()` 空字符串处理 |
| **L1 (默认)** | **单个文件** | **新模块** | 新增 `age_filter.py` |
| L2 | 2-3 相关文件 | 模块 + 测试 | 新增 `age_filter.py` + `test_age_filter.py` |
| L3 | 跨目录 | 后端 + 前端 | 必须拆分为 L1+L1 |

**铁律**：默认 L1。一次执行引擎调用 = 一个文件。绝不超过 L2。

## 5. 纠错循环模式

```
架构师写 task → 执行引擎改代码 → 架构师跑测试
                                      │
                        ┌─ 绿灯 → 下一步 ─┐
                        │                  │
                        └─ 红灯 → 读报错 ─┘
                              │
                        更新 task 文件
                              │
                        重唤执行引擎
```

**关键**：架构师不猜测报错原因，直接把 pytest 输出贴在更新后的 task 文件中。

## 6. 执行引擎配置文件

```yaml
# .aider.conf.yml
model: deepseek/deepseek-v4-pro
map-tokens: 8000
auto-commits: true

message: |
  你是 <Workspace Name> 的全局架构执行引擎 (Executor)。

  ## 启动时必读
  1. WORKSPACE_MAP.md — 全局项目拓扑和依赖隔离红线
  2. AI_RULES.md — 行为宪法 (9 法则)
  3. 目标子项目的 CONVENTIONS.md — 地方法规
  4. 目标子项目的 PRD 文档 — 功能规格

  ## PRD Sync Iron Law
  开发完成后**必须**同时更新 ROADMAP.md + 主 PRD

  ## Git Push 策略
  每完成一个独立任务 → git commit + git push
  禁止任务完成后不 push，让代码在本地堆积
```

## 7. 委托桥接脚本

架构师通过桥接脚本将任务委派给执行引擎。执行引擎的冗长 TDD 循环日志写入 `/tmp`，只返回 git diff 摘要给架构师 → Token 成本可控。

```bash
#!/bin/bash
# delegate_to_aider.sh — 架构师 → 执行引擎 委派桥接
# Usage: ./delegate_to_aider.sh <task_file> <target_files...>

TASK_FILE="$1"
shift
TARGET_FILES="$@"

if [ ! -f "$TASK_FILE" ]; then
    echo "Task file not found: $TASK_FILE"
    exit 1
fi

echo "Delegating to Aider..."
echo "   Task: $(head -1 $TASK_FILE)"
echo "   Files: $TARGET_FILES"

# 调用 Aider，日志写入 /tmp
TASK_CONTENT=$(cat "$TASK_FILE")
aider --model deepseek/deepseek-v4-pro \
      --message "$TASK_CONTENT" \
      $TARGET_FILES \
      2>&1 | tee /tmp/aider_$(date +%Y%m%d_%H%M%S).log

echo ""
echo "Git diff summary:"
git diff --stat
```

## 8. 禁止模式

- ❌ 把 ≥3 个逻辑步骤打包进一次 `--message`
- ❌ 不生成 task 文件直接调用执行引擎（简单 bug fix 除外）
- ❌ 执行引擎卡住 >2 分钟不介入（停止并检查日志）
- ❌ 跳过架构师测试验证环节（执行引擎退出后必须跑 pytest）
- ❌ 架构师自己动手写大量业务代码（你是 Tech Lead，不是 Dev）

## 附录：Host Repo 初始化清单

当宿主仓库引入 MAP 后，需要准备以下基础设施：

| 文件 | 角色 | 来源 |
|------|------|------|
| `AI_RULES.md` | 全局 Agent 行为宪法 | `setup_map.sh` 从模板生成 |
| `.aider.conf.yml` | 执行引擎全局配置 | `setup_map.sh` 从模板生成 |
| `delegate_to_aider.sh` | 委派桥接脚本 | 从本文件 §7 复制 |
| `WORKSPACE_MAP.md` | 全局坐标系 | 宿主自行编写 |
| `Makefile` | 全局测试/lint/git 编排 | 宿主自行编写 |
| `.importlinter` | 物理级跨系统 import 拦截 | `setup_map.sh` 从模板生成 |
