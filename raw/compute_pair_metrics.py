import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from datetime import datetime


tickers = [
    # Actions
    'AAPL', 'MSFT', 'GOOG', 'META', 'AMZN', 'TSLA', 'JPM', 'NVDA', 'WMT',
    'BNP.PA', 'OR.PA', 'AIR.PA', 'MC.PA', 'SAN.PA',
    'BMW.DE', 'BAYN.DE', 'SAP.DE', 'DTE.DE',"AC.PA", "AI.PA", "AIR.PA",
    "MT.PA", "CS.PA", "BNP.PA", "EN.PA", "BVI.PA", "CAP.PA", "CA.PA", 
    "ACA.PA", "BN.PA", "DSY.PA", "EDEN.PA", "ENGI.PA", "EL.PA", "ERF.PA", 
    "RMS.PA", "KER.PA", "LR.PA", "OR.PA", "MC.PA", "ML.PA", "ORA.PA", "RI.PA", 
    "PUB.PA", "RNO.PA", "SAF.PA", "SGO.PA", "SAN.PA", "SU.PA", "GLE.PA", "STLAP.PA", 
    "STMPA.PA", "TEP.PA", "HO.PA", "TTE.PA", "URW.PA", "VIE.PA", "DG.PA",

    # ETF
    '^GSPC', '^DJI', '^NDX', '^FCHI', '^GDAXI',

    # Forex
    'EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCHF=X',

    # Commodities
    'GC=F', 'SI=F', 'CL=F', 'NG=F', 'ZC=F', 'ZW=F', "BZ=F"
]

start_date = "2022-01-01"
end_date   = datetime.today().strftime("%Y-%m-%d")


prices = pd.DataFrame()
valid_count = 0

for t in tickers:
    try:
        df = yf.download(
            t,
            start=start_date,
            end=end_date,
            progress=False,
            threads=False,
            auto_adjust=True   
        )
        
        if not df.empty and 'Close' in df.columns:
            df = df[['Close']].copy()
            df.columns = [t]           
            prices = prices.join(df, how='outer') if not prices.empty else df
            valid_count += 1
            print(f"✅ {t} OK ({len(df)} lignes)")
        else:
            print(f"⚠️ {t} ignoré (colonne 'Close' manquante ou vide)")

    except Exception as e:
        print(f"❌ {t} erreur : {e}")


prices = prices.dropna()
print(f"\n✔️ {valid_count} tickers valides / {len(prices)} jours d’historique après nettoyage")


if prices.empty or prices.shape[1] < 2:
    raise RuntimeError("Pas assez de séries valides pour tester la cointégration.")


pairs = [
    (a, b) for i, a in enumerate(prices.columns)
    for b in prices.columns[i + 1 :]
]


def test_cointegration(pairs, data):
    results = []
    for a, b in pairs:
        duo = data[[a, b]]
        if len(duo) < 50:     # au moins 50 obs.
            continue
        try:
            # Engle-Granger
            _, eg_pval, _ = coint(duo[a], duo[b])

            # Johansen – sélection du lag avec fallback
            try:
                lag = VAR(duo).select_order().selected_orders["aic"]
            except Exception:
                lag = 1

            cj = coint_johansen(duo, det_order=0, k_ar_diff=lag)
            trace_stat, trace_cv = cj.lr1, cj.cvt[:, 1]
            trace_sig = int(
                (trace_stat[0] > trace_cv[0]) and (trace_stat[1] > trace_cv[1])
            )

            results.append({
                "pair"      : f"{a}-{b}",
                "eg_pval"   : eg_pval,
                "eg_sig"    : int(eg_pval < 0.05),
                "trace_sig" : trace_sig,
                "lag"       : lag
            })

        except Exception as e:
            print(f"⚠️  Skip {a}-{b} : {e}")

    return pd.DataFrame(results)

results = test_cointegration(pairs, prices)


valid = (
    results[(results.eg_sig == 1) & (results.trace_sig == 1)]
    .sort_values("eg_pval")
    .reset_index(drop=True)
)


print(f"\n✅ {len(valid)} paires cointégrées trouvées :\n")
print(valid[["pair", "eg_pval", "eg_sig", "trace_sig", "lag"]].head(20))
