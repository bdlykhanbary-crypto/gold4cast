# Live snapshot input

Gold4Cast separates **historical training/context data** from the **current live market snapshot**.

A daily-history feed can lag during the trading day. Without a separate live snapshot, yesterday's close may be mistaken for today's current price. Gold4Cast v1.0.3 adds a provider-agnostic live-input layer to prevent that.

## Public, provider-agnostic design

The public repository does not hard-code a named market-data provider. Users supply:

1. historical normalized CSV through `GOLD4CAST_DATA`;
2. current normalized snapshot CSV through `GOLD4CAST_LIVE_SNAPSHOT`.

Required live-snapshot columns:

```text
date,gold18_toman,usd_irr,xau_usd
2026-09-21,23859100,2313400,4355.49
```

Optional quote-time columns:

```text
gold_quote_time,usd_quote_time,xau_quote_time
13:08:34,13:08:40,13:08:34
```

## Fail-closed live mode

When `GOLD4CAST_REQUIRE_LIVE=1`, Gold4Cast refuses to publish a live report if:

- the snapshot file is missing;
- required columns are missing;
- a price is invalid or non-positive;
- the snapshot date is not today's date in `Asia/Tehran`.

This prevents a stale closing price from being silently presented as a live input.

## Forecast behavior

The model still uses the full historical dataset. The current snapshot only replaces or appends the final observation immediately before the XGBoost forecast is generated.

```text
historical Gold18 + USD/IRR + XAU/USD
                  +
current normalized live snapshot
                  ↓
          XGBoost Quantile
                  ↓
        3M / 6M / 12M forecasts
```

The HTML report displays the exact live values used by that run and, when supplied, the quote time for Gold18, USD/IRR and XAU/USD.

## GitHub Actions

For the public workflow, configure both repository secrets:

- `GOLD4CAST_DATA_URL`
- `GOLD4CAST_LIVE_SNAPSHOT_URL`

The URLs must point to data that the user is authorized to access and use.
