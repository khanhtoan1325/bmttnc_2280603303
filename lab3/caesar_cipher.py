import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối nút bấm với hàm xử lý
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        plain_text = self.ui.txt_plain_text.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not plain_text or not key:
            QMessageBox.warning(self, "Warning", "Please enter both plain text and key.")
            return

        payload = {
            "plain_text": plain_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data.get("encrypted_message", ""))
                QMessageBox.information(self, "Success", "Encrypted Successfully")
            else:
                QMessageBox.critical(self, "Error", f"Encryption failed: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request Error: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not cipher_text or not key:
            QMessageBox.warning(self, "Warning", "Please enter both cipher text and key.")
            return

        payload = {
            "cipher_text": cipher_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data.get("decrypted_message", ""))
                QMessageBox.information(self, "Success", "Decrypted Successfully")
            else:
                QMessageBox.critical(self, "Error", f"Decryption failed: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
