# SXMU_MDD_Twin 局部开发法则

> 本文件是 SXMU_MDD_Twin 科学项目的"地方法规"。
> 全局宪法见根目录 `AI_RULES.md`。
> 研究方案见 `docs/PROTOCOL.md` (v1.6)。科学项目使用 PROTOCOL 替代 PRD。

## 核心原则

### 数据不进 Git
- 科研数据（NIfTI、DICOM、.mat、.edf）一律存放在交我算 Lustre
- 本仓库只存放代码、配置、文档
- `.env` 包含数据路径，已加入 `.gitignore`

### HPC 路径约定
- 数据根路径：`/lustre/home/acct-tifei.yuan/share/SXMU_Data/`
- BIDS 数据：`/lustre/home/acct-tifei.yuan/share/SXMU_Data/MRI/Bids_data/`
- 工作目录：`/lustre/home/acct-yuzhang2/yuzhang2/SXMU/`
- 登录节点：`pilogin.hpc.sjtu.edu.cn`

### 依赖的系统 MCP 工具
| 工具 | 来源 | 用途 |
|------|------|------|
| `sros-db-query` | SROS MCP Gateway | DuckDB 结构化查询 |
| `sros-hpc-submit` | SROS MCP Gateway | Slurm 作业提交 |
| `sros-hpc-status` | SROS MCP Gateway | 作业状态监控 |
| `arc-wiki-read` | ARC MCP Server | Data-Wiki 知识查询 |

## 测试与验证
- 数据分析脚本：通过 SROS MCP `sros-data-run-script` 执行
- HPC 作业：Slurm 模板（`config/slurm/`）+ `sros-hpc-submit`

## 禁止行为
- ❌ 将科研数据（NIfTI/DICOM/mat/edf）放入 Git
- ❌ 修改 `docs/PROTOCOL.md` 中的研究设计（需 PI 审批）
- ❌ 在 HPC 上直接运行重计算（必须通过 Slurm 模板）
