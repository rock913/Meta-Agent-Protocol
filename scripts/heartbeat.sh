#!/usr/bin/env bash
# heartbeat.sh — Loop Engineering 自动化心跳脚本
# 周期性检查 git 状态 + 运行测试，适合 cron/systemd timer 集成。
#
# Usage:
#   bash conventions/scripts/heartbeat.sh              # 一次性执行
#   bash conventions/scripts/heartbeat.sh --check-only # 只检查 git 状态，不运行测试
#   bash conventions/scripts/heartbeat.sh --test-only  # 只运行测试，不检查 git 状态
#
# Cron 示例 (每 30 分钟检查一次):
#   */30 * * * * /path/to/conventions/scripts/heartbeat.sh >> /tmp/heartbeat.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAP_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 尝试自动检测宿主仓库根目录
# 如果 MAP 作为 git submodule 引入，宿主根 = MAP_ROOT/../..
HOST_ROOT="$(cd "$MAP_ROOT/../.." && pwd 2>/dev/null || echo "")"
if [ -z "$HOST_ROOT" ] || [ ! -f "$HOST_ROOT/Makefile" ]; then
    # 回退：假设从宿主仓库直接调用
    HOST_ROOT="$(pwd)"
fi

MODE="${1:---full}"

echo "━━━ Heartbeat $(date '+%Y-%m-%d %H:%M:%S') ━━━"
echo "   Host: $HOST_ROOT"

# ─── Phase 1: Git Status Check ───
if [[ "$MODE" != "--test-only" ]]; then
    echo ""
    echo "--- Git Status ---"

    cd "$HOST_ROOT"

    # Check for uncommitted changes
    DIRTY=$(git status --short 2>/dev/null | wc -l || echo "0")
    if [ "$DIRTY" -gt 0 ]; then
        echo "⚠️  $DIRTY uncommitted files:"
        git status --short | head -20
    else
        echo "✅ Working tree clean"
    fi

    # Check for unpushed commits
    BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    AHEAD=$(git rev-list --count origin/$BRANCH..HEAD 2>/dev/null || echo "0")
    BEHIND=$(git rev-list --count HEAD..origin/$BRANCH 2>/dev/null || echo "0")

    if [ "$AHEAD" -gt 0 ]; then
        echo "⚠️  $AHEAD unpushed commits on $BRANCH"
    fi
    if [ "$BEHIND" -gt 0 ]; then
        echo "⚠️  $BEHIND new commits on remote/$BRANCH — consider git pull"
    fi
    if [ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ]; then
        echo "✅ Branch $BRANCH in sync with remote"
    fi
fi

# ─── Phase 2: Test Suite ───
if [[ "$MODE" != "--check-only" ]]; then
    echo ""
    echo "--- Test Suite ---"

    if [ -f "$HOST_ROOT/Makefile" ] && grep -q "test-all" "$HOST_ROOT/Makefile"; then
        echo "Running: make test-all"
        cd "$HOST_ROOT"
        make test-all 2>&1 | tail -30
        echo ""
        echo "✅ make test-all completed"
    else
        echo "⚠️  No Makefile with 'test-all' target found."
        echo "   Create a Makefile with per-project test targets + 'test-all'."
        echo "   See MAP rules/arch-rules.md for guidance."
    fi
fi

echo ""
echo "━━━ Heartbeat complete ━━━"
