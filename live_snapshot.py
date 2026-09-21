from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

DEFAULT_LIVE_PATH = Path(__file__).resolve().parent / "live_snapshot.csv"
REQUIRED_COLUMNS = ("date", "gold18_toman", "usd_irr", "xau_usd")
OPTIONAL_TIME_COLUMNS = ("gold_quote_time", "usd_quote_time", "xau_quote_time")


def _resolve_live_path() -> Path:
    configured = os.environ.get("GOLD4CAST_LIVE_SNAPSHOT", "").strip()
    path = Path(configured).expanduser() if configured else DEFAULT_LIVE_PATH
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def overlay_live_snapshot(market: pd.DataFrame, meta: dict, require_live: bool = False):
    """Overlay a provider-agnostic current market snapshot onto historical data."""
    path = _resolve_live_path()

    if not path.exists():
        if require_live:
            raise FileNotFoundError(
                "Live snapshot required but not found. Set GOLD4CAST_LIVE_SNAPSHOT "
                "to a normalized CSV containing date,gold18_toman,usd_irr,xau_usd."
            )
        return market, dict(meta or {})

    raw = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError("Missing live-snapshot columns: " + ", ".join(missing))
    if raw.empty:
        raise ValueError("Live snapshot CSV is empty.")

    row = raw.iloc[-1].copy()
    live_date = pd.to_datetime(row["date"], errors="coerce")
    if pd.isna(live_date):
        raise ValueError("Live snapshot date is invalid.")

    values = {}
    for col in ("gold18_toman", "usd_irr", "xau_usd"):
        value = pd.to_numeric(pd.Series([row[col]]), errors="coerce").iloc[0]
        if pd.isna(value) or not np.isfinite(float(value)) or float(value) <= 0:
            raise ValueError(f"Invalid live snapshot value for {col}: {row[col]!r}")
        values[col] = float(value)

    if require_live:
        today_tehran = pd.Timestamp(datetime.now(ZoneInfo("Asia/Tehran")).date())
        if pd.Timestamp(live_date).normalize() != today_tehran:
            raise RuntimeError(
                f"Stale live snapshot: got {pd.Timestamp(live_date).date()}, "
                f"expected {today_tehran.date()}."
            )

    out = market.copy()
    snapshot_date = pd.Timestamp(live_date).normalize()

    new_row = {
        "date": snapshot_date,
        "gold18_toman": values["gold18_toman"],
        "usd_irr": values["usd_irr"],
        "xau_usd": values["xau_usd"],
        "price_toman": values["gold18_toman"],
        "gold_close_irr": values["gold18_toman"] * 10.0,
        "usd_close_irr": values["usd_irr"],
        "xau_close_usd": values["xau_usd"],
        "log_gold": np.log(values["gold18_toman"]),
        "log_usd": np.log(values["usd_irr"]),
        "log_xau": np.log(values["xau_usd"]),
        "log_price": np.log(values["gold18_toman"]),
    }

    if len(out) and pd.Timestamp(out["date"].iloc[-1]).normalize() == snapshot_date:
        idx = out.index[-1]
        for key, value in new_row.items():
            out.loc[idx, key] = value
    else:
        out = pd.concat([out, pd.DataFrame([new_row])], ignore_index=True)

    out = out.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)

    quote_times = {}
    for col in OPTIONAL_TIME_COLUMNS:
        value = row.get(col, None)
        quote_times[col] = None if pd.isna(value) else str(value)

    meta2 = dict(meta or {})
    meta2["live_snapshot"] = {
        "source": "user-supplied normalized live snapshot",
        "file": str(path),
        "date": str(snapshot_date.date()),
        "gold18_toman": values["gold18_toman"],
        "usd_irr": values["usd_irr"],
        "xau_usd": values["xau_usd"],
        **quote_times,
    }
    meta2["aligned_to"] = str(snapshot_date.date())

    print(
        "LIVE_SNAPSHOT",
        f"gold18_toman={values['gold18_toman']:.0f}",
        f"usd_irr={values['usd_irr']:.0f}",
        f"xau_usd={values['xau_usd']:.2f}",
        f"date={snapshot_date.date()}",
        f"gold_time={quote_times['gold_quote_time'] or 'unknown'}",
        f"usd_time={quote_times['usd_quote_time'] or 'unknown'}",
        f"xau_time={quote_times['xau_quote_time'] or 'unknown'}",
        flush=True,
    )

    return out, meta2
