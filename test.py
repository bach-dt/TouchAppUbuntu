import datetime
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

translateDate = {"Thứ hai": "Monday",
                 "Thứ ba": "Tuesday",
                 "Thứ tư": "Wednesday",
                 "Thứ năm": "Thursday",
                 "Thứ sáu": "Friday",
                 "Thứ bảy": "Saturday",
                 "Chủ nhật": "Sunday"}


class CloseTime(QtCore.QThread):
    dataChanged = QtCore.pyqtSignal(str)

    def run(self):
        while True:
            # timeThis = datetime.datetime.now().strftime("%S")
            timeThis = "abc"
            print(timeThis)
            self.dataChanged.emit(timeThis)


a = 4


def ab():
    print("a")


app = QApplication(sys.argv)
close = CloseTime()
close.start()
close.dataChanged.connect(ab)
sys.exit(app.exec_())
