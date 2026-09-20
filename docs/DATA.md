# Data input

Gold4Cast public releases are data-provider agnostic. The repository does not
bundle a third-party historical market dataset and does not hard-code a
third-party market-data endpoint.

Supply a CSV you are legally permitted to use:

```text
date,gold18_toman,usd_irr,xau_usd
2026-01-01,....
```

Set its path before running:

```bash
export GOLD4CAST_DATA=/path/to/market_data.csv
python forecast_xgboost_live.py
```

For GitHub Actions, set the repository secret `GOLD4CAST_DATA_URL` to a URL
that you are authorized to access. The workflow downloads that CSV only for
the current run and uploads forecast artifacts; it does not commit market
data or scorecard history back to the repository.

Users are responsible for the provider's license, terms, rate limits, and
applicable law.
