import socket
import sys
import re
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QTextEdit, QWidget, QLineEdit


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.address = None
        self.curr_data = None
        self.fpsdata = ''
        self.brdata = ''
        self.x = list()
        self.yfps = list()
        self.ybr = list()
        self.counter = 0
        self.setWindowTitle("VideoBenchmark Client")
        self.resize(800, 600)

        self.datatimer = QTimer(self)
        self.drawtimer = QTimer(self)
        self.textEdit = QTextEdit()
        self.socket_data = QLineEdit()
        self.pgfpsplot = pg.PlotWidget()
        self.pgbrplot = pg.PlotWidget()
        self.btn1 = QPushButton("Connect")
        self.btn2 = QPushButton("Disconnect")
        self.socket_data.setText("127.0.0.1:5000")
        self.textEdit.setReadOnly(True)
        self.btn2.setDisabled(True)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.textEdit)
        vlayout.addWidget(self.btn1)
        vlayout.addWidget(self.btn2)
        vlayout.addWidget(self.socket_data)
        vlayout.addWidget(self.pgfpsplot)
        vlayout.addWidget(self.pgbrplot)
        self.setLayout(vlayout)

        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.datatimer.timeout.connect(self.getsomedata)
        self.drawtimer.timeout.connect(self.drawsomedata)

    def btn1_clicked(self):
        self.datatimer.start(500)
        self.drawtimer.start(501)
        self.btn1.setDisabled(True)
        self.btn2.setDisabled(False)

    def btn2_clicked(self):
        self.datatimer.stop()
        self.drawtimer.stop()
        self.btn1.setDisabled(False)
        self.btn2.setDisabled(True)

    def getsomedata(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = self.socket_data.text().split(":")
        self.address[1] = int(self.address[1])
        self.address = tuple(self.address)
        sock.connect(self.address)
        sock.sendall(bytes("getdata\n", "utf-8"))
        data = str(sock.recv(1024), "utf-8")
        self.curr_data = data
        fpsregexp = re.compile("fps= ([0-9]*)")
        brregexp = re.compile("bitrate= ([0-9.]*)")
        self.fpsdata = fpsregexp.search(data).group(1)
        self.brdata = brregexp.search(data).group(1)
        self.textEdit.append(self.curr_data)

    def drawsomedata(self):
        self.counter += 1
        self.x.append(self.counter)
        self.yfps.append(int(self.fpsdata))
        self.ybr.append(float(self.brdata))
        self.pgfpsplot.plot(self.x, self.yfps, pen='g')
        self.pgbrplot.plot(self.x, self.ybr, pen='g')
        if self.counter > 60:
            self.counter = 0
            self.x.clear()
            self.yfps.clear()
            self.ybr.clear()
            self.pgfpsplot.clear()
            self.pgbrplot.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
