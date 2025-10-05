import os
import pandas as pd
import requests
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv()
ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")
FRED_KEY = os.getenv("FREDAPI_KEY")
NEWS_KEY = os.getenv("NEWSAPI_KEY")

def get_prices(ticker, period="1y", interval="1d"):
    """Fetch Adjusted Close or Close prices from yfinance → Alpha Vantage → Stooq."""
    print(f"[TOOL] prices[{ticker}] attempting yfinance...")
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        # ✅ Handle both Adj Close and Close
        if "Adj Close" in df.columns:
            df = df[["Adj Close"]].rename(columns={"Adj Close": "adj_close"})
        elif "Close" in df.columns:
            df = df[["Close"]].rename(columns={"Close": "adj_close"})
        else:
            raise KeyError("No price column found")
        print(f"[TOOL] source=yfinance → rows={len(df)}")
        return df
    except Exception as e:
        print(f"yfinance failed: {e}")

    print(f"[TOOL] fallback → Alpha Vantage (free endpoint)")
    try:
        ts = TimeSeries(key=ALPHAVANTAGE_KEY, output_format="pandas")
        data, _ = ts.get_daily(symbol=ticker, outputsize="compact")  # ✅ free version
        df = data[["4. close"]].rename(columns={"4. close": "adj_close"})
        print(f"[TOOL] source=alphavantage (free) → rows={len(df)}")
        return df
    except Exception as e:
        print(f"Alpha Vantage failed: {e}")

    print(f"[TOOL] fallback → Stooq")
    try:
        import pandas_datareader.data as web
        df = web.DataReader(f"{ticker}.US", "stooq")
        df = df[["Close"]].rename(columns={"Close": "adj_close"})
        print(f"[TOOL] source=stooq → rows={len(df)}")
        return df
    except Exception as e:
        print(f"Stooq failed: {e}")
        print("💡 Hint: run 'pip install pandas-datareader setuptools'")

    raise RuntimeError("All price sources failed!")

def get_financials(ticker):
    """Fetch fundamentals via Alpha Vantage."""
    print(f"[TOOL] financials[{ticker}] attempting alphavantage...")
    fd = FundamentalData(key=ALPHAVANTAGE_KEY, output_format='pandas')
    data, _ = fd.get_income_statement_annual(ticker)
    df = data.head(4)[['fiscalDateEnding', 'totalRevenue', 'grossProfit']]
    df['revenue_bil'] = df['totalRevenue'].astype(float) / 1e9
    df['ttm_margin'] = (df['grossProfit'].astype(float) / df['totalRevenue'].astype(float)).rolling(2).mean()
    df = df.set_index('fiscalDateEnding')
    print(f"[TOOL] financials[alphavantage] → rows={len(df)}")
    return df

def get_news(ticker, n=8):
    """Fetch recent news from NewsAPI"""
    print(f"[TOOL] news[{ticker}] attempting NewsAPI...")
    key = os.getenv("NEWSAPI_KEY", "")
    if not key or len(key) < 10:
        print("❌ Missing or invalid NEWSAPI_KEY. Set it in .env.")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": n,
        "apiKey": key,
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise RuntimeError(f"NewsAPI failed: {r.status_code} → {r.text}")

    articles = r.json().get("articles", [])
    docs = [
        {
            "title": a["title"],
            "content": a.get("description", "") or a.get("content", ""),
            "published": a.get("publishedAt", ""),
            "source": a["source"]["name"],
        }
        for a in articles
    ]
    print(f"[TOOL] news[newsapi] → articles={len(docs)}")
    return docs


def get_macro(series_id="CPIAUCSL", start="2019-01-01"):
    """Fetch macroeconomic data from FRED."""
    print(f"[TOOL] macro[{series_id}] attempting FRED...")
    try:
        fred = Fred(api_key=os.getenv("FREDAPI_KEY"))
        data = fred.get_series(series_id)
        df = pd.DataFrame(data, columns=[series_id])
        df.index = pd.to_datetime(df.index)
        print(f"[TOOL] macro[fred] → rows={len(df)}")
        return df
    except ValueError as e:
        print(f" Invalid FRED API key: {e}")
        print("Fix: Check .env → FREDAPI_KEY must be 32 characters, lowercase.")
    except Exception as e:
        print(f"FRED failed: {e}")

    return pd.DataFrame()  # fail-safe

