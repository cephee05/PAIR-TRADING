import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime


selected_pairs = [
    "TEP.PA-^FCHI",
    "TEP.PA-ZW=F",
    "TEP.PA-TTE.PA",
    "TEP.PA-AUDUSD=X",
    "TEP.PA-VIE.PA",
    "TEP.PA-NG=F",
    "TEP.PA-CL=F",
    "TEP.PA-BZ=F",
    "CL=F-BZ=F",
    "VIE.PA-CL=F",
    "ZW=F-BZ=F",
    "RNO.PA-TEP.PA"
]

start_date = "2022-01-01"
end_date   = datetime.today().strftime("%Y-%m-%d")


unique_tickers = sorted({t for pair in selected_pairs for t in pair.split('-')})
prices = yf.download(
    unique_tickers,
    start=start_date,
    end=end_date,
    progress=False,
    threads=False,
    auto_adjust=True
)['Close'].dropna()


def compute_spread_zscore(series_a: pd.Series, series_b: pd.Series):
    beta = np.polyfit(series_b, series_a, 1)[0]
    spread = series_a - beta * series_b
    zscore = (spread - spread.mean()) / spread.std()
    return beta, spread.iloc[-1], zscore.iloc[-1]


rows = []
for pair in selected_pairs:
    a, b = pair.split('-')
    df_pair = prices[[a, b]].dropna()
    if len(df_pair) < 50:
        print(f"⚠️ {pair} ignorée (moins de 50 observations communes)")
        continue
    beta, spread_last, zscore_last = compute_spread_zscore(df_pair[a], df_pair[b])
    rows.append({
        'pair': pair,
        'beta': beta,
        'spread_last': spread_last,
        'zscore_last': zscore_last
    })

spread_df = pd.DataFrame(rows).sort_values('zscore_last', key=abs, ascending=False)
print("\n📊 Spread & z-score :")
print(spread_df)
