from __future__ import annotations

import json
import math
import os
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

HORIZONS = {63: "3M", 126: "6M", 252: "12M"}
MAX_H = 252
FOUNDATION_CONTEXT = 512
XGB_LAGS = 63
QUANTILES = [0.1, 0.5, 0.9]

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "market_data.csv"

REQUIRED_MARKET_COLUMNS = ("date", "gold18_toman", "usd_irr", "xau_usd")


def _resolve_market_data_path() -> Path:
    configured = os.environ.get("GOLD4CAST_DATA", "").strip()
    path = Path(configured).expanduser() if configured else DATA_PATH
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def load_market_data(refresh=True):
    # Public Gold4Cast uses a provider-agnostic normalized CSV.
    # Required columns: date,gold18_toman,usd_irr,xau_usd
    # refresh is retained for API compatibility.
    path = _resolve_market_data_path()
    if not path.exists():
        raise FileNotFoundError(
            "Market data not found. Set GOLD4CAST_DATA to a normalized CSV "
            "containing: date,gold18_toman,usd_irr,xau_usd"
        )

    raw = pd.read_csv(path)
    missing = [c for c in REQUIRED_MARKET_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(
            "Missing required market-data columns: " + ", ".join(missing)
        )

    market = raw.loc[:, list(REQUIRED_MARKET_COLUMNS)].copy()
    market["date"] = pd.to_datetime(market["date"], errors="coerce")

    for col in ("gold18_toman", "usd_irr", "xau_usd"):
        market[col] = pd.to_numeric(market[col], errors="coerce")

    market = (
        market.dropna(subset=list(REQUIRED_MARKET_COLUMNS))
        .sort_values("date")
        .drop_duplicates("date", keep="last")
        .reset_index(drop=True)
    )

    if market.empty:
        raise ValueError("Normalized market dataset contains no valid rows.")

    positive_cols = ["gold18_toman", "usd_irr", "xau_usd"]
    market = market[(market[positive_cols] > 0).all(axis=1)].reset_index(drop=True)
    if market.empty:
        raise ValueError("Market prices must be positive.")

    market["price_toman"] = market["gold18_toman"].astype(float)
    market["gold_close_irr"] = market["price_toman"] * 10.0
    market["usd_close_irr"] = market["usd_irr"].astype(float)
    market["xau_close_usd"] = market["xau_usd"].astype(float)

    market["log_gold"] = np.log(market["price_toman"])
    market["log_usd"] = np.log(market["usd_close_irr"])
    market["log_xau"] = np.log(market["xau_close_usd"])
    market["log_price"] = market["log_gold"]

    meta = {
        "source": {"market_csv": str(path)},
        "notes": [
            "Provider-agnostic public loader; user is responsible for lawful data access.",
            "Input rows are sorted by date and duplicate dates keep the last observation.",
        ],
        "aligned_rows": int(len(market)),
        "aligned_from": str(market.date.min().date()),
        "aligned_to": str(market.date.max().date()),
        "alignment": "user-supplied normalized common calendar",
        "inputs": [
            "Gold18 price in toman",
            "USD/IRR",
            "XAU/USD",
        ],
    }
    return market, meta


def benchmark_origins(n: int):
    origins = []
    o = n - MAX_H
    floor = max(FOUNDATION_CONTEXT, XGB_LAGS + MAX_H + 128)
    while o >= floor:
        origins.append(o)
        o -= 21
    origins = sorted(origins)
    if len(origins) < 20:
        raise RuntimeError(f"Too few dense walk-forward origins: {len(origins)}")
    return origins


def to_row(gold, model, origin, h, q10_log, q50_log, q90_log):
    actual_log = float(gold.log_price.iloc[origin + h - 1])
    current_log = float(gold.log_price.iloc[origin - 1])
    vals = sorted([float(q10_log), float(q50_log), float(q90_log)])
    q10_log, q50_log, q90_log = vals
    return {
        "model": model,
        "origin_index": int(origin),
        "origin_date": str(gold.date.iloc[origin - 1].date()),
        "horizon": int(h),
        "label": HORIZONS[h],
        "current_price": float(math.exp(current_log)),
        "actual_price": float(math.exp(actual_log)),
        "actual_log": actual_log,
        "q10_log": q10_log,
        "q50_log": q50_log,
        "q90_log": q90_log,
        "q10_price": float(math.exp(q10_log)),
        "q50_price": float(math.exp(q50_log)),
        "q90_price": float(math.exp(q90_log)),
    }


def pinball(y, qhat, q):
    e = y - qhat
    return max(q * e, (q - 1) * e)


def summarize_results(df):
    rows = []
    if df is None or len(df) == 0:
        return pd.DataFrame()
    for (model, h), g in df.groupby(["model", "horizon"]):
        qloss = np.mean(
            [
                (
                    pinball(r.actual_log, r.q10_log, 0.1)
                    + pinball(r.actual_log, r.q50_log, 0.5)
                    + pinball(r.actual_log, r.q90_log, 0.9)
                ) / 3
                for r in g.itertuples()
            ]
        )
        mape = np.mean(np.abs(g["q50_price"] / g["actual_price"] - 1)) * 100
        cov = np.mean(
            (g["actual_price"] >= g["q10_price"]) & (g["actual_price"] <= g["q90_price"])
        ) * 100
        diracc = np.mean(
            np.sign(g["q50_price"] / g["current_price"] - 1)
            == np.sign(g["actual_price"] / g["current_price"] - 1)
        ) * 100
        rows.append(
            {
                "model": model,
                "horizon": int(h),
                "label": HORIZONS[int(h)],
                "n": int(len(g)),
                "mean_pinball": float(qloss),
                "median_mape_pct": float(mape),
                "coverage80_pct": float(cov),
                "direction_accuracy_pct": float(diracc),
            }
        )
    out = pd.DataFrame(rows)
    out["rank_pinball"] = out.groupby("horizon")["mean_pinball"].rank(method="min")
    return out.sort_values(["horizon", "mean_pinball"])


def save_status(path: Path, **kwargs):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, ensure_ascii=False, indent=2), encoding="utf-8")
