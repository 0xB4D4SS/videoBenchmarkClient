import socket
import sys
import time
from multiprocessing import Process

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QTextEdit, QWidget, QLineEdit


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = None
        self.flag = True
        self.setWindowTitle("VideoBenchmark Client")
        self.resize(400, 300)

        self.textEdit = QTextEdit()
        self.socket_data = QLineEdit()
        self.socket_data.setText("127.0.0.1:5000")
        self.textEdit.setReadOnly(True)
        self.btn1 = QPushButton("Connect")
        self.btn2 = QPushButton("Stop")
        self.btn3 = QPushButton("Receive")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.socket_data)
        self.setLayout(layout)

        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.btn3.clicked.connect(self.btn3_clicked)

    def btn1_clicked(self):
        if not self.flag:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = self.socket_data.text().split(":")
        self.address[1] = int(self.address[1])
        self.address = tuple(self.address)
        try:
            self.sock.connect(self.address)
            self.textEdit.append("Connected!")
        except OSError as msg:
            self.textEdit.append(f"Error: {msg}")

    def btn2_clicked(self):
        # TODO: end connection properly (now we get crash after stop->connect)
        self.sock.close()
        self.flag = not self.flag
        self.textEdit.append(f"Flag state: {self.flag}")

    def btn3_clicked(self):
        # TODO: need loop to continuously receive data
        self.sock.sendall(bytes("getdata\n", "utf-8"))
        data = str(self.sock.recv(1024), "utf-8")
        self.textEdit.append(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
