import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import os, json, time, random, pathlib, datetime as dt, math, warnings, re
from typing import List, Dict, Tuple, Optional
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

# Optional imports (robustness)
try:
    import yfinance as yf
except Exception:
    yf = None

try:
    from pandas_datareader import data as pdr
except Exception:
    pdr = None

try:
    from fredapi import Fred
except Exception:
    Fred = None

# Load environment variables
load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore")

# API keys and model setup
alphavantage_key = os.getenv("ALPHAVANTAGE_KEY", "")
fredapi_key = os.getenv("FREDAPI_KEY", "")
newsapi_key = os.getenv("NEWSAPI_KEY", "")
openai_key = os.getenv("OPENAI_API_KEY", "")
llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
repo = "https://github.com/DMulabegovic/Financial-Analysis-with-Agentic-AI.git"

# Plotting config
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Reproducibility
np.random.seed(42)
random.seed(42)

# Default ticker
ticker = 'AAPL'

# Memory directory
root = pathlib.Path('.').resolve()
memory_directory = root / "memory"
memory_directory.mkdir(exist_ok=True)

# Data source tracker
source_tracker = {"prices": None, "financials": None, "macro": None, "news": None, "llm": bool(openai_key)}

# Utility functions
def current_time(): 
    return dt.datetime.utcnow().isoformat()+"Z"

def source_counter(name, data_count):
    print(f"Source {name}: {data_count} entries")

# Plan info
print("Plan: Get prices, financials, news, and macro; then synthesize, evaluate, improve, and save to memory.\n")
print("Current Settings:\n")
print(f"Ticker: {ticker}")
print(f"Alpha Vantage: {'Present' if alphavantage_key else 'Missing'}")
print(f"Fred API: {'Present' if fredapi_key else 'Missing'}")
print(f"News API: {'Present' if newsapi_key else 'Missing'}")
print(f"LLM: {'Present' if openai_key else 'Missing'}\n")


from src.data_tools import get_prices, get_financials, get_news, get_macro
from src.nlp_routing import simple_sentiment, route_document_rule


prices = get_prices(ticker)
financials = get_financials(ticker)
macro = get_macro()
news = get_news(ticker)

# Display proof outputs
print("\n Data collection complete!\n")
print(f"Prices rows: {len(prices)} | Financials rows: {len(financials)} | Macro rows: {len(macro)} | News articles: {len(news)}")


print("\n Routing and Sentiment Demo:")
for article in news:
    route, reason = route_document_rule(article['title'] or '', article.get('content', ''))
    sentiment = simple_sentiment(article.get('content', ''))
    print(f"- {article['title'][:60]}... → route={route}, sentiment={sentiment}, reason={reason}")
