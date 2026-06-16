# AgenticOps 局部开发法则

> 本文件是 AgenticOps 子项目的"地方法规"。
> 全局宪法见根目录 `AI_RULES.md`。

## 技术栈
- 后端：Python 3.10+ + FastAPI + SQLite WAL
- 前端：Vue 3 + Element Plus + ECharts (暗色主题大屏)
- 实时推送：SSE (复用 GraphMRI-Lite 模式)

## 架构红线 (Hard Boundaries)
1. **Telemetry 标准化**：所有事件遵循 `collector/schema.py` 的 JSON Schema
2. **SSE 复用**：实时推送模式参考 GraphMRI-Lite `server.py` 的 SSE 实现
3. **飞书联动**：告警通过 `alerts/feishu.py` 发送，复用 A13 的消息卡片格式

## 测试
- 运行：`make test-agenticops` 或 `python3 -m pytest tests/ -v`

## 关键指标
- Token 成本追踪：按模型分组的 USD/Bug 指标
- Agent 状态灯：HR Dashboard 的实时状态指示灯
- 告警规则：token_spike / loop_detection / cost_budget_breach

## 禁止行为
- ❌ 直接 import SROS/ARC/GraphMRI 的代码
- ❌ 硬编码 API 端点和 Token
- ❌ 飞书消息绕过 `alerts/feishu.py` 直接发送
