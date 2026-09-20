# Validation — Gold4Cast v1.0

[نسخه فارسی](VALIDATION_FA.md)

## Setup

Target: Iranian 18K gold  
Covariates: USD/IRR and XAU/USD  
Primary model: XGBoost Quantile  
Horizons: 63 / 126 / 252 trading sessions  
Dense walk-forward origins: 131  
Origin spacing: 21 trading sessions

Because forecast windows overlap, observations are serially dependent. Descriptive leaderboard metrics are therefore supplemented with HAC/Newey-West-adjusted loss-differential tests.

## XGBoost dense walk-forward results

| Horizon | N | Mean pinball | Median MAPE | Coverage Q10–Q90 | Direction accuracy |
|---|---:|---:|---:|---:|---:|
| 63 / 3M | 131 | 0.0425576 | 12.8559% | 68.7023% | 71.7557% |
| 126 / 6M | 131 | 0.0723235 | 18.8869% | 61.8321% | 83.9695% |
| 252 / 12M | 131 | 0.1188316 | 29.5521% | 63.3588% | 90.0763% |

Overall:
- Avg pinball: 0.0779043
- Avg MAPE: 20.4316%
- Avg Q10–Q90 coverage: 64.6310%
- Avg direction accuracy: 81.9338%

## XGBoost vs Chronos-2

HAC-adjusted two-sided tests on the pinball-loss differential:

| Horizon | Mean XGB−Chronos loss difference | HAC statistic | p-value | XGB origin wins |
|---|---:|---:|---:|---:|
| 3M | -0.003785 | -1.075 | 0.282459 | 77/131 |
| 6M | -0.011428 | -1.601 | 0.109399 | 77/131 |
| 12M | -0.039397 | -3.003 | 0.002677 | 99/131 |
| Overall | -0.018203 | -2.418 | 0.015592 | 89/131 |

Negative loss differential favors XGBoost.

## Interpretation

The strongest statistical evidence in the current benchmark is at the 12-month horizon. The 3M and 6M pairwise differences are not statistically significant at the conventional 5% level.

These results should not be interpreted as universal superiority of XGBoost. They describe this dataset, feature construction, horizon definition, and validation design.

## Limitations

- Results are historical.
- Forecast windows overlap.
- Market structure can change.
- Quantile coverage is not perfectly calibrated.
- Future shocks can lie outside the historical regime.
- Data quality and source methodology matter.
