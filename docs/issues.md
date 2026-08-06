# Research Output Issues

## Issues

| # | item | type | severity | description |
|---|---|---|---|---|
| 1 | `Table_network_and_simulation_descriptive_summary.xlsx` | table | minor | The workbook has 10 columns, whereas the Section 8 plan specifies an 8-column table. The two additional descriptor fields are interpretable, the 40 data rows are complete where statistics are meaningful, and the discrepancy does not affect the reported results, but the planned and delivered structures should be reconciled. |
| 2 | Eight superseded scripts in `src/analyses/` | script | minor | Eight scripts for fixed disruption scenarios, Shapley or corridor attribution, municipal-loss mapping, hospital reallocation, population-loss mapping, or the uniform-failure pilot remain mixed with the accepted length-dependent pipeline without an archive location or a consistent inactive marker. Their outputs are absent from the current plan, so their placement leaves the reproducible evidence chain unnecessarily ambiguous. |

## Severity Summary

| severity | count |
|---|---|
| critical | 0 |
| major | 0 |
| minor | 2 |

## Recommended Next Steps

- 将 AnaSOP Section 8 中 Network and Simulation Descriptive Summary 的计划列数由 8 更新为当前已接受的 10 列；无需重新生成表格。
- 将 8 个已被当前研究设计替代的脚本移入明确的 archive 目录，或加上统一的 inactive 标记；保留仍被正式流程导入的共享路由模块。
- 当前没有 critical 或 major 问题，可以继续运行 `build-content-dictionary`。上述两项 minor 可在内容字典构建前一并整理，也可作为不阻断研究进度的仓库清理事项。
