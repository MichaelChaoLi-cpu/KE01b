# Research Output Issues

## Issues

| # | item | type | severity | description |
|---|---|---|---|---|
| 1 | Eight superseded scripts in `src/analyses/` | script | minor | Eight scripts for the former fixed Low/Central/High disruption scenarios, corridor/Shapley attribution, municipal and hospital reallocation maps, population-loss mapping, or the uniform-failure pilot remain alongside the accepted junction-section, length-dependent Monte Carlo pipeline without an archive location or consistent inactive marker. None of the current nine figures or six tables depends on these superseded outputs, so they do not affect the reported evidence, but their placement makes the intended reproduction path less explicit. |

## Severity Summary

| severity | count |
|---|---:|
| critical | 0 |
| major | 0 |
| minor | 1 |

## Recommended Next Steps

- 将 8 个已被当前研究设计替代的脚本移入明确的 archive 目录，或增加统一的 inactive/legacy 标记和说明；保留仍被正式图件调用的共享路由模块。
- 当前 9 张图和 6 张表均未发现阻断性问题，可以继续运行 `build-content-dictionary`。上述 minor 属于不阻断研究进度的仓库整理事项。
