# Agent Loop — 双引擎微循环协作规范

> 版本：v1.1.0 | 2026-06-24
> 本文件定义 Claude Code（架构师）+ Aider/执行引擎（执行者）的协作模式、Task 文件格式和标准执行循环。
> 与 THE_CODEX.md 法则九配套使用。
> v1.1.0 新增：L0-L3 任务分级策略 — 区分机械任务 vs 复杂功能，降低流程摩擦。

---

## 1. 双引擎架构

```
Claude Code (架构师/Tech Lead)     执行引擎 (Executor/Dev)
──────────────────────────────     ──────────────────────────
✅ 读 PRD、分析架构                  ✅ 精准修改指定文件
✅ 任务分级 (L0-L3)                  ✅ 严格按 task 文件范围工作
✅ 生成 .aider_task.md              ❌ 不读 PRD、不做架构决策
✅ 运行 pytest / lint、读报错         ❌ 不运行测试
✅ 纠错循环 (更新 task → 重唤执行)    ❌ 不主动扩大修改范围
✅ L0 机械任务直接执行               ❌ 不写大量业务代码
❌ L1+ 不一次性把 7 步全给执行引擎
```

### L0 例外

架构师在 L0 机械任务（rename/sed/模板替换/import 批量修改）中**直接执行**，
pytest 全量回归作安全网。这不是角色越界，而是任务分级策略。
详见 §4。

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

## 4. 任务分级策略 (L0-L3)

> v1.1.0 核心升级 — 不是所有任务都需要 proposal → delegate 流水线。

```
┌─────────────────────────────────────────────────────────┐
│  L0 机械任务 (rename / move / sed / 模板替换 / import)    │
│  → 架构师直接执行  pytest 全量回归作安全网                │
│  特征: 无算法决策，纯文本变换，确定性结果，>50 文件        │
│  例: Ω1 全栈重命名 (89 files, sed + git mv)              │
│  工具: sed + find + git mv，pytest 事后验证               │
├─────────────────────────────────────────────────────────┤
│  L1 单文件新模块 (新函数 / 新类 / 新 endpoint)            │
│  → 轻量 proposal (≤50 行) + 执行引擎                      │
│  特征: 有参考实现可抄，改动范围 ≤1 文件                   │
│  工具: .aider_task.md + delegate_to_aider.sh             │
├─────────────────────────────────────────────────────────┤
│  L2 跨文件功能 (2-5 文件联动)                             │
│  → 标准 proposal + 架构师规划 + delegate_to_aider        │
│  特征: 需要架构规划，但实现范围可控                        │
│  工具: proposal + task 拆解 + 逐文件委派                  │
├─────────────────────────────────────────────────────────┤
│  L3 跨系统变更 (MCP 契约 / Schema / 多项目联动)           │
│  → 完整 proposal + Contract Spec + 多会话交付             │
│  特征: 需要多方协调，不可单人草率执行                      │
│  工具: full proposal template + Quick Start + cross_system_contracts │
└─────────────────────────────────────────────────────────┘
```

### 分级判断速查

| 问题 | 是 → L0 | 否 → L1+ |
|------|:------:|:-------:|
| 改动是否纯文本替换，不涉及算法逻辑？ | ✅ L0 | ❌ |
| 结果是否可被 pytest 100% 验证？ | ✅ L0 | ❌ |
| git diff 是否可被人类一眼审完？ | ✅ L0 | ❌ |
| 是否需要架构决策或参考实现调研？ | ❌ | ✅ L1+ |

### 铁律

- **L0**: 架构师执行后必须跑全量 pytest，红灯立即回滚修正
- **L1**: 默认粒度。一次执行引擎调用 = 一个文件
- **L2**: 必须拆分为独立 task 文件逐文件委派
- **L3**: 必须包含 Contract Spec + cross_system_contracts，不可单人草率执行

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
- ❌ 不生成 task 文件直接调用执行引擎（L0 机械任务和简单 bug fix 除外）
- ❌ 执行引擎卡住 >2 分钟不介入（停止并检查日志）
- ❌ 跳过测试验证环节（任何代码变更后必须跑 pytest）
- ❌ 架构师在 L1+ 任务中自己动手写业务代码（L0 机械任务除外）
- ❌ 用 L0 策略处理 L1+ 任务（sed 批量改算法逻辑 = 灾难）
- ❌ 用 L3 流程处理 L0 任务（机械改名写 200 行 proposal = 浪费）

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
