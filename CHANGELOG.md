# Changelog

## [1.0.1]
- Removed hard-coded third-party market-data provider coupling from the public loader.
- Added provider-agnostic normalized CSV input through `GOLD4CAST_DATA`.
- Changed the public GitHub Actions workflow to least-privilege `contents: read`.
- Removed automatic repository writes from the public forecasting workflow.
- Added constrained baseline dependency versions.
- Added English and Persian data-input documentation.

## [1.0.0]
- Selected XGBoost Quantile as the primary Gold4Cast forecasting model.
- Added Gold18 + USD/IRR + XAU/USD multivariate inputs.
- Added 3M / 6M / 12M probabilistic endpoint forecasts.
- Added Persian mobile-friendly HTML report.
- Added scenario visualization.
- Added permanent live forecast scorecard.
- Added dense walk-forward validation and HAC-adjusted comparison.
- Prepared bilingual English/Persian open-source documentation.
