import socket
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QTextEdit, QWidget, QLineEdit


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.address = None
        self.setWindowTitle("VideoBenchmark Client")
        self.resize(400, 300)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getsomedata)
        self.textEdit = QTextEdit()
        self.socket_data = QLineEdit()
        self.socket_data.setText("127.0.0.1:5000")
        self.textEdit.setReadOnly(True)
        self.btn1 = QPushButton("Connect")
        self.btn2 = QPushButton("Stop")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.socket_data)
        self.setLayout(layout)

        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)

    def btn1_clicked(self):
        self.timer.start(1000)

    def btn2_clicked(self):
        self.timer.stop()

    def getsomedata(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = self.socket_data.text().split(":")
        self.address[1] = int(self.address[1])
        self.address = tuple(self.address)
        sock.connect(self.address)
        sock.sendall(bytes("getdata\n", "utf-8"))
        data = str(sock.recv(1024), "utf-8")
        self.textEdit.append(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
