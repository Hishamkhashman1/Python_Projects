from tkinter import ttk
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from keras import Sequential, Input
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.regularizers import l2
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import matplotlib.dates as mdates
import os
from newsapi import NewsApiClient
from unidecode import unidecode

# Initialize News API client
newsapi = NewsApiClient(api_key='ab57665b93dc4be5be77fdf1154cf384')

def fetch_data(ticker):
    end = datetime.datetime.now() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=7*30)  # Approximately 6 months
    end = end.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    
    stock_data = yf.download(ticker, start=start, end=end, interval='1d')  # Fetch daily data
    if stock_data.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    
    if 'Adj Close' not in stock_data.columns:
        stock_data['Adj Close'] = stock_data['Open'].shift(-1)
        stock_data = stock_data.dropna()
    
    print(f"Fetched {len(stock_data)} samples for ticker {ticker}")  # Debugging statement
    return stock_data

def fetch_exchange_data(exchange_ticker):
    end = datetime.datetime.now() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=7*30)  # Approximately 6 months
    end = end.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    
    exchange_data = yf.download(exchange_ticker, start=start, end=end, interval='1d')  # Fetch daily data
    if exchange_data.empty:
        raise ValueError(f"No data found for exchange ticker {exchange_ticker}")
    
    if 'Adj Close' not in exchange_data.columns:
        exchange_data['Adj Close'] = exchange_data['Open'].shift(-1)
        exchange_data = exchange_data.dropna()
    
    print(f"Fetched {len(exchange_data)} samples for exchange ticker {exchange_ticker}")  # Debugging statement
    return exchange_data

def fetch_company_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    full_name = info.get('longName', 'N/A')
    current_price = info.get('currentPrice', 'N/A')
    description = info.get('longBusinessSummary', 'N/A')
    industry = info.get('industry', 'N/A')
    exchange = info.get('exchange', 'N/A')  # Get the stock exchange
    return full_name, current_price, description, industry, exchange

def fetch_latest_news(ticker):
    articles = newsapi.get_everything(q=ticker, language='en', sort_by='publishedAt', page_size=5)
    news = []
    for article in articles['articles']:
        news.append({
            'title': article['title'] if article['title'] else 'No title available',
            'description': article['description'] if article['description'] else 'No description available',
            'url': article['url'] if article['url'] else 'No URL available'
        })
    return news

def calculate_technical_indicators(stock_data):
    stock_data['SMA'] = stock_data['Adj Close'].rolling(window=20).mean()
    stock_data['EMA'] = stock_data['Adj Close'].ewm(span=20, adjust=False).mean()
    stock_data['RSI'] = 100 - (100 / (1 + stock_data['Adj Close'].pct_change().rolling(window=14).mean() / stock_data['Adj Close'].pct_change().rolling(window=14).std()))
    stock_data['MACD'] = stock_data['Adj Close'].ewm(span=12, adjust=False).mean() - stock_data['Adj Close'].ewm(span=26, adjust=False).mean()
    stock_data['MACD_Signal'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
    stock_data['MACD_Histogram'] = stock_data['MACD'] - stock_data['MACD_Signal']
    stock_data['Upper_BB'] = stock_data['SMA'] + (stock_data['Adj Close'].rolling(window=20).std() * 2)
    stock_data['Lower_BB'] = stock_data['SMA'] - (stock_data['Adj Close'].rolling(window=20).std() * 2)
    stock_data['ATR'] = stock_data['High'].rolling(window=14).max() - stock_data['Low'].rolling(window=14).min()
    stock_data['CCI'] = (stock_data['Adj Close'] - stock_data['Adj Close'].rolling(window=20).mean()) / (0.015 * stock_data['Adj Close'].rolling(window=20).std())
    stock_data['Momentum'] = stock_data['Adj Close'] - stock_data['Adj Close'].shift(14)
    stock_data['Parabolic_SAR'] = stock_data['Adj Close'].ewm(span=20, adjust=False).mean()  # Simplified version
    stock_data['Volume'] = stock_data['Volume']
    return stock_data

def preprocess_data(stock_data, exchange_data, sequence_length=120):
    stock_data = calculate_technical_indicators(stock_data)
    exchange_data = calculate_technical_indicators(exchange_data)
    
    stock_data = stock_data.dropna()  # Ensure no missing values
    exchange_data = exchange_data.dropna()  # Ensure no missing values
    
    feature_scaler = StandardScaler()
    target_scaler = StandardScaler()
    
    # Include the technical indicators as features
    features = ['Adj Close', 'SMA', 'EMA', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram', 'Upper_BB', 'Lower_BB', 'ATR', 'CCI', 'Momentum', 'Parabolic_SAR', 'Volume']
    
    stock_data = stock_data[features]
    exchange_data = exchange_data[['Adj Close']].rename(columns={'Adj Close': 'Exchange_Adj_Close'})
    
    combined_data = pd.concat([stock_data, exchange_data], axis=1)
    
    scaled_features = feature_scaler.fit_transform(combined_data.values)
    scaled_target = target_scaler.fit_transform(stock_data[['Adj Close']].values)
    
    X, y = [], []
    for i in range(sequence_length, len(scaled_features)):
        X.append(scaled_features[i-sequence_length:i])
        y.append(scaled_target[i, 0])
    
    X, y = np.array(X), np.array(y)
    print(f"Preprocessed data size: {X.shape[0]} samples")  # Debugging statement
    return X, y, feature_scaler, target_scaler

def build_lstm_model(input_shape, units=128, dropout_rate=0.3, learning_rate=0.001, l2_lambda=0.01):
    model = Sequential([
        Input(shape=input_shape),
        LSTM(units=units, return_sequences=True, kernel_regularizer=l2(l2_lambda)),
        Dropout(dropout_rate),
        LSTM(units=units//2, return_sequences=False, kernel_regularizer=l2(l2_lambda)),
        Dropout(dropout_rate),
        Dense(64, activation='relu', kernel_regularizer=l2(l2_lambda)),
        Dense(1)
    ])
    
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mean_absolute_error', metrics=['mae'])
    return model

def train_lstm_model(X_train, y_train, X_test, y_test, target_scaler):
    units = 128
    dropout_rate = 0.3
    learning_rate = 0.001
    batch_size = 50
    epochs = 50
    l2_lambda = 0.01

    print(f"Training model with units={units}, dropout_rate={dropout_rate}, learning_rate={learning_rate}, batch_size={batch_size}, epochs={epochs}, l2_lambda={l2_lambda}")
    model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]), units=units, dropout_rate=dropout_rate, learning_rate=learning_rate, l2_lambda=l2_lambda)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, callbacks=[EarlyStopping(monitor='val_loss', patience=10)], verbose=1)
    
    predictions = model.predict(X_test)
    predictions_inv = target_scaler.inverse_transform(predictions.reshape(-1, 1))  # Ensure correct shape
    y_test_inv = target_scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # Print some values to check the inverse transformation
    print("Original values (first 5):", y_test_inv[:5].flatten())
    print("Predicted values (first 5):", predictions_inv[:5].flatten())
    
    mae = mean_absolute_error(y_test_inv, predictions_inv)
    mse = mean_squared_error(y_test_inv, predictions_inv)
    
    return model, mae, mse

def forecast_trend(model, stock_data, exchange_data, feature_scaler, target_scaler, sequence_length=120, forecast_days=30):
    features = ['Adj Close', 'SMA', 'EMA', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram', 'Upper_BB', 'Lower_BB', 'ATR', 'CCI', 'Momentum', 'Parabolic_SAR', 'Volume']
    stock_data = stock_data[features]
    exchange_data = exchange_data[['Adj Close']].rename(columns={'Adj Close': 'Exchange_Adj_Close'})
    
    combined_data = pd.concat([stock_data, exchange_data], axis=1)
    
    last_sequence = combined_data.values[-sequence_length:]
    
    print(f"Last sequence for forecasting: {last_sequence}")  # Debugging statement
    
    current_sequence = last_sequence.copy()
    forecast = []
    
    for _ in range(forecast_days):
        scaled_sequence = feature_scaler.transform(current_sequence)
        model_input = scaled_sequence.reshape(1, sequence_length, len(combined_data.columns))
        
        prediction = model.predict(model_input, verbose=0)
        forecast.append(prediction[0, 0])
        
        new_row = current_sequence[-1].copy()
        new_row[0] = prediction[0, 0]
        current_sequence = np.vstack([current_sequence[1:], new_row])
    
    forecast = np.array(forecast).reshape(-1, 1)
    forecast_inv = target_scaler.inverse_transform(forecast)
    
    print(f"Forecasted values: {forecast_inv.flatten()}")  # Debugging statement
    
    return forecast_inv

def determine_trend_and_recommendation(forecasted_prices):
    initial_price = forecasted_prices[0]
    final_price = forecasted_prices[-1]
    percentage_change = ((final_price - initial_price) / initial_price) * 100

    if percentage_change > 0:
        trend = f"Bullish ({len(forecasted_prices)} days)"
        recommendation = "Buy"
    elif percentage_change < 0:
        trend = f"Bearish ({len(forecasted_prices)} days)"
        recommendation = "Sell"
    else:
        trend = f"Neutral ({len(forecasted_prices)} days)"
        recommendation = "Hold"
    
    return trend, recommendation

def generate_pdf(ticker, data, forecasted_prices, mae, mse, full_name, current_price, description, industry, trend, recommendation, news, exchange):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=unidecode(f"Stock Forecast Report for {ticker}"), ln=True, align='C')
    
    pdf.cell(200, 10, txt=unidecode(f"Mean Absolute Error (MAE): {mae}"), ln=True, align='L')
    pdf.cell(200, 10, txt=unidecode(f"Mean Squared Error (MSE): {mse}"), ln=True, align='L')
    pdf.cell(200, 10, txt=unidecode(f"{ticker} {full_name}"), ln=True, align='L')
    pdf.cell(200, 10, txt=unidecode(f"Current Price: {current_price}"), ln=True, align='L')
    pdf.cell(200, 10, txt=unidecode(f"Exchange: {exchange}"), ln=True, align='L')  # Add exchange information
    pdf.cell(200, 10, txt=unidecode(f"Tendency: {trend}"), ln=True, align='L')
    pdf.cell(200, 10, txt=unidecode(f"Recommendation: {recommendation}"), ln=True, align='L')
    pdf.cell(200, 10, txt=unidecode(f"Industry: {industry}"), ln=True, align='L')
    
 


    # Plot and save the forecast
    plt.figure(figsize=(14, 5))
    plt.plot(data.index, data['Adj Close'], label='Historical Prices')
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=len(forecasted_prices), freq='B')
    plt.plot(future_dates, forecasted_prices)
    plt.title(f'{ticker} Stock Price Trend Forecast ({recommendation})')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)  # Add gridlines
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('forecast.png')
    plt.close()
    
    pdf.image('forecast.png', x=10, y=80, w=190)
    
    pdf.set_y(150)  # Move to a new position below the plot
    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=unidecode("Description:"), ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, unidecode(description))
    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=unidecode("Latest News:"), ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for article in news:
        pdf.cell(200, 10, txt=unidecode(article['title']), ln=True, align='L')
        pdf.multi_cell(0, 10, unidecode(article['description']))
        pdf.cell(200, 10, txt=unidecode(article['url']), ln=True, align='L')
    
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pdf_path = os.path.join(output_dir, f"{ticker}_forecast_report.pdf")
    pdf.output(pdf_path)
    
    return pdf_path

def main():
    root = tk.Tk()
    root.withdraw()
    
    ticker = simpledialog.askstring("Input", "Enter Stock Ticker:")
    if not ticker:
        messagebox.showerror("Error", "Please enter a stock ticker.")
        return
    progress_window = tk.Toplevel(root)
    progress_window.title("Forecasting in Progress")
    progress_label = tk.Label(progress_window, text="Forecasting the future in progress...")
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
    progress_bar.pack(pady=10, padx=20)
    progress_bar.start()

    root.update()

    try:
        data = fetch_data(ticker)
        full_name, current_price, description, industry, exchange = fetch_company_info(ticker)
        
        # Fetch exchange data
        exchange_ticker = "^GSPC"  # Example: S&P 500 index ticker
        exchange_data = fetch_exchange_data(exchange_ticker)
        
        X, y, feature_scaler, target_scaler = preprocess_data(data, exchange_data)
        
        if len(X) == 0:
            raise ValueError("Not enough data to create sequences. Try increasing the date range or reducing the sequence length.")
        
        best_model = None
        best_mae = float('inf')
        best_mse = None
        
        for attempt in range(5):  # Increase the number of attempts to increase training diversity
            print(f"Training attempt {attempt + 1} of 5")
            if len(X) < 5:
                test_size = 0.5
            else:
                test_size = 0.2
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=attempt)  # Use different random states
            
            model, mae, mse = train_lstm_model(X_train, y_train, X_test, y_test, target_scaler)
            
            if mae < best_mae:
                best_mae = mae
                best_model = model
                best_mse = mse
        
        print(f"Best MAE: {best_mae}")
        
        forecasted_prices = forecast_trend(best_model, data, exchange_data, feature_scaler, target_scaler)
        trend, recommendation = determine_trend_and_recommendation(forecasted_prices)
        news = fetch_latest_news(ticker)
        
        pdf_path = generate_pdf(ticker, data, forecasted_prices, best_mae, best_mse, full_name, current_price, description, industry, trend, recommendation, news, exchange)
        
        messagebox.showinfo("Info", f"Report generated for {ticker}\nLocation: {pdf_path}")
        print(f"PDF report generated at: {pdf_path}")
        os.startfile(pdf_path)  # Automatically open the generated PDF
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()