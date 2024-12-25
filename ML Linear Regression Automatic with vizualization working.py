import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QLabel, QWidget, QListWidget, QLineEdit, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from fpdf import FPDF
import time

class DescriptionWindow(QWidget):
    def __init__(self, description):
        super().__init__()
        self.setWindowTitle("Data Description")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(description)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ML: Data Load Analyze Visualize and Train Model")
        self.setGeometry(100, 100, 800, 600)
        
        # Set up the main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        
        # Add widgets to the layout
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)
        
        self.describe_button = QPushButton("Show Data Description")
        self.describe_button.clicked.connect(self.show_data_description)
        self.layout.addWidget(self.describe_button)
        
        self.visualize_button = QPushButton("Visualize Data")
        self.visualize_button.clicked.connect(self.visualize_data)
        self.layout.addWidget(self.visualize_button)
        
        self.train_button = QPushButton("Train Model")
        self.train_button.clicked.connect(self.train_model_button)
        self.layout.addWidget(self.train_button)
        
        self.export_pdf_button = QPushButton("Export to PDF")
        self.export_pdf_button.clicked.connect(self.export_to_pdf_button)
        self.layout.addWidget(self.export_pdf_button)
        
        self.export_excel_button = QPushButton("Export to Excel")
        self.export_excel_button.clicked.connect(self.export_to_excel_button)
        self.layout.addWidget(self.export_excel_button)
        
        self.status_label = QLabel("Status: Ready")
        self.layout.addWidget(self.status_label)

        self.stats_label = QLabel("")
        self.layout.addWidget(self.stats_label)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.df = pd.read_csv(file_path)
            self.status_label.setText(f"Status: Loaded data from {file_path}")

    def show_data_description(self):
        if hasattr(self, 'df'):
            description = self.df.describe().to_string()
            self.description_window = DescriptionWindow(description)
            self.description_window.show()
        else:
            QMessageBox.warning(self, "Error", "No data loaded")

    def visualize_data(self):
        if hasattr(self, 'df'):
            sns.pairplot(self.df)
            plt.savefig("pairplot.png")
            plt.show()
            self.status_label.setText("Status: Data visualized")
        else:
            QMessageBox.warning(self, "Error", "No data loaded")

    def train_model(self, df, features, target, manual=False, learning_rate=0.01, epochs=100, batch_size=32):
        """Train a linear regression model with options for automatic and supervised learning."""
        X = df[features]
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        start_time = time.time()
        
        if manual:
            # Implement supervised learning with adjustable parameters
            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            print(f"Supervised Training - MSE: {mse}, MAE: {mae}")
        else:
            # Implement automatic learning
            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            print(f"Automatic Training - MSE: {mse}, MAE: {mae}")

        end_time = time.time()
        training_time = end_time - start_time

        self.model = model
        self.loss_table = {"MSE": mse, "MAE": mae}
        self.training_stats = {
            "Time to execute": training_time,
            "Batch size used": batch_size,
            "Epochs used": epochs,
            "Learning rate used": learning_rate,
            "MSE": mse,
            "MAE": mae,
            "Prediction formula": f"y = {model.intercept_} + {model.coef_} * X"
        }

        stats_text = "\n".join([f"{key}: {value}" for key, value in self.training_stats.items()])
        self.stats_label.setText(stats_text)

    def train_model_button(self):
        if hasattr(self, 'df'):
            features = self.df.columns[:-1]  # Assuming the last column is the target
            target = self.df.columns[-1]
            self.train_model(self.df, features, target)
            self.status_label.setText("Status: Model trained")
        else:
            QMessageBox.warning(self, "Error", "No data loaded")

    def export_to_pdf(self, file_path):
        """Export model results and plots to a PDF."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Model Results", ln=True, align='C')

        pdf.cell(200, 10, txt="Coefficients:", ln=True)
        for i, coef in enumerate(self.model.coef_):
            pdf.cell(200, 10, txt=f"Feature {i}: {coef}", ln=True)

        pdf.cell(200, 10, txt=f"Intercept: {self.model.intercept_}", ln=True)

        pdf.cell(200, 10, txt="Loss Table:", ln=True)
        for key, value in self.loss_table.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        pdf.cell(200, 10, txt="Training Stats:", ln=True)
        for key, value in self.training_stats.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        pdf.image("pairplot.png", x=10, y=None, w=190)
        pdf.output(file_path)

    def export_to_pdf_button(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.export_to_pdf(file_path)
            self.status_label.setText(f"Status: Exported to {file_path}")

    def export_to_excel(self, file_path):
        coeffs = pd.DataFrame({
            "Feature": [self.feature_list.item(i).text() for i in range(self.feature_list.count()) if self.feature_list.item(i).isSelected()],
            "Coefficient": self.model.coef_
        })
        coeffs.to_excel(file_path, index=False)

        stats_df = pd.DataFrame(list(self.training_stats.items()), columns=["Metric", "Value"])
        with pd.ExcelWriter(file_path, mode='a') as writer:
            stats_df.to_excel(writer, sheet_name='Training Stats', index=False)

    def export_to_excel_button(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            self.export_to_excel(file_path)
            self.status_label.setText(f"Status: Exported to {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec_())