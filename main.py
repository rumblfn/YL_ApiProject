import sys
import os
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [600, 450]


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design.ui', self)
        self.setGeometry(600, 450, *SCREEN_SIZE)

        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = "37.530887"
        lat = "55.703118"
        delta = "0.002"

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)
        if response:
            f = open("Res.png", 'wb')
            data = response.content
            self.pixmap = QPixmap('Res.png')
            self.image = QLabel(self)
            self.image.move(0, 0)
            self.image.resize(600, 450)
            self.image.setPixmap(self.pixmap)
            f.close()
            os.remove('Res.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())