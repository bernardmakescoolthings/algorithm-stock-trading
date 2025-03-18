# Algorithmic Stock Trading System

A sophisticated algorithmic trading system that combines multiple strategies including LSTM neural networks, NLP analysis, and traditional technical analysis to make trading decisions. The system supports both live trading through Robinhood and backtesting capabilities.

## Features

- **Multiple Trading Strategies**:
  - LSTM-based price prediction
  - Natural Language Processing (NLP) for sentiment analysis
  - Popularity-based market sentiment analysis
  - Technical analysis with SMA crossover strategy

- **Trading Integration**:
  - Direct integration with Robinhood API
  - Real-time trading capabilities
  - Secure credential management

- **Backtesting Framework**:
  - Historical data analysis
  - Strategy performance evaluation
  - Visualization tools

## Prerequisites

- Python 3.x
- Robinhood account and API credentials
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/algorithm-stock-trading.git
cd algorithm-stock-trading
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Robinhood credentials:
   - Create a `.cred` file in the parent directory
   - Add your Robinhood username and password (space-separated)

## Project Structure

```
algorithm-stock-trading/
├── lstm/              # LSTM-based trading models
├── nlp/               # Natural Language Processing components
├── popularity/        # Popularity-based analysis
├── testRobinhood.py  # Robinhood API integration
├── backtest.py       # Backtesting framework
└── archive/          # Archived code and experiments
```

## Usage

### Live Trading

1. Ensure your Robinhood credentials are properly set up
2. Run the trading system:
```bash
python testRobinhood.py
```

### Backtesting

To test strategies on historical data:
```bash
python backtest.py
```

## Trading Strategies

### LSTM Strategy
- Uses Long Short-Term Memory neural networks
- Predicts future price movements based on historical data
- Located in the `lstm/` directory

### NLP Strategy
- Analyzes news and social media sentiment
- Generates trading signals based on market sentiment
- Located in the `nlp/` directory

### Popularity Strategy
- Tracks market popularity indicators
- Generates signals based on market trends
- Located in the `popularity/` directory

### Technical Analysis
- Implements SMA (Simple Moving Average) crossover strategy
- Located in `backtest.py`

## Security Note

- Never commit your `.cred` file to version control
- Keep your API credentials secure
- Use environment variables for sensitive information in production

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This trading system is for educational purposes only. Always do your own research and never risk money you cannot afford to lose. The creators of this system are not responsible for any financial losses incurred through its use.
