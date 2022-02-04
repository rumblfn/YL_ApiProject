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
        self.delta_ind = 0
        self.delta_pars = [0.5, 1, 2, 4, 6, 10, 18, 70]
        self.image = QLabel(self)
        self.image.move(0, 50)
        self.image.resize(600, 450)

        self.pushButton_sql.clicked.connect(lambda: self.set_view('skl'))
        self.pushButton_sat.clicked.connect(lambda: self.set_view('sat'))
        self.pushButton_map.clicked.connect(lambda: self.set_view('map'))

        self.lon = 37.530887
        self.lat = 55.703118
        self.move_speed = 0.001
        self.view = 'map'

        self.add_img()

    def set_view(self, arg):
        self.view = arg
        self.add_img()

    def add_img(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        self.params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            "spn": ",".join([str(self.delta_pars[self.delta_ind] / 100), str(self.delta_pars[self.delta_ind] / 100)]),
            "l": self.view
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

    def movement(self, key):
        if key == Qt.Key_Left:
            self.lon -= self.move_speed
            self.add_img()
        if key == Qt.Key_Up:
            self.lat += self.move_speed
            self.add_img()
        if key == Qt.Key_Right:
            self.lon += self.move_speed
            self.add_img()
        if key == Qt.Key_Down:
            self.lat -= self.move_speed
            self.add_img()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.change_delta(False)
        if event.key() == Qt.Key_PageDown:
            self.change_delta(True)

        # task 1.3
        self.movement(event.key())

    def change_delta(self, arg):
        if arg:
            if self.delta_ind < 7:
                self.move_speed *= 2
                self.delta_ind += 1
                self.add_img()
        else:
            if self.delta_ind > 0:
                self.move_speed /= 2
                self.delta_ind -= 1
                self.add_img()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())