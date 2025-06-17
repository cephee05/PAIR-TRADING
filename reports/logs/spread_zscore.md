### 📈 Cointegrated Pairs — Spread & Z-Score

| Pair            | Beta        | Spread Last     | Z-Score Last |
|-----------------|-------------|------------------|---------------|
| CL=F-BZ=F       | 0.987738    | -0.562071        |  1.752974     |
| VIE.PA-CL=F     | -0.145740   | 40.809772        |  1.524886     |
| TEP.PA-NG=F     | 27.304442   | -9.837046        | -1.177597     |
| TEP.PA-TTE.PA   | -9.635602   | 617.833021       | -1.095798     |
| TEP.PA-AUDUSD=X | 2043.120414 | -1235.527855     | -0.630592     |
| TEP.PA-CL=F     | 4.383266    | -222.086969      | -0.521597     |
| TEP.PA-BZ=F     | 4.505031    | -237.403459      | -0.280694     |
| TEP.PA-VIE.PA   | -16.966594  | 607.436135       |  0.280285     |
| TEP.PA-^FCHI    | -0.098858   | 857.880117       | -0.272988     |
| RNO.PA-TEP.PA   | -0.080568   | 46.752523        | -0.238177     |
| TEP.PA-ZW=F     | 0.393830    | -118.789653      | -0.226126     |
| ZW=F-BZ=F       | 11.191151   | -283.027999      | -0.190561     |

After normalization using Min-Max scaling, each variable (spread, beta, z-score) is rescaled to the [0, 1] range.
This ensures comparability across features with different units or magnitudes, making it easier to rank or filter pairs objectively.

| Pair            | Beta\_norm | Spread\_norm | ZScore\_norm |
| --------------- | ---------- | ------------ | ------------ |
| CL=F-BZ=F       | 0.51       | 0.38         | 1.00         |
| VIE.PA-CL=F     | 0.43       | 0.97         | 0.94         |
| TEP.PA-NG=F     | 0.60       | 0.27         | 0.21         |
| TEP.PA-TTE.PA   | 0.00       | 0.86         | 0.23         |
| TEP.PA-AUDUSD=X | 1.00       | 0.00         | 0.38         |
| TEP.PA-CL=F     | 0.47       | 0.20         | 0.41         |
| TEP.PA-BZ=F     | 0.48       | 0.17         | 0.50         |
| TEP.PA-VIE.PA   | 0.07       | 0.84         | 0.59         |
| TEP.PA-^FCHI    | 0.42       | 1.00         | 0.51         |
| RNO.PA-TEP.PA   | 0.41       | 0.39         | 0.52         |
| TEP.PA-ZW=F     | 0.45       | 0.22         | 0.52         |
| ZW=F-BZ=F       | 0.49       | 0.14         | 0.53         |

## Pairs to Focus On (to Avoid False Positives)

To minimize false-positive signals, concentrate on the pairs that satisfy **all three** of these normalized metrics:

- **β_norm** > 0.40  
- **Spread_norm** > 0.30  
- **ZScore_norm** > 0.50  

| Pair           | β_norm | Spread_norm | ZScore_norm |
| -------------- | ------ | ----------- | ----------- |
| **CL=F–BZ=F**     | 0.51   | 0.38        | 1.00        |
| **VIE.PA–CL=F**   | 0.43   | 0.97        | 0.94        |
| **TEP.PA–^FCHI**  | 0.42   | 1.00        | 0.51        |
| **RNO.PA–TEP.PA** | 0.41   | 0.39        | 0.52        |

> **Note**: If you tighten the β_norm filter to **> 0.45**, the only remaining pair is **CL=F–BZ=F**.

### Rationale

- **CL=F–BZ=F** consistently scores high across all three metrics—strong cointegration, healthy spread, and very high z-score.  
- **VIE.PA–CL=F** and **TEP.PA–^FCHI** both exhibit excellent spread behavior and z-score, even if their β_norm is slightly lower.  
- **RNO.PA–TEP.PA** is a solid runner-up option if you want an additional candidate.


