# Model Selection History

[نسخه فارسی](MODEL_SELECTION_FA.md)

Gold4Cast did **not** select XGBoost by default. The v1.x primary model was
chosen after staged out-of-sample benchmarking against established forecasting
models using their published/standard implementations.

## Models already evaluated

- **XGBoost Quantile** — official `reg:quantileerror` objective
- **TimesFM-3** — Google, `google/timesfm-3.0-pytorch`
- **Chronos-2** — Amazon
- **Moirai-2.0** — Salesforce, `Salesforce/moirai-2.0-R-small`

No ensemble is used in the v1.x production forecast.

## Stage 1A — Gold-only screening

The first benchmark used 11 non-overlapping forecast origins.

| Model | Average pinball loss |
|---|---:|
| XGBoost Quantile | 0.06916 |
| TimesFM-3 | 0.07703 |
| Chronos-2 | 0.07913 |
| Moirai-2.0 | 0.10118 |

This was only a screening stage.

## Stage 1B — multivariate screening

The benchmark was then repeated with:

- Iranian 18K gold
- USD/IRR
- XAU/USD

again over 11 non-overlapping origins.

| Model | Avg pinball | Avg MAPE | Q10-Q90 coverage | Direction |
|---|---:|---:|---:|---:|
| XGBoost Quantile | 0.07218 | 19.06% | 72.73% | 90.91% |
| Chronos-2 | 0.07335 | 17.01% | 81.82% | 72.73% |
| TimesFM-3 | 0.07548 | — | — | — |
| Moirai-2.0 | 0.11017 | — | — | — |

For XGBoost vs Chronos-2, the exact permutation comparison across the 11
independent origins was not decisive overall:

- overall XGB − Chronos pinball difference: **-0.00117**
- XGBoost wins: **6/11**
- Chronos-2 wins: **5/11**
- two-sided exact permutation p-value: **0.930664**

Therefore Gold4Cast did **not** stop at the small 11-origin comparison.

## Stage 2 — dense walk-forward benchmark

The two strongest candidates from the screening stage, **XGBoost Quantile**
and **Chronos-2**, were taken into a denser walk-forward test:

- **131 forecast origins**
- one new origin every **21 trading sessions**
- horizons: **63 / 126 / 252 trading sessions**
- overlapping forecast windows
- HAC/Newey-West-adjusted statistical comparison

### Dense results

| Horizon | XGBoost pinball | Chronos-2 pinball | XGBoost MAPE | Chronos-2 MAPE | XGBoost direction | Chronos-2 direction |
|---|---:|---:|---:|---:|---:|---:|
| 3M / 63 | 0.0425576 | 0.0463426 | 12.8559% | 14.1218% | 71.7557% | 62.5954% |
| 6M / 126 | 0.0723235 | 0.0837518 | 18.8869% | 23.2925% | 83.9695% | 64.1221% |
| 12M / 252 | 0.1188316 | 0.1582288 | 29.5521% | 45.4325% | 90.0763% | 70.2290% |

Overall:

| Model | Avg pinball | Avg MAPE | Q10-Q90 coverage | Direction |
|---|---:|---:|---:|---:|
| XGBoost Quantile | 0.0779043 | 20.4316% | 64.6310% | 81.934% |
| Chronos-2 | 0.0961077 | 27.6156% | 69.9746% | 65.6489% |

### HAC/Newey-West comparison

Pinball-loss difference is defined as **XGBoost − Chronos-2**, so negative
values favor XGBoost.

| Horizon | Mean loss difference | HAC statistic | p-value | XGBoost wins |
|---|---:|---:|---:|---:|
| 3M | -0.003785 | -1.075 | 0.282459 | 77/131 |
| 6M | -0.011428 | -1.601 | 0.109399 | 77/131 |
| 12M | -0.039397 | -3.003 | 0.002677 | 99/131 |
| Overall | -0.018203 | -2.418 | 0.015592 | 89/131 |

The strongest individual-horizon evidence was at 12 months. The 3M and 6M
differences were not individually significant at the conventional 5% level.

## Why XGBoost is the current production model

XGBoost Quantile was selected for Gold4Cast v1.x because it produced the
strongest dense historical performance in the current benchmark, especially at
12 months, while remaining simple to deploy and audit.

This does **not** claim that XGBoost is universally superior to foundation
models. XGBoost also has a task-specific training advantage here, while the
foundation models were evaluated as published forecasting candidates.

## Before proposing another model

Please check this document before opening a model-replacement issue.

A proposal that simply says “try TimesFM-3”, “try Chronos-2”, or “try
Moirai-2.0” duplicates work already completed.

A new proposal is useful when at least one of the following is true:

1. a materially newer model/version has been released;
2. an official capability not used in the existing benchmark is relevant;
3. a reproducible paper or implementation provides a materially different,
   justified setup;
4. the candidate is evaluated under the same leakage-free walk-forward
   protocol and improves out-of-sample evidence;
5. the contribution improves calibration, robustness, speed, or deployment
   without weakening predictive performance.

Gold4Cast does not adopt a new model merely because it is newer, larger, or
more complex. Stable model changes require reproducible out-of-sample evidence.
