#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np
import vectorbt as vbt
import matplotlib.pyplot as plt

# ========== CONFIG ==========
CSV_FOLDER        = Path(r"C:\Users\wille\Desktop\ARBITRAGE\statistical arbitrage\csv")
capital_leg       = 1_000
window_atr        = 20           # ATR lookback (bars)
window_mr_days    = 15           # mean‐reversion window (days)
bars_per_day      = 24
window_mr         = window_mr_days * bars_per_day
z_thresh          = 2.0          # seuil en σ
init_cash         = 100_000
fees              = 0.0005
slippage          = 0.0002
freq              = "1h"
# ===================================

def true_range(h: pd.Series, l: pd.Series, c_prev: pd.Series) -> pd.Series:
    return np.maximum.reduce([
        h - l,
        (h - c_prev).abs(),
        (l - c_prev).abs()
    ])

# 1) Repérer toutes les paires
pairs = []
for f in CSV_FOLDER.glob("*_1h.csv"):
    name = f.stem.rsplit("_", 1)[0]
    if "-" in name:
        pairs.append(tuple(name.split("-", 1)))

results = []

for a, b in pairs:
    print(f"\n=== Backtest {a} vs {b} ===")
    csv_path = CSV_FOLDER / f"{a}-{b}_1h.csv"

    # 2) Lecture CSV (skip 3 header lines)
    df = pd.read_csv(
        csv_path,
        skiprows=3,
        header=None,
        names=["Datetime", a, b],
        parse_dates=["Datetime"],
        index_col="Datetime"
    ).astype(float).dropna()
    if df.empty:
        print("No data, skipping.")
        continue

    # 3) Calcul ATR(20) sur close-only
    prev = df.shift(1)
    tr = pd.DataFrame({
        a: true_range(df[a], df[a], prev[a]),
        b: true_range(df[b], df[b], prev[b])
    }, index=df.index)
    atr = tr.rolling(window_atr).mean().dropna()

    # 4) Volatility parity sizing
    size = (capital_leg / atr).reindex(df.index).ffill()

    # 5) Align index avant stats
    idx0 = df.index.intersection(size.index)
    prices = df.loc[idx0, [a, b]]
    sz     = size.loc[idx0]

    # 6) Spread, moyenne et écart‐type roulants
    spread = prices[a] - prices[b]
    m      = spread.rolling(window_mr).mean()
    s      = spread.rolling(window_mr).std()

    # 7) Drop NaN initiaux
    idx = idx0.intersection(m.dropna().index).intersection(s.dropna().index)
    prices = prices.loc[idx]
    sz     = sz.loc[idx]
    spread = spread.loc[idx]
    m      = m.loc[idx]
    s      = s.loc[idx]

    # 8) Séries de signaux (Series)
    le = spread <  (m - z_thresh * s)   # long entry
    lx = spread >= m                    # exit longs
    se = spread >  (m + z_thresh * s)   # short entry
    sx = spread <= m                    # exit shorts

    print(f"  signals → Longs: {int(le.sum())}, Shorts: {int(se.sum())}")
    if le.sum() + se.sum() == 0:
        print("  ⚠️ Aucun signal, on skip.")
        continue

    # 9) Construire 4 DataFrames pour VectorBT
    cols = [a, b]
    entries       = pd.DataFrame(False, index=idx, columns=cols)
    exits         = entries.copy()
    short_entries = entries.copy()
    short_exits   = entries.copy()

    # Long trade  = buy A / sell B
    entries[a]       = le
    short_entries[b] = le
    exits[a]         = lx
    short_exits[b]   = lx

    # Short trade = sell A / buy B
    short_entries[a] = se
    entries[b]       = se
    short_exits[a]   = sx
    exits[b]         = sx

    # 10) Backtest VectorBT
    pf = vbt.Portfolio.from_signals(
        close=prices,
        entries=entries, exits=exits,
        short_entries=short_entries, short_exits=short_exits,
        size=sz,
        init_cash=init_cash,
        fees=fees,
        slippage=slippage,
        freq=freq
    )

    # 11) Stats et équité
    n_trades = len(pf.trades.records_readable)
    print(f"  Trades exécutés: {n_trades}")
    if n_trades == 0:
        print("  ⚠️ Aucun trade, skip stats.")
        continue

    stats = pf.stats()
    print(stats)

    results.append({
        "pair":              f"{a}-{b}",
        "Total Return [%]":  stats["Total Return [%]"],
        "Sharpe Ratio":      stats["Sharpe Ratio"],
        "Max Drawdown [%]":  stats["Max Drawdown [%]"],
        "Total Trades":      stats["Total Trades"],
        "Win Rate [%]":      stats["Win Rate [%]"],
    })

    # Équity curve
    eq = pf.value().sum(axis=1)
    plt.figure(figsize=(8, 3))
    eq.plot(title=f"Equity Curve {a}-{b}")
    plt.tight_layout()
    plt.show()

# 12) Résumé final
if results:
    df_res = pd.DataFrame(results).set_index("pair")
    print("\n=== Résumé global ===")
    print(df_res)
else:
    print("Aucun résultat à afficher.")
