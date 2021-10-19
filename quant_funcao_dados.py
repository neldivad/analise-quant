import yfinance as yf

def precos(ticker, periodo, pct):
    if pct == True:
        df = yf.download(ticker, period = periodo, progress=False)['Adj Close'].pct_change()
    else:
        df = yf.download(ticker, period=periodo, progress=False)['Adj Close']
    return df