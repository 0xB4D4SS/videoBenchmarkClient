import socket
import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QTextEdit, QWidget, QLineEdit


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.sock = None
        self.address = None
        self.setWindowTitle("VideoBenchmark Client")
        self.resize(400, 300)

        self.textEdit = QTextEdit()
        self.socket = QLineEdit()
        self.socket.setPlaceholderText("127.0.0.1:5000")
        self.socket.setText("127.0.0.1:5000")
        self.textEdit.setReadOnly(True)
        self.btn1 = QPushButton("Connect")
        self.btn2 = QPushButton("Disconnect")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.socket)
        self.setLayout(layout)

        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)

    def btn1_clicked(self):
        self.address = self.socket.text().split(":")
        self.address[1] = int(self.address[1])
        self.address = tuple(self.address)
        self.textEdit.append(f"Connecting to: {str(self.address)}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(self.address)

            self.textEdit.append("Connected!\n")
        except ConnectionError:
            self.textEdit.append("Error!\n")

    def btn2_clicked(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.textEdit.append("Closed!\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
