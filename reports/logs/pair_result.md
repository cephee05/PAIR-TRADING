| #  | Pair                | EG p-value | EG ✔ | Johansen ✔ | Optimal Lag |
| -- | ------------------- | ---------- | ---- | ---------- | ----------- |
| 1  | `TEP.PA - ^FCHI`    | 0.0071     | ✅    | ✅          | 1           |
| 2  | `TEP.PA - ZW=F`     | 0.0088     | ✅    | ✅          | 5           |
| 3  | `TEP.PA - TTE.PA`   | 0.0112     | ✅    | ✅          | 1           |
| 4  | `TEP.PA - AUDUSD=X` | 0.0137     | ✅    | ✅          | 2           |
| 5  | `TEP.PA - VIE.PA`   | 0.0139     | ✅    | ✅          | 2           |
| 6  | `TEP.PA - NG=F`     | 0.0202     | ✅    | ✅          | 1           |
| 7  | `TEP.PA - CL=F`     | 0.0231     | ✅    | ✅          | 1           |
| 8  | `TEP.PA - BZ=F`     | 0.0232     | ✅    | ✅          | 1           |
| 9  | `CL=F - BZ=F`       | 0.0349     | ✅    | ✅          | 2           |
| 10 | `VIE.PA - CL=F`     | 0.0386     | ✅    | ✅          | 2           |
| 11 | `ZW=F - BZ=F`       | 0.0412     | ✅    | ✅          | 1           |
| 12 | `RNO.PA - TEP.PA`   | 0.0470     | ✅    | ✅          | 2           |

From a macro perspective, these three cointegrated pairs each reflect distinct but interrelated economic dynamics:

1. **TEP.PA – ^FCHI (Technip Energies vs. CAC 40)**

   * **Context:** Technip Energies is a leading engineering and services firm in oil and gas, listed in Paris. The CAC 40 (^FCHI) is France’s benchmark equity index.
   * **Macro Insight:** Their tight linkage indicates that Technip Energies behaves very much like a “market proxy” for the broader French equity cycle. When risk appetite in European markets rises—driven by ECB accommodative policy or global growth optimism—both the CAC 40 and Technip tend to rally together. Conversely, in downturns or volatility spikes, Technip’s project backlog and revenues contract in step with the wider market.

2. **TEP.PA – ZW=F (Technip Energies vs. Chicago Wheat Futures)**

   * **Context:** ZW=F is the benchmark wheat futures contract on the CBOT.
   * **Macro Insight:** At first glance, oil-field engineering and agricultural commodities may seem unrelated. In reality, both are tied to energy and logistics costs. Wheat prices often rise alongside other commodity prices under global demand surges or supply disruptions (e.g. extreme weather). Those same pressures typically boost oil and gas prices, improving margins for energy-services providers like Technip. Their cointegration thus captures a common “inflation pulse” in basic commodities—energy and food—driven by macro shocks.

3. **TEP.PA – TTE.PA (Technip Energies vs. TotalEnergies)**

   * **Context:** TTE.PA is the ticker for TotalEnergies, one of the world’s largest integrated oil and gas majors.
   * **Macro Insight:** This pair is the most intuitive: both companies operate across upstream production, refining, and mid-stream services, and are subject to the same global oil-price cycles (OPEC decisions, geopolitical tensions), regulatory regimes, and transition-energy trends. Their cointegration confirms that, on broad energy-sector shocks, they move practically in lockstep.

---

**Key takeaways for a pairs-trading strategy:**

* **Monetary & Market Cycle Exposure:** The TEP vs. CAC 40 relationship lets you trade Technip’s relative performance when European risk sentiment shifts (e.g. ECB rate decisions).
* **Commodity-Inflation Link:** The TEP vs. Wheat futures spread captures macro shocks to raw-material costs and global supply chain stress—useful when real-economy inflation surprises occur.
* **Sector-Specific Hedging:** The TEP vs. TotalEnergies pair provides a pure energy-sector trade, isolating idiosyncratic moves (e.g. company-specific news) from broad oil-price trends.

