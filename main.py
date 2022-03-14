import socket
import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QTextEdit, QWidget


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("VideoBenchmark Client")
        self.resize(400, 300)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.btn1 = QPushButton("Connect")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btn1)
        self.setLayout(layout)

        self.btn1.clicked.connect(self.btn1_clicked)

    def btn1_clicked(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(("127.0.0.1", 5000))
            self.textEdit.append("Connected!\n")
        except ConnectionRefusedError:
            self.textEdit.append("Error!\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
