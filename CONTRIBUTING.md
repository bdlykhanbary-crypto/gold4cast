# Contributing to Gold4Cast

[راهنمای فارسی](CONTRIBUTING_FA.md)

Contributions are welcome from developers, quantitative researchers, data engineers, UI developers, and financial-modeling practitioners.

## Before coding

For significant changes, open an Issue first and describe:

1. the problem,
2. the proposed change,
3. whether model outputs can change,
4. how you plan to validate the change.

## Pull request requirements

A PR that changes forecasting behavior should include:

- no look-ahead leakage,
- a reproducible walk-forward evaluation,
- comparison against the current v1.0 baseline,
- horizon-level metrics for 63/126/252 sessions,
- probabilistic calibration metrics when quantiles are affected,
- documentation of any new hyperparameters,
- no proprietary datasets committed to the repository.

## Preferred improvement areas

- lawful/open data providers,
- quantile calibration,
- model drift detection,
- robust missing-data handling,
- alternative forecasting models with reproducible benchmarks,
- block-bootstrap/HAC statistical comparison,
- faster inference,
- better mobile UI,
- automated tests,
- internationalization.

## Style

Keep modeling logic explicit and auditable. Avoid adding an ensemble, indicator, or handcrafted feature without a benchmark showing why it helps.

## Security and data

Never commit API keys, private tokens, credentials, private datasets, or user-specific account information.
