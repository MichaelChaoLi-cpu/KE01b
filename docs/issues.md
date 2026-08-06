# Research Output Issues

## Issues

| # | item | type | severity | description |
|---|---|---|---|---|
| 1 | `run_length_weighted_monte_carlo_full.py` and AnaSOP Section 6.2 | method/script | major | AnaSOP defines P90 emergency access time as the 90th percentile of finite travel times, with infinite outcomes reported separately. The implementation instead takes the percentile over all 1,000 outcomes and returns an unreachable P90 when at least 10% of outcomes are infinite. The reported tables follow the implementation, so the documented estimand and the computed estimand do not match. |
| 2 | Hospital Service Reliability outputs | evidence coverage | major | The required robustness checks for alternative operational-hospital sets and separately labelled hospital-role or hospital-capacity weighting specifications are not implemented in the current scripts or outputs. Hospital reliability conclusions therefore lack two prespecified sensitivity analyses. |
| 3 | Municipal Emergency Access Reliability outputs | evidence coverage | major | AnaSOP requires municipal rank-stability assessment across Monte Carlo replicate checkpoints, but the current municipal table reports reliability levels and uncertainty only. No script or output tests whether municipal rankings remain stable as the number of replicates increases. |
| 4 | AnaSOP Section 7 Analytical Workflow | plan | major | Workflow steps 1–7 still characterize the formal simulation, reliability products, hospital results, grid results, road-section results, and audit evidence as pending or inconclusive, although the corresponding validated outputs now exist. This makes the analytical evidence map inconsistent with the repository state and risks incorrect downstream content assembly. |
| 5 | `Table_network_and_simulation_descriptive_summary.xlsx` | table | minor | The workbook has 10 columns, whereas the Section 8 plan specifies an 8-column table. The additional descriptor columns are interpretable, but the planned and delivered table structures should be reconciled. |
| 6 | `Figure_monte_carlo_convergence_and_stress_sensitivity.png` | figure | minor | Panel b retains a “Not stable” legend category even though every displayed non-reference checkpoint satisfies the confirmed 5-percentage-point stability rule. Its annotation highlights only the 1,000-replicate checkpoint and does not communicate that all displayed checkpoints from 250 onward are stable. |
| 7 | Legacy scripts in `src/analyses/` | script | minor | Several scripts implement superseded fixed-scenario, Shapley/corridor, municipal-loss, hospital-reallocation, or 100 m segmentation designs but remain mixed with the active analysis pipeline without an archive location or inactive marker. This creates ambiguity about which scripts reproduce the accepted evidence set. |

## Severity Summary

| severity | count |
|---|---|
| critical | 0 |
| major | 4 |
| minor | 3 |

## Recommended Next Steps

- 先重新运行 `estimation-framework-planning`：统一 P90 急救时间的文字定义与实际估计量，并依据现有正式结果更新 AnaSOP Section 7 的证据状态。
- 对“替代运营医院集合／医院角色或容量权重”和“市町村排名随重复次数的稳定性”补充明确的输出设计；如继续保留这两项预设检验，应更新 `figure-table-planning`，随后通过 `figure-table-generation` 生成并核验结果。
- 在 `figure-table-generation` 中修订蒙特卡洛收敛图：移除当前未使用的 “Not stable” 图例项，并准确说明从 250 次到 1,000 次检查点均满足 5 percentage points 稳定性规则。
- 统一 Section 8 与网络描述表的列结构：可以接受现有 10 列并修订计划，或按计划重制为 8 列，但两者必须一致。
- 在进入 `build-content-dictionary` 前，将旧设计脚本移入明确的归档位置或加上 inactive 标记，避免旧分析链与当前正式证据链混淆。
