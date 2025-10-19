Financial Analysis with Agentic AI

This project implements an agentic AI system that performs end to end financial analysis using live data sources. It plans, executes, summarizes, evaluates, improves, and replans, creating a self adapting analysis loop.

  
Setup Instructions

Requirements:

* Python 3.9+
* Jupyter Notebook

Install required libraries:

pip install numpy pandas matplotlib requests yfinance pandas_datareader fredapi python-dotenv


  

API Keys (.env Setup):

Create a file named .env in the project’s root folder (same directory as the notebook).
Add your API keys as shown below:

ALPHAVANTAGE_KEY=your_alpha_vantage_key

FREDAPI_KEY=your_fred_key

NEWSAPI_KEY=your_newsapi_key

OPENAI_API_KEY=your_openai_key

LLM_MODEL=gpt-4



  
Running the Notebook

1. Open the Jupyter Notebook:
Financial Analysis with Agentic AI.ipynb
2. Run all cells. The system will:
* Build a plan (Plan 1) using the LLM planner.
* Execute the steps (fetch, summarize, evaluate, visualize, and store memory).
* Generate feedback.
* Replan a second iteration (Plan 2) using that feedback.
* Produce all visuals, summaries, and evaluation results.


  

Outputs

* DataFrames: Prices, financials, macro (CPI), and news
* Briefs: Rule based and LLM based summaries (v1 → v2)
* Visuals: Moving averages, RSI, volatility, drawdown, macro trend, sentiment
* Memory: JSONL entries stored per ticker
* Feedback Loop: Plan 2 adapts from Plan 1 results


  

Summary

This notebook demonstrates a complete agentic loop:

Plan → Act with tools → Summarize → Critique → Improve → Remember → Replan.

It integrates multiple data sources and AI-driven reasoning to autonomously improve its analysis with each pass.


  

Notes

* Default ticker: AAPL
* Missing keys will skip that data source (fallbacks included)
* Recommended to run sequentially in Jupyter
