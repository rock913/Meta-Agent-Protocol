#!/bin/bash
# MAP v1.1 — Script syntax validation tests.
# Run: bash tests/test_scripts.sh

PASS=0
FAIL=0

SCRIPTS_DIR="$(cd "$(dirname "$0")/../scripts" && pwd)"

echo "=== MAP Script Syntax Check ==="
echo ""

for script in "$SCRIPTS_DIR"/*.sh; do
    name=$(basename "$script")
    if bash -n "$script" 2>/dev/null; then
        echo "  ✅ $name — syntax OK"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $name — syntax ERROR"
        FAIL=$((FAIL + 1))
    fi
done

echo ""
echo "=== Result: $PASS passed, $FAIL failed ==="

[ $FAIL -eq 0 ] || exit 1
