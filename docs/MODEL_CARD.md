# Model Card — Gold4Cast v1.0

[نسخه فارسی](MODEL_CARD_FA.md)

## Model
XGBoost Quantile Regression (`reg:quantileerror`).

## Intended use
Research, probabilistic market forecasting, model evaluation, and educational/engineering experimentation.

## Not intended for
Guaranteed price targets, guaranteed downside floors, autonomous trading without independent risk controls, or personalized financial advice.

## Inputs
- Iranian 18K gold
- USD/IRR
- XAU/USD

## Outputs
Q10, Q50, Q90 endpoint forecasts at 63, 126, and 252 trading sessions.

## Important UI note
Scenario paths shown in the HTML are visual interpolations between the current price and endpoint quantiles. They are not day-by-day XGBoost forecasts.

## Risks
Structural breaks, stale/bad data, FX regime changes, geopolitical events, policy shocks, extreme global-gold moves, and model miscalibration.
