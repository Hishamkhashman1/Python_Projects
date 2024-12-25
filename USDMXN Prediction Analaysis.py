import sys
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime

class ExchangeRateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USD/MXN Exchange Rate Prediction")
        self.setGeometry(100, 100, 800, 600)
        
        # Set up the main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        
        # Add widgets to the layout
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)
        
        self.train_button = QPushButton("Train Model")
        self.train_button.clicked.connect(self.train_model)
        self.layout.addWidget(self.train_button)
        
        self.predict_button = QPushButton("Predict Exchange Rate")
        self.predict_button.clicked.connect(self.predict_exchange_rate)
        self.layout.addWidget(self.predict_button)
        
        self.plot_button = QPushButton("Plot Data")
        self.plot_button.clicked.connect(self.plot_data)
        self.layout.addWidget(self.plot_button)
        
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.status_label)
        
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.result_label)
        
        self.data_loaded_label = QLabel("")
        self.data_loaded_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.data_loaded_label)

    def load_data(self):
        try:
            # Fetch historical data using yfinance
            self.df = self.get_historical_data()
            self.status_label.setText("Status: Data loaded")
            self.data_loaded_label.setText("Data Loaded: USD/MXN, Oil Price, USD Interest Rate, INMEX.MX, S&P 500, DJI, Gold")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")

    def get_historical_data(self):
        # Fetch historical data for USD/MXN exchange rate, oil prices, USD interest rates, INMEX.MX, GSPC, DJI, Crude Oil, and Gold
        exchange_rate_data = yf.download('MXN=X', start='2020-01-01', end='2024-12-31')
        oil_price_data = yf.download('CL=F', start='2020-01-01', end='2024-12-31')
        usd_interest_rate_data = yf.download('^IRX', start='2020-01-01', end='2024-12-31')
        in_mex_data = yf.download('^MXX', start='2020-01-01', end='2024-12-31')
        gspc_data = yf.download('^GSPC', start='2020-01-01', end='2024-12-31')
        dji_data = yf.download('^DJI', start='2020-01-01', end='2024-12-31')
        gold_data = yf.download('GC=F', start='2020-01-01', end='2024-12-31')

        # Prepare the dataframes
        exchange_rate_df = exchange_rate_data[['Close']].rename(columns={'Close': 'exchange_rate'})
        oil_price_df = oil_price_data[['Close']].rename(columns={'Close': 'oil_price'})
        usd_interest_rate_df = usd_interest_rate_data[['Close']].rename(columns={'Close': 'usd_interest_rate'})
        in_mex_df = in_mex_data[['Close']].rename(columns={'Close': 'in_mex'})
        gspc_df = gspc_data[['Close']].rename(columns={'Close': 'gspc'})
        dji_df = dji_data[['Close']].rename(columns={'Close': 'dji'})
        gold_df = gold_data[['Close']].rename(columns={'Close': 'gold'})

        # Merge dataframes on date
        data = exchange_rate_df.join(oil_price_df, how='inner').join(usd_interest_rate_df, how='inner')
        data = data.join(in_mex_df, how='inner').join(gspc_df, how='inner')
        data = data.join(dji_df, how='inner').join(gold_df, how='inner')

        # Reset index to have date as a column
        data.reset_index(inplace=True)
        data.rename(columns={'Date': 'date'}, inplace=True)

        # Ensure date column is in datetime format
        data['date'] = pd.to_datetime(data['date'])

        # Handle missing values
        data = data.dropna()

        return data

    def train_model(self):
        try:
            if hasattr(self, 'df'):
                # Use only the exchange rate for SARIMA model
                self.model = SARIMAX(self.df['exchange_rate'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
                self.model_fit = self.model.fit(disp=False)
                self.status_label.setText("Status: Model trained")

                # Display training statistics
                mse = mean_squared_error(self.df['exchange_rate'], self.model_fit.fittedvalues)
                mae = mean_absolute_error(self.df['exchange_rate'], self.model_fit.fittedvalues)
                QMessageBox.information(self, "Training Complete", f"Methodology: SARIMA\nMSE: {mse:.4f}\nMAE: {mae:.4f}")
            else:
                QMessageBox.warning(self, "Error", "No data loaded")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to train model: {e}")

    def predict_exchange_rate(self):
        try:
            if hasattr(self, 'model_fit'):
                # Predict the exchange rate for the next 12 months
                future_dates = pd.date_range(start=self.df['date'].max() + pd.DateOffset(months=1), periods=12, freq='M')
                forecast = self.model_fit.get_forecast(steps=12)
                forecast_index = pd.date_range(start=self.df['date'].max() + pd.DateOffset(months=1), periods=12, freq='M')
                forecast_df = pd.DataFrame({'date': forecast_index, 'predicted_exchange_rate': forecast.predicted_mean})

                # Display the predicted exchange rates
                result_text = "Predicted Exchange Rate for next 12 months:\n"
                result_text += forecast_df.to_string(index=False)
                self.result_label.setText(result_text)
                self.status_label.setText("Status: Prediction complete")

                # Plot the predictions
                plt.figure(figsize=(10, 6))
                plt.plot(forecast_df['date'], forecast_df['predicted_exchange_rate'], label='Predicted Exchange Rate', linestyle='--')
                plt.xlabel('Date')
                plt.ylabel('Exchange Rate')
                plt.title('USD/MXN Exchange Rate Prediction')
                plt.legend()
                plt.show()

                # Show a message box with methodology and metrics
                mse = mean_squared_error(self.df['exchange_rate'], self.model_fit.fittedvalues)
                mae = mean_absolute_error(self.df['exchange_rate'], self.model_fit.fittedvalues)
                QMessageBox.information(self, "Prediction Complete", f"Methodology: SARIMA\nMSE: {mse:.4f}\nMAE: {mae:.4f}")
            else:
                QMessageBox.warning(self, "Error", "Model not trained")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to predict exchange rate: {e}")

    def plot_data(self):
        try:
            if hasattr(self, 'df'):
                self.df.plot(x='date', y=['exchange_rate', 'oil_price', 'usd_interest_rate', 'in_mex', 'gspc', 'dji', 'gold'])
                plt.show()
                self.status_label.setText("Status: Data plotted")
            else:
                QMessageBox.warning(self, "Error", "No data loaded")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot data: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExchangeRateApp()
    window.show()
    sys.exit(app.exec_())