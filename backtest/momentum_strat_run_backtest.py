#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np
import vectorbt as vbt
import matplotlib.pyplot as plt

# ========== CONFIGURATION ==========
CSV_FOLDER    = Path(r"C:\Users\wille\Desktop\ARBITRAGE\statistical arbitrage\csv")
stoch_days    = 6
bars_per_day  = 24
stoch_w       = stoch_days * bars_per_day  # 144 bars
atr_w         = 20
capital_leg   = 1_000
fee, slip     = 0.0005, 0.0002
init_cash     = 10_000
freq          = "1h"
# ===================================

def true_range(h: pd.Series, l: pd.Series, c0: pd.Series) -> pd.Series:
    return np.maximum.reduce([
        h - l,
        (h - c0).abs(),
        (l - c0).abs()
    ])

def raw_stoch(s: pd.Series, w: int) -> pd.Series:
    low  = s.rolling(w).min()
    high = s.rolling(w).max()
    return 100 * (s - low) / (high - low)

results = []

# Discover all CSV pairs
for csv_path in CSV_FOLDER.glob("*_1h.csv"):
    name = csv_path.stem.rsplit("_", 1)[0]
    if "-" not in name:
        continue
    leg_a, leg_b = name.split("-", 1)
    print(f"\n=== Backtesting {leg_a}-{leg_b} ===")

    # Load CSV (skip 3 header lines)
    df = pd.read_csv(
        csv_path,
        skiprows=3,
        header=None,
        names=["Datetime", leg_a, leg_b],
        parse_dates=["Datetime"],
        index_col="Datetime"
    ).astype(float).dropna()
    if df.empty:
        print("No data, skipping.")
        continue

    # Compute ATR sizing on close-only
    prev = df.shift(1)
    tr = pd.DataFrame({
        leg_a: true_range(df[leg_a], df[leg_a], prev[leg_a]),
        leg_b: true_range(df[leg_b], df[leg_b], prev[leg_b])
    }, index=df.index)
    atr  = tr.rolling(atr_w).mean().dropna()
    size = (capital_leg / atr).reindex(df.index).ffill()

    # Compute raw stochastic momentum
    stA = raw_stoch(df[leg_a], stoch_w)
    stB = raw_stoch(df[leg_b], stoch_w)
    diff = (stA - stB).fillna(0)

    # Build signals
    long_entry  = diff < -20
    strong_is_A = stA > stB
    short_entry = (diff > 70) & (
        (strong_is_A & (stA > 90)) |
        (~strong_is_A & (stB > 90))
    )
    long_exit   = diff >= 0
    short_exit  = (diff <= 50) | (
        (strong_is_A & (stA <= 50)) |
        (~strong_is_A & (stB <= 50))
    )

    n_long  = int(long_entry.sum())
    n_short = int(short_entry.sum())
    print(f"  → Long entries:  {n_long}")
    print(f"  → Short entries: {n_short}")
    if n_long + n_short == 0:
        print("  ⚠️ No signals, skipping.")
        continue

    # Align on common index and drop NaNs
    common_idx = df.index.intersection(size.index)
    sig_idx = common_idx
    for s in (long_entry, long_exit, short_entry, short_exit):
        sig_idx = sig_idx.intersection(s.dropna().index)
    close = df.loc[sig_idx, [leg_a, leg_b]]
    sz    = size.loc[sig_idx]
    le    = long_entry.loc[sig_idx]
    lx    = long_exit.loc[sig_idx]
    se    = short_entry.loc[sig_idx]
    sx    = short_exit.loc[sig_idx]

    # Backtest with vectorbt
    pf = vbt.Portfolio.from_signals(
        close=close,
        entries=le, exits=lx,
        short_entries=se, short_exits=sx,
        size=sz,
        freq=freq,
        init_cash=init_cash,
        fees=fee,
        slippage=slip
    )

    # Skip if no executed trades
    n_trades = len(pf.trades.records_readable)
    if n_trades == 0:
        print("  ⚠️ No trades executed, skipping stats.")
        continue

    # Collect stats
    stats = pf.stats()
    print(stats)
    results.append({
        "pair":              f"{leg_a}-{leg_b}",
        "Total Return [%]":  stats.get("Total Return [%]",  np.nan),
        "Sharpe Ratio":      stats.get("Sharpe Ratio",      np.nan),
        "Max Drawdown [%]":  stats.get("Max Drawdown [%]",  np.nan),
        "Total Trades":      stats.get("Total Trades",      np.nan),
        "Win Rate [%]":      stats.get("Win Rate [%]",      np.nan),
    })

    # Plot equity curve
    eq = pf.value().sum(axis=1)
    plt.figure(figsize=(8, 3))
    eq.plot(title=f"Equity Curve — {leg_a}-{leg_b}")
    plt.tight_layout()
    plt.show()

# Summary of all pairs
if results:
    df_res = pd.DataFrame(results).set_index("pair")
    print("\n=== Summary Results ===")
    print(df_res)
else:
    print("No results to display.")
