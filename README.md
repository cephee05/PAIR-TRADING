**crypto-arbitrage/**
├── **docs/**
│   └── overview.md           # Théorie du pair trading, formules, sources
├── **data/**
│   ├── raw/                  # CSV bruts ou extraction des prix
│   └── processed/            # Séries temporelles nettoyées, spreads, z-scores
├── **notebooks/**
│   ├── 01_pair_selection.ipynb
│   ├── 02_strategy_backtest.ipynb
│   └── 03_walk_forward.ipynb
├── **src/**
│   ├── data_prep.py          # Chargement, nettoyage, calcul de spread
│   ├── stats_tests.py        # Corrélation, cointégration, z-score, variance
│   ├── **strategies/**
│   │   ├── mean_reversion.py
│   │   ├── momentum_pair.py
│   │   └── stochastic_stress.py
│   └── sizing.py             # Volatility parity position sizing
├── **backtest/**
│   ├── run_backtest.py
│   └── monte_carlo.py
├── **results/**              # Backtest outputs, equity curves, CSVs
├── **tests/**                # Tests unitaires pour chaque module src/
├── **benchmarks/**           # Tableaux de bord et graphiques de synthèse
├── requirements.txt
├── LICENSE
└── README.md

