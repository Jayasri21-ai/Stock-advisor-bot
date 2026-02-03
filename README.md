📈 Stock Advisor Bot

Stock Advisor Bot is a Flask-based web application that provides real-time insights into the Indian stock market. It allows users to interact using natural language queries and receive instant responses such as current stock prices, company details, financial performance, CEO information, and basic buy/sell recommendations.
The application also integrates OpenAI to handle general investment-related questions, making it an intelligent and interactive decision-support tool.

**Features

1.Fetches real-time Indian stock prices (NSE)

2.Provides company details and CEO information

3.Displays financial data such as revenue, net income, and profit margin

4.Generates basic buy/sell recommendations using historical price trends

5.AI-powered responses for general stock market queries

6.RESTful API built using Flask

7.Secure API key management using environment variables

8.Tech Stack

**Backend:** Python, Flask, Flask-SocketIO

**Market Data**: Yahoo Finance (yfinance)

**AI Integration**: OpenAI API

**Frontend**: HTML, JavaScript

**Architecture**: Client–Server, REST API

**How It Works

1.The user enters a query (e.g., stock price, company details, or investment-related questions).
2.The Flask backend analyzes the query and identifies the stock ticker if present.
3.Stock-related data is fetched using Yahoo Finance.
4.General queries are handled using the OpenAI API.
5.The response is returned in JSON format and displayed on the frontend.

**Installation & Setup
Python 3.8+
pip
OpenAI API Key
