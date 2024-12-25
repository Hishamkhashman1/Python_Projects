import sys
import yfinance as yf
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QWidget, QMessageBox, QCompleter
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import os

class CurrencyExchangeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Exchange")
        self.setGeometry(100, 100, 400, 300)
        
        # Set up the main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        
        # Set font
        font = QFont()
        font.setPointSize(12)
        
        # Add widgets to the layout
        self.amount_label = QLabel("Amount:")
        self.amount_label.setFont(font)
        self.amount_input = QLineEdit()
        self.amount_input.setFont(font)
        self.layout.addWidget(self.amount_label)
        self.layout.addWidget(self.amount_input)
        
        self.from_currency_label = QLabel("From Currency:")
        self.from_currency_label.setFont(font)
        self.from_currency_combo = QComboBox()
        self.from_currency_combo.setFont(font)
        self.from_currency_combo.setEditable(True)  # Make the combo box editable
        self.layout.addWidget(self.from_currency_label)
        self.layout.addWidget(self.from_currency_combo)
        
        self.to_currency_label = QLabel("To Currency:")
        self.to_currency_label.setFont(font)
        self.to_currency_combo = QComboBox()
        self.to_currency_combo.setFont(font)
        self.to_currency_combo.setEditable(True)  # Make the combo box editable
        self.layout.addWidget(self.to_currency_label)
        self.layout.addWidget(self.to_currency_combo)
        
        self.convert_button = QPushButton("Convert")
        self.convert_button.setFont(font)
        self.convert_button.clicked.connect(self.convert_currency)
        self.layout.addWidget(self.convert_button)
        
        self.result_label = QLabel("")
        self.result_label.setFont(font)
        self.layout.addWidget(self.result_label)
        
        self.rate_label = QLabel("")
        self.rate_label.setFont(font)
        self.layout.addWidget(self.rate_label)
        
        # Populate the currency dropdowns
        self.currencies = {
            'AFN': 'Afghan afghani',
            'ALL': 'Albanian lek',
            'AMD': 'Armenian dram',
            'ANG': 'Netherlands Antillean guilder',
            'AOA': 'Angolan kwanza',
            'ARS': 'Argentine peso',
            'AUD': 'Australian dollar',
            'AWG': 'Aruban florin',
            'AZN': 'Azerbaijani manat',
            'BAM': 'Bosnia and Herzegovina convertible mark',
            'BBD': 'Barbadian dollar',
            'BDT': 'Bangladeshi taka',
            'BGN': 'Bulgarian lev',
            'BHD': 'Bahraini dinar',
            'BIF': 'Burundian franc',
            'BMD': 'Bermudian dollar',
            'BND': 'Brunei dollar',
            'BOB': 'Bolivian boliviano',
            'BRL': 'Brazilian real',
            'BSD': 'Bahamian dollar',
            'BTN': 'Bhutanese ngultrum',
            'BWP': 'Botswana pula',
            'BYN': 'Belarusian ruble',
            'BZD': 'Belize dollar',
            'CAD': 'Canadian dollar',
            'CDF': 'Congolese franc',
            'CHF': 'Swiss franc',
            'CLP': 'Chilean peso',
            'CNY': 'Chinese yuan',
            'COP': 'Colombian peso',
            'CRC': 'Costa Rican colón',
            'CUP': 'Cuban peso',
            'CVE': 'Cape Verdean escudo',
            'CZK': 'Czech koruna',
            'DJF': 'Djiboutian franc',
            'DKK': 'Danish krone',
            'DOP': 'Dominican peso',
            'DZD': 'Algerian dinar',
            'EGP': 'Egyptian pound',
            'ERN': 'Eritrean nakfa',
            'ETB': 'Ethiopian birr',
            'EUR': 'Euro',
            'FJD': 'Fijian dollar',
            'FKP': 'Falkland Islands pound',
            'FOK': 'Faroese króna',
            'GBP': 'British pound sterling',
            'GEL': 'Georgian lari',
            'GGP': 'Guernsey pound',
            'GHS': 'Ghanaian cedi',
            'GIP': 'Gibraltar pound',
            'GMD': 'Gambian dalasi',
            'GNF': 'Guinean franc',
            'GTQ': 'Guatemalan quetzal',
            'GYD': 'Guyanese dollar',
            'HKD': 'Hong Kong dollar',
            'HNL': 'Honduran lempira',
            'HRK': 'Croatian kuna',
            'HTG': 'Haitian gourde',
            'HUF': 'Hungarian forint',
            'IDR': 'Indonesian rupiah',
            'ILS': 'Israeli new shekel',
            'IMP': 'Isle of Man pound',
            'INR': 'Indian rupee',
            'IQD': 'Iraqi dinar',
            'IRR': 'Iranian rial',
            'ISK': 'Icelandic króna',
            'JEP': 'Jersey pound',
            'JMD': 'Jamaican dollar',
            'JOD': 'Jordanian dinar',
            'JPY': 'Japanese yen',
            'KES': 'Kenyan shilling',
            'KGS': 'Kyrgyzstani som',
            'KHR': 'Cambodian riel',
            'KID': 'Kiribati dollar',
            'KMF': 'Comorian franc',
            'KRW': 'South Korean won',
            'KWD': 'Kuwaiti dinar',
            'KYD': 'Cayman Islands dollar',
            'KZT': 'Kazakhstani tenge',
            'LAK': 'Lao kip',
            'LBP': 'Lebanese pound',
            'LKR': 'Sri Lankan rupee',
            'LRD': 'Liberian dollar',
            'LSL': 'Lesotho loti',
            'LYD': 'Libyan dinar',
            'MAD': 'Moroccan dirham',
            'MDL': 'Moldovan leu',
            'MGA': 'Malagasy ariary',
            'MKD': 'Macedonian denar',
            'MMK': 'Myanmar kyat',
            'MNT': 'Mongolian tögrög',
            'MOP': 'Macanese pataca',
            'MRU': 'Mauritanian ouguiya',
            'MUR': 'Mauritian rupee',
            'MVR': 'Maldivian rufiyaa',
            'MWK': 'Malawian kwacha',
            'MXN': 'Mexican peso',
            'MYR': 'Malaysian ringgit',
            'MZN': 'Mozambican metical',
            'NAD': 'Namibian dollar',
            'NGN': 'Nigerian naira',
            'NIO': 'Nicaraguan córdoba',
            'NOK': 'Norwegian krone',
            'NPR': 'Nepalese rupee',
            'NZD': 'New Zealand dollar',
            'OMR': 'Omani rial',
            'PAB': 'Panamanian balboa',
            'PEN': 'Peruvian sol',
            'PGK': 'Papua New Guinean kina',
            'PHP': 'Philippine peso',
            'PKR': 'Pakistani rupee',
            'PLN': 'Polish złoty',
            'PYG': 'Paraguayan guaraní',
            'QAR': 'Qatari riyal',
            'RON': 'Romanian leu',
            'RSD': 'Serbian dinar',
            'RUB': 'Russian ruble',
            'RWF': 'Rwandan franc',
            'SAR': 'Saudi riyal',
            'SBD': 'Solomon Islands dollar',
            'SCR': 'Seychellois rupee',
            'SDG': 'Sudanese pound',
            'SEK': 'Swedish krona',
            'SGD': 'Singapore dollar',
            'SHP': 'Saint Helena pound',
            'SLL': 'Sierra Leonean leone',
            'SOS': 'Somali shilling',
            'SRD': 'Surinamese dollar',
            'SSP': 'South Sudanese pound',
            'STN': 'São Tomé and Príncipe dobra',
            'SYP': 'Syrian pound',
            'SZL': 'Eswatini lilangeni',
            'THB': 'Thai baht',
            'TJS': 'Tajikistani somoni',
            'TMT': 'Turkmenistani manat',
            'TND': 'Tunisian dinar',
            'TOP': 'Tongan paʻanga',
            'TRY': 'Turkish lira',
            'TTD': 'Trinidad and Tobago dollar',
            'TZS': 'Tanzanian shilling',
            'UAH': 'Ukrainian hryvnia',
            'UGX': 'Ugandan shilling',
            'USD': 'United States dollar',
            'UYU': 'Uruguayan peso',
            'UZS': 'Uzbekistani som',
            'VES': 'Venezuelan bolívar soberano',
            'VND': 'Vietnamese đồng',
            'VUV': 'Vanuatu vatu',
            'WST': 'Samoan tālā',
            'XAF': 'Central African CFA franc',
            'XCD': 'East Caribbean dollar',
            'XOF': 'West African CFA franc',
            'XPF': 'CFP franc',
            'YER': 'Yemeni rial',
            'ZAR': 'South African rand',
            'ZMW': 'Zambian kwacha',
            'ZWL': 'Zimbabwean dollar'
        }
        
        self.currency_codes = list(self.currencies.keys())
        self.currency_codes.sort()  # Sort currency codes alphabetically

        # Add flags and predictive text
        self.add_currencies_with_flags(self.from_currency_combo)
        self.add_currencies_with_flags(self.to_currency_combo)
    
    def add_currencies_with_flags(self, combo_box):
        completer = QCompleter(self.currency_codes, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        combo_box.setCompleter(completer)
        
        for code in self.currency_codes:
            currency_name = self.currencies[code]
            display_text = f"{code} - {currency_name}"
            flag_path = os.path.join('flags', f'{code}.png')
            if os.path.exists(flag_path):
                flag_icon = QIcon(flag_path)
            else:
                flag_icon = QIcon()  # Placeholder for missing flags
            combo_box.addItem(flag_icon, display_text)
    
    def convert_currency(self):
        try:
            amount = float(self.amount_input.text().replace(',', ''))
            from_currency_text = self.from_currency_combo.currentText()
            to_currency_text = self.to_currency_combo.currentText()
            
            from_currency = from_currency_text.split(' - ')[0]
            to_currency = to_currency_text.split(' - ')[0]
            
            if from_currency == to_currency:
                QMessageBox.warning(self, "Error", "Please select different currencies for conversion.")
                return
            
            # Fetch exchange rate using USD as an intermediary
            if from_currency != 'USD':
                ticker_from_usd = f"{from_currency}USD=X"
                data_from_usd = yf.download(ticker_from_usd, period='1d')
                if data_from_usd.empty:
                    raise ValueError(f"No data fetched for {ticker_from_usd}")
                exchange_rate_from_usd = data_from_usd['Close'].iloc[-1].item()
            else:
                exchange_rate_from_usd = 1.0
            
            if to_currency != 'USD':
                ticker_to_usd = f"USD{to_currency}=X"
                data_to_usd = yf.download(ticker_to_usd, period='1d')
                if data_to_usd.empty:
                    raise ValueError(f"No data fetched for {ticker_to_usd}")
                exchange_rate_to_usd = data_to_usd['Close'].iloc[-1].item()
            else:
                exchange_rate_to_usd = 1.0
            
            # Calculate the final exchange rate
            exchange_rate = exchange_rate_from_usd * exchange_rate_to_usd
            print(f"Exchange rate: {exchange_rate}")
            
            converted_amount = amount * exchange_rate
            formatted_amount = f"{converted_amount:,.2f}"
            self.result_label.setText(f"{amount:,.2f} {from_currency} = {formatted_amount} {to_currency}")
            self.rate_label.setText(f"Exchange Rate: 1 {from_currency} = {exchange_rate:.4f} {to_currency}")
        except ValueError as ve:
            QMessageBox.critical(self, "Error", f"Value Error: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert currency: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyExchangeApp()
    window.show()
    sys.exit(app.exec_())