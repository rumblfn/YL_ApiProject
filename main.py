import sys
import os
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design.ui', self)
        self.setGeometry(600, 450, *SCREEN_SIZE)
        self.delta = "0.02"
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.add_img()

    def add_img(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = "37.530887"
        lat = "55.703118"

        self.params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }

        response = requests.get(api_server, params=self.params)
        if response:
            f = open("Res.png", 'wb')
            data = response.content
            f.write(data)
            self.pixmap = QPixmap('Res.png')
            self.image.setPixmap(self.pixmap)
            f.close()
            os.remove('Res.png')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.change_delta(True)
        if event.key() == Qt.Key_PageDown:
            self.change_delta(False)

    def change_delta(self, arg):
        if arg:
            if round(float(self.delta) + 0.005, 3) <= 0.3:
                self.delta = str(round(float(self.delta) + 0.005, 3))
                self.add_img()
                print(self.delta)
        else:
            if round(float(self.delta) - 0.005, 3) >= 0.005:
                self.delta = str(round(float(self.delta) - 0.005, 3))
                self.add_img()
                print(self.delta)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
