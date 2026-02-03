from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import yfinance as yf
from openai import OpenAI  # Updated OpenAI import
from openai import OpenAI


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Set your OpenAI API key herecd
from openai import OpenAI

# Try to load OpenAI only if key is set
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


# List of popular Indian stock tickers
INDIAN_STOCKS = ["TCS", "INFY", "WIPRO", "TATAMOTORS", "ZOMATO", "PAYTM", "HCLTECH", "SBIN", "HDFCBANK"]

def get_stock_price(ticker):
    """Fetch the latest stock price."""
    try:
        if not ticker.endswith('.NS'):
            ticker += '.NS'
        
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        
        if hist.empty:
            return f"No data available for {ticker}."
        
        latest_price = hist['Close'].iloc[-1]
        return f"💰 **Latest price of {ticker}:** ₹{latest_price:.2f}"
    except Exception as e:
        return f"Could not fetch price for {ticker}. Error: {str(e)}"

def get_ceo_details(ticker):
    """Fetch CEO and executive details."""
    try:
        if not ticker.endswith('.NS'):
            ticker += '.NS'
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info:
            return f"No details available for {ticker}."
        
        ceo = info.get('companyOfficers', [{}])[0].get('name', 'N/A')
        title = info.get('companyOfficers', [{}])[0].get('title', 'N/A')
        return f"👤 **CEO of {ticker}:** {ceo} ({title})"
    except Exception as e:
        return f"Could not fetch CEO details for {ticker}. Error: {str(e)}"

def get_stock_details(ticker):
    """Fetch detailed information about a stock in 4-5 points."""
    try:
        if not ticker.endswith('.NS'):
            ticker += '.NS'
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info:
            return f"No details available for {ticker}."
        
        # Extract and format stock details
        name = info.get('shortName', 'N/A')
        sector = info.get('sector', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        current_price = info.get('currentPrice', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')

        return (
            f"📊 **Details for {ticker}:**\n"
            f"- **Name:** {name}\n"
            f"- **Sector:** {sector}\n"
            f"- **Market Cap:** ₹{market_cap:,.2f}\n"
            f"- **Current Price:** ₹{current_price:.2f}\n"
            f"- **P/E Ratio:** {pe_ratio}"
        )
    except Exception as e:
        return f"Could not fetch details for {ticker}. Error: {str(e)}"

def get_stock_financials(ticker):
    """Fetch financial metrics for a stock."""
    try:
        if not ticker.endswith('.NS'):
            ticker += '.NS'
        
        stock = yf.Ticker(ticker)
        financials = stock.financials
        
        if financials.empty:
            return f"No financial data available for {ticker}."
        
        # Extract latest financial data
        revenue = financials.loc['Total Revenue'].iloc[0]
        net_income = financials.loc['Net Income'].iloc[0]
        profit_margin = (net_income / revenue) * 100
        
        return (
            f"💰 **Financials for {ticker}:**\n"
            f"- **Revenue:** ₹{revenue:,.2f}\n"
            f"- **Net Income:** ₹{net_income:,.2f}\n"
            f"- **Profit Margin:** {profit_margin:.2f}%"
        )
    except Exception as e:
        return f"Could not fetch financials for {ticker}. Error: {str(e)}"

def get_stock_recommendation(ticker):
    """Fetch stock data and provide buy/sell recommendations."""
    try:
        if not ticker.endswith('.NS'):
            ticker += '.NS'
        
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        
        if hist.empty:
            return f"No data available for {ticker}."
        
        # Analyze stock prices
        current_price = hist['Close'].iloc[-1]
        previous_price = hist['Close'].iloc[0]
        if current_price > previous_price:
            return f"The stock price of {ticker} has increased. It might be a good time to **buy**!"
        else:
            return f"The stock price of {ticker} has decreased. It might be a good time to **sell** or hold."
    except Exception as e:
        return f"Could not fetch data for {ticker}. Error: {str(e)}"

def generate_ai_response(user_message):
    """Generate a response using OpenAI's GPT-4."""
    try:
        ai_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful stock market advisor specializing in the Indian stock market."},
                {"role": "user", "content": user_message}
            ]
        )
        return ai_response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}. Please ensure the OpenAI API is configured correctly."

@app.route('/chat', methods=['POST'])
def chat():
    """Handle user messages."""
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please provide a valid message."})

    # Check if the user asked for stock details, historical data, or financials
    words = user_message.upper().split()
    ticker = next((word for word in words if word in INDIAN_STOCKS), None)

    if "CEO" in user_message.upper() and ticker:
        response = get_ceo_details(ticker)
    elif "PRICE" in user_message.upper() and ticker:
        response = get_stock_price(ticker)
    elif "DETAILS" in user_message.upper() and ticker:
        response = get_stock_details(ticker)
    elif "PROFIT" in user_message.upper() and ticker:
        response = get_stock_financials(ticker)
    elif "REVENUE" in user_message.upper() and ticker:
        response = get_stock_financials(ticker)
    elif ("BUY" in user_message.upper() or "SELL" in user_message.upper()) and ticker:
        response = get_stock_recommendation(ticker)
    elif "SECTOR" in user_message.upper() and ticker:
        response = get_stock_details(ticker)
    elif ticker:
        response = get_stock_details(ticker)
    else:
        # Handle general queries using OpenAI
        response = generate_ai_response(user_message)

    return jsonify({"response": response})

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)