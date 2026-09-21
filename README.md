# Gold4Cast

[نسخه فارسی](README_FA.md)

Gold4Cast is an open-source probabilistic forecasting project for Iranian 18K gold.  
The current v1.0 pipeline uses **XGBoost Quantile Regression** with three market inputs:

- Iranian 18K gold price
- USD/IRR
- XAU/USD

It produces probabilistic forecasts for approximately:

- **3 months** — 63 trading sessions
- **6 months** — 126 trading sessions
- **12 months** — 252 trading sessions

For each horizon, Gold4Cast reports:

- **Lower estimate (Q10)**
- **Main/median forecast (Q50)**
- **Upper estimate (Q90)**

The project also includes a Persian mobile-friendly HTML report, scenario charts, and a permanent live scorecard that compares old forecasts with realized prices after their forecast horizon has matured.

## Why open source?

Gold4Cast v1.0 is intentionally published so developers, quantitative researchers, data engineers, and financial-modeling practitioners can:

- audit the implementation,
- reproduce the validation,
- add legal and reliable data providers,
- improve calibration,
- test stronger models,
- improve the UI,
- add monitoring and model-drift detection,
- propose future Gold4Cast versions through pull requests.

## Current model

**Primary model:** XGBoost Quantile  
**Objective:** `reg:quantileerror`  
**Inputs:** Gold18 + USD/IRR + XAU/USD  
**Lag structure:** 63 raw return lags from the three series  
**Forecast horizons:** 63 / 126 / 252 trading sessions  
**Output quantiles:** Q10 / Q50 / Q90

Gold4Cast does **not** blend models in v1.0.

## Validation summary

The dense walk-forward benchmark used **131 forecast origins**, spaced every 21 trading sessions. Forecast windows overlap, so ordinary independent-sample tests are not appropriate. HAC/Newey-West-adjusted comparisons were therefore used for the XGBoost vs Chronos-2 loss differential.

Selected v1.0 results:

| Horizon | XGBoost Pinball | Median MAPE | 80% interval coverage | Direction accuracy |
|---|---:|---:|---:|---:|
| 3M | 0.04256 | 12.86% | 68.70% | 71.76% |
| 6M | 0.07232 | 18.89% | 61.83% | 83.97% |
| 12M | 0.11883 | 29.55% | 63.36% | 90.08% |

Overall:

- Average pinball loss: **0.07790**
- Average MAPE: **20.43%**
- Direction accuracy: **81.93%**
- XGBoost had lower overall origin-level loss in **89/131** origins.

HAC-adjusted two-sided p-values for XGBoost vs Chronos-2:

- 3M: `0.282459`
- 6M: `0.109399`
- 12M: `0.002677`
- Overall: `0.015592`

These results are historical validation, not a guarantee of future performance. See [Validation](docs/VALIDATION.md).

## Live market snapshot

Live reports can use a separate provider-agnostic current snapshot so yesterday's daily close is not silently treated as today's current price. In strict live mode, stale or missing snapshots stop the run. The HTML also shows the exact live Gold18, USD/IRR and XAU/USD inputs and optional quote times. See [Live snapshot input](docs/LIVE_DATA.md).

## Live scorecard

Every live forecast can be stored permanently. When a forecast matures after 63, 126, or 252 trading sessions, Gold4Cast can compare the original forecast with the realized market price and report:

- absolute percentage error,
- direction accuracy,
- whether realized price fell inside the Q10–Q90 interval,
- recent forecast-vs-actual results.

This makes the system auditable in real use, not only through backtesting.

## Data

**No proprietary or third-party historical dataset is distributed with the public repository.**

Users are responsible for supplying market data they are legally permitted to access and use. Data-provider integrations should respect the relevant provider's terms, licensing, rate limits, and applicable law.

Recommended normalized schema:

```text
date,gold18_toman,usd_irr,xau_usd
2026-01-01,...
```

Contributions that add properly licensed public-data providers are welcome.

## Quick start

```bash
git clone https://github.com/bdlykhanbary-crypto/gold4cast.git
cd gold4cast
python -m pip install -r requirements.txt
```

Then provide a lawful normalized CSV and run the forecast pipeline:

```bash
export GOLD4CAST_DATA=/path/to/market_data.csv
python forecast_xgboost_live.py
```

See [Data input](docs/DATA.md).

For the maintainer's Termux workflow, the project may also expose:

```bash
gold4cast
```

## Repository structure

```text
.
├── forecast_xgboost_live.py
├── run_model.py
├── benchmark_common.py
├── scorecard_update.py
├── run_live_and_open.sh
├── .github/
│   └── workflows/
├── docs/
│   ├── MODEL_CARD.md
│   ├── MODEL_CARD_FA.md
│   ├── VALIDATION.md
│   └── VALIDATION_FA.md
├── README.md
├── README_FA.md
├── CONTRIBUTING.md
├── CONTRIBUTING_FA.md
├── ROADMAP.md
├── ROADMAP_FA.md
├── SECURITY.md
├── SECURITY_FA.md
├── CHANGELOG.md
└── LICENSE
```

## Model-selection history

Before proposing a replacement forecasting model, read [Model Selection History](docs/MODEL_SELECTION.md). It documents the existing TimesFM-3, Chronos-2, Moirai-2.0, and XGBoost benchmarks and the evidence required for a new model proposal.

## Contributing

Professional and research contributions are welcome. Please read:

- [Contributing guide](CONTRIBUTING.md)
- [راهنمای مشارکت فارسی](CONTRIBUTING_FA.md)
- [Roadmap](ROADMAP.md)
- [نقشه راه فارسی](ROADMAP_FA.md)

Please open an issue before major architectural changes so benchmark methodology remains reproducible.

## Responsible use

Gold4Cast is a forecasting and research tool. It is **not financial advice**, does not guarantee returns, and does not provide a guaranteed floor or target price. Market shocks, policy changes, FX movements, geopolitical events, data errors, and structural breaks can cause realized prices to fall far outside the displayed ranges.

## License

Apache License 2.0. See [LICENSE](LICENSE).

## Version

**Gold4Cast v1.0.3**
