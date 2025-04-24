# crypto-arbitrage
'''
Pair Trading (Statistical Arbitrage)
is a market-neutral trading strategy that involves simultaneously buying and selling two correlated assets
to profit from their price divergence. 
The idea is based on the assumption that the two assets have a long-term equilibrium relationship, 
and any significant deviation from this equilibrium is temporary.

The process typically involves:

Selecting Pairs: Identifying two assets with strong historical correlation or cointegration (e.g., stocks in the same sector or related cryptocurrencies like BTC and ETH).
Calculating the Spread: Monitoring the price difference (spread) between the two assets.
Trading the Divergence: When the spread widens significantly, you short the overvalued asset and go long on the undervalued asset, expecting the spread to revert to its mean.
Closing the Position: Once the spread normalizes, you close both positions to realize the profit.
This strategy relies on statistical models to identify pairs and assess deviations, aiming to exploit temporary inefficiencies while minimizing market risk.


_____________________________________________________________________________________
HOW TO IDENTIFY PAIRS
----------------------------------------------------------------------------------------

1 = A correlation higher than 0.8 (or lower than -0.8 if the relationship is inverse) is often considered strong.
between 0.4 et 0.7 short term relationship between two series

low standard deviation of the spread (indicating that the spread is stable around a mean)

EX :
Date	    A (Market A Price)	B (Market B Price)	C (Daily Diff A)	D (Daily Diff B)	E (Spread A - B)
2023-01-01	21000	            21100	            -	                -	                -100.00
2023-01-02	21100	            21050	            100.00	            -50.00	            50.00
2023-01-03	20950	            20900	            -150.00	            -150.00	            50.00
2023-01-04	21050	            21000	            100.00	            100.00	            50.00
2023-01-05	21200	            21250	            150.00	            250.00	            -50.00
2023-01-06	21300	            21350	            100.00	            100.00	            -50.00
2023-01-07	21150	            21200	            -150.00	            -150.00	            -50.00
2023-01-08	21250	            21280	            100.00	            80.00	            -30.00
2023-01-09	21350	            21370	            100.00	            90.00	            -20.00

idealy, the spread should have a high variance
need to calculate the variance of the spread column E with :

std = the standard deviation

variance of the spread = Std²(a,b) = Std²(a) + Std²(b) - 2*cov(a,b)

cov(a,b) =1/N * Σ (a(i) - avg(a)) * (b(i) - avg(b))
-------------------------------------------------------------------------------------
2 = high z-score ou t-test (indicating that the mean and distribution of prices in the two series are similar)

z-score = 95% confidence interval for z-score need to be out of [-1.96 and 1.96] to be significant

t-test = p-value < 0.05 (5% significance level) indicates that the mean difference between the two series is statistically significant.
-------------------------------------------------------------------------------------
3 = coinintegration approach (long terme trend)

easiest:
The Engle-Granger two-step method is a simpler test for cointegration, typically applied to two time series

more advanced:
The Johansen test is a more advanced method that allows for testing cointegration among multiple time series simultaneously.
It uses a Vector Autoregression (VAR) framework.

Engle-Granger: Best for simpler cases with two time series. Easier to implement but less robust.
Johansen: Used for multiple time series or when more complex relationships need to be analyzed. 
It is more robust and provides richer insights.

other methods who can be considerate :  
Distance approach, 
Time-series approach,
stochastic contro approach

_____________________________________________________________________________________
STRATEGIE 1

mean reversion strategy 
take the rolling 15 days difference standard deviation and form a + ou - 2.0 standard deviation band around the differences

BUY == buy A and sell B when the difference is below  the 15-days average minus 2.0 standard deviation.
EXIT == Exit when the current difference crosses aabove the average of the 15-days difference.

SELL == sell A and buy B when the difference is above the 15-days average plus 2.0 standard deviation.
EXIT == Exit when the current difference crosses below the average of the 15-days difference.

END
_____________________________________________________________________________________
STRATEGIE 2

The difference between two momentum Indicators 
using the 6_day raw stochastic (using RSI or MACD would given similar results)

1 ==  sell the stronger when one stock is overbought at 90 and the momentum difference is greater than 70,
or some other threshold. That argues the overbought stock will correct but does not say anything about the other leg of the pair.

EXIT == Exit when the overbought stock corrects to neutral or the momentum difference narrows to a neutral level.

2 == buy the weaker when the momentum difference is below -20 and sell when the difference is the opposite. 

EXIT == Exit when the difference crosses zero

END
_____________________________________________________________________________________
STRATEGIE 3

based on stochastic oscillator

stress indicator 

D(t) = the difference between stchastic(1) and stchastic(2) at time t

stress(t)= (D(t) - min(Di))/((max(Di) - min(Di))

for i = t-n, t-1 

BUY == buy (leg1) and sell (leg2) when stress(t) < 5. Exit when stress(t) >= 50

SELL == sell (leg1) and buy (leg2) when stress(t) >95 . Exit when stress(t) <= 50

!! The success of this technique depends on how strongly the market trends !!
Momentum indicators show price fluctuation over the calculation period, but in a very quiet market, the range of that fluctuation will be small to trade.
This can be fixed by loking at the average true range of the price range from the last momentum low and using a minimum volatility filter.

END.
_____________________________________________________________________________________
POSITION SIZING

Volatility Parity Position Sizing
calculate the ATR (generaly on 20 days) and divide the price of the same investment (ex 1000 usd) by the ATR 

Example : A = 5$, B= 25$ and ATR(A) = 0.25$ "low relative volatility" and ATR(B) = 1$ "higher relative volatility"

position : P(A)= 1000/0.25 = 4000 units of A and P(B) = 1000/1 = 1000 units of B

so the position size is 4 times larger for A than for B

END
_____________________________________________________________________________________

Sources : 
BOOKS:///
-Trading systems and methods by KAUFMAN

-Machine Learning for Algorithmic Trading by Stefan Jansen

GOOGLE SCHOLAR:///
-Opportunity detection and trade simulation system for arbitrage trading on the crypto market by Lukas Fankhauser, BA 



------------------------------------------------------------------------------------------------
⚠️ Avertissement :
Les stratégies de trading que vous partagez sur GitHub sont fournies uniquement à titre éducatif. Elles ne garantissent pas de gains et impliquent un risque de pertes financières. Avant d’utiliser ou d’investir, assurez-vous de bien comprendre leur fonctionnement, effectuez vos propres tests et n’engagez que des sommes que vous pouvez vous permettre de perdre.
