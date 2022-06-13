import datetime
import sys
import random
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QDialog, QMessageBox, QGraphicsBlurEffect
import BorrowFrame
import ReturnFrame
import MainFrame
import Success
import Warning
from serial import Serial
import JsonFirestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Declare app
app = QApplication(sys.argv)
Json = JsonFirestore

# Use a service account
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

period = [["00-00", "06-45"],
          ["06-45", "07-30"],
          ["07-30", "08-15"],
          ["08-25", "09-10"],
          ["09-20", "10-15"],
          ["10-15", "11-00"],
          ["11-00", "11-45"],
          ["12-30", "13-15"],
          ["13-15", "14-00"],
          ["14-10", "14-55"],
          ["15-05", "15-50"],
          ["16-00", "16-45"],
          ["16-45", "17-30"],
          ["17-45", "18-30"],
          ["18-30", "19-15"]]

translateDate = {"Thứ hai": "Monday",
                 "Thứ ba": "Tuesday",
                 "Thứ tư": "Wednesday",
                 "Thứ năm": "Thursday",
                 "Thứ sáu": "Friday",
                 "Thứ bảy": "Saturday",
                 "Chủ nhật": "Sunday",
                 "Monday": "Monday",
                 "Tuesday": "Tuesday",
                 "Wednesday": "Wednesday",
                 "Thursday": "Thursday",
                 "Friday": "Friday",
                 "Saturday": "Saturday",
                 "Sunday": "Sunday"}

VieDate = {"Thứ hai": "Thứ Hai",
           "Thứ ba": "Thứ ba",
           "Thứ tư": "Thứ tư",
           "Thứ năm": "Thứ năm",
           "Thứ sáu": "Thứ sáu",
           "Thứ bảy": "Thứ bảy",
           "Chủ nhật": "Chủ nhật",
           "Monday": "Thứ hai",
           "Tuesday": "Thứ ba",
           "Wednesday": "Thứ tư",
           "Thursday": "Thứ năm",
           "Friday": "Thứ sáu",
           "Saturday": "Thứ bảy",
           "Sunday": "Chủ nhật"}


class SerialThread(QtCore.QThread):
    dataChanged = QtCore.pyqtSignal(str)

    def run(self):
        while True:
            try:
                ser = Serial(port='/dev/ttyUSB0', baudrate=115200)
                rfid = str(ser.readline())
                if rfid != "b''":
                    rfid = rfid.split(":  ")[1].split("\\")[0]
                    print(rfid)
                    self.dataChanged.emit(rfid)
            except:
                continue


class WarningF(Warning.Ui_Dialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        # Appear position
        size = Dialog.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = int((desktopSize.height() / 2) - (size.height() / 2))
        left = int((desktopSize.width() / 2) - (size.width() / 2))
        Dialog.move(left, top)


class ReturnF(ReturnFrame.Ui_Dialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        # Appear position
        size = Dialog.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = int((desktopSize.height() / 2) - (size.height() / 2))
        left = int((desktopSize.width() / 2) - (size.width() / 2))
        Dialog.move(left, top)
        # Setup date
        today = VieDate[datetime.datetime.now().strftime("%A")]
        date = datetime.datetime.now().strftime(today + ", ngày %d tháng %m")
        self.date.setText(date)


class BorrowF(BorrowFrame.Ui_Dialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        # Appear position
        size = Dialog.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = int((desktopSize.height() / 2) - (size.height() / 2))
        left = int((desktopSize.width() / 2) - (size.width() / 2))
        Dialog.move(left, top)
        # Setup date
        today = VieDate[datetime.datetime.now().strftime("%A")]
        date = datetime.datetime.now().strftime(today + ", ngày %d tháng %m")
        self.date.setText(date)

        self.label.setVisible(False)


class MainF(MainFrame.Ui_MainWindow):
    def __init__(self):
        self.serialThread = SerialThread()
        self.numberW = 0
        self.numberB = 0
        self.numberR = 0

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # setup interface
        self.success.setVisible(False)
        GIF = QMovie("Images/animation.gif")
        self.label.setMovie(GIF)
        GIF.start()
        # Appear position
        size = MainWindow.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = int((desktopSize.height() / 2) - (size.height() / 2))
        left = int((desktopSize.width() / 2) - (size.width() / 2))
        MainWindow.move(left, top)

        # timeThread
        # self.timeThread.start()  # ------------------------------------------------------------------------------------
        today = VieDate[datetime.datetime.now().strftime("%A")]
        self.today.setText(today)
        date = datetime.datetime.now().strftime("ngày %d tháng %m năm 2022")
        self.date.setText(date)
        # Serial Thread
        self.serialThread.start()
        self.serialThread.dataChanged.connect(self.process)
        # Time to close Dialog
        # timeClose = Thread(target=self.CloseDialog)
        # timeClose.start()

    def closeSuccess(self):
        self.success.setVisible(False)

    def resetRemainTime(self):
        QtCore.QTimer.singleShot(29000, self.closeDialog)  # ------------------------------------------------------------
        if self.numberB == 1:
            GIF_ = QMovie("Images/countdown.gif")
            self.BorrowFr.remainTime.setMovie(GIF_)
            GIF_.start()
            self.timeShow = datetime.datetime.now().strftime("%M-%S")
        if self.numberR == 1:
            GIF_ = QMovie("Images/countdown.gif")
            self.ReturnFr.remainTime.setMovie(GIF_)
            GIF_.start()
            self.timeShow = datetime.datetime.now().strftime("%M-%S")

    def closeDialog(self):
        lastsecond = int(self.timeShow.split("-")[1])
        lastminute = int(self.timeShow.split("-")[0])
        thissecond = int(datetime.datetime.now().strftime("%S"))
        thisminute = int(datetime.datetime.now().strftime("%M"))

        print(lastsecond)
        print(thissecond)
        print(thisminute)
        print(lastminute)

        if lastsecond > 29 and thissecond > lastsecond - 32 and thisminute == lastminute + 1: #-------------------------
            if self.numberB == 1 and self.numberW == 0:
                self.BorrowDialog.close()
            if self.numberR == 1:
                self.ReturnDialog.close()

        if lastsecond < 30 and thissecond > lastsecond + 28 and thisminute == lastminute: #-----------------------------
            if self.numberB == 1 and self.numberW == 0:
                self.BorrowDialog.close()
            if self.numberR == 1:
                self.ReturnDialog.close()

    # Process with RFID:
    def process(self, rfid):
        self.RFID = None
        self.BorrowDialog = QDialog()
        self.BorrowFr = BorrowF()
        self.BorrowFr.setupUi(self.BorrowDialog)

        self.ReturnDialog = QDialog()
        self.ReturnFr = ReturnF()
        self.ReturnFr.setupUi(self.ReturnDialog)

        try:
            self.name = JsonFirestore.loadRFIDname(rfid)
            self.mail = JsonFirestore.loadRFIDmail(rfid)

            self.RFID = rfid
            self.Last = db.collection("History").document(self.mail)\
                .collection("EquipmentState").document("Last").get().to_dict()
            print(str(self.Last))
            if self.Last["LastState"] == "Borrowed":
                self.setupRdialog()
            else:
                if self.Last["LastState"] == "Returned":
                    self.setupBdialog()
        except:
            print("RFID is not exist!")

    def setupBdialog(self):
        today = VieDate[datetime.datetime.now().strftime("%A")]
        self.BorrowFr.today.setText(today)
        date = datetime.datetime.now().strftime("ngày %d tháng %m năm 2022")
        self.BorrowFr.date.setText(date)
        note = " ..."
        self.BorrowFr.you_borrowed.setVisible(False)
        self.BorrowFr.refirm.setText(note)
        # setup account
        self.mail = JsonFirestore.loadRFIDmail(self.RFID)
        self.name = JsonFirestore.loadRFIDname(self.RFID)
        self.BorrowFr.name.setText(self.name)
        self.BorrowFr.email.setText("Email: " + self.mail.replace("_", ".").replace(".sis", "@sis"))

        re_minute = int(datetime.datetime.now().strftime("%M"))
        re_hour = int(datetime.datetime.now().strftime("%H"))
        i_minute = re_minute + 30 if re_minute < 30 else re_minute - 30
        i_hour = re_hour if re_minute < 30 else re_hour + 1
        str_minute = str(i_minute) if i_minute > 9 else f"0{i_minute}"
        str_hour = str(i_hour) if i_hour > 9 else f"0{i_hour}"
        timenow = str_hour + "-" + str_minute
        today = str(translateDate[str(datetime.datetime.now().strftime("%A"))])
        print("to day is :" + today)
        sections = JsonFirestore.readScheToday(self.RFID)
        self.check = 0
        for section in sections:
            section = JsonFirestore.readScheToday(self.RFID)[section]
            start = str(section["period"]).split("-")[0]
            end = str(section["period"]).split("-")[1]
            if (period[int(start)][0]) < timenow:
                if (period[int(end)][1]) > timenow:
                    self.check = 1
                    room = section["room"]
                    subject = section["subject"]

                    self.BorrowFr.room.setText("Phòng " + room + " - D6")
                    self.BorrowFr.subject.setText(subject)
                    self.BorrowFr.code.setText(str(random.randrange(100000, 999999)))
                    self.BorrowFr.label_.setText("|")
                    self.BorrowFr.start.setText(period[int(start)][0])
                    self.BorrowFr.end.setText(period[int(end)][1])

                    self.time_ = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
                    self.data = {
                        "borrow_nt": "_",
                        "return_nt": "_",
                        "borrow_tm": self.time_,
                        "return_tm": "_",
                        "period_tm": section["period"],
                        "teachroom": room,
                        "_subject_": subject
                    }

                    self.BorrowDialog.close()
                    self.numberB = 0
                    self.success.setVisible(True)
                    print("ok")
                    QtCore.QTimer.singleShot(1000, self.closeSuccess)
                    self.resetRemainTime()

                    print(room + " " + subject)
        if self.check == 0:
            self.BorrowFr.start.setText("")
            self.BorrowFr.end.setText("")
            self.BorrowFr.label_.setText("")
            self.BorrowFr.subject.setText("")
            self.BorrowFr.code.setText("")
            self.BorrowFr.room.setText("                  ...")

        self.BorrowFr.remote_cb.setChecked(False)
        self.BorrowFr.laser_cb.setChecked(False)
        self.BorrowFr.hdmi_cb.setChecked(False)
        self.BorrowFr.micro_cb.setChecked(False)

        self.resetRemainTime()
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(0)
        self.BorrowDialog.setGraphicsEffect(blur)
        GIF_ = QMovie("Images/countdown.gif")
        self.BorrowFr.remainTime.setMovie(GIF_)
        GIF_.start()
        # self.BorrowDialog.showFullScreen()
        self.BorrowDialog.showFullScreen()
        self.timeShow = datetime.datetime.now().strftime("%M-%S")
        QtCore.QTimer.singleShot(29500, self.closeDialog) # ------------------------------------------------------------
        self.numberB = 1
        self.BorrowFr.back.clicked.connect(self.BorrowDialog_close)
        self.BorrowFr.confirm.clicked.connect(self.Borrow)
        self.BorrowFr.continue_.clicked.connect(self.resetRemainTime)

        self.BorrowFr.rmt_btn.clicked.connect(self.changeStateRemoteCheckbox)
        self.BorrowFr.lsr_btn.clicked.connect(self.changeStateLaserCheckbox)
        self.BorrowFr.mcr_btn.clicked.connect(self.changeStateMicroCheckbox)
        self.BorrowFr.hdmi_btn.clicked.connect(self.changeStateHdmiCheckbox)

    def BorrowDialog_close(self):
        self.BorrowDialog.close()
        self.numberB = 0

    def Borrow(self):

        if self.BorrowFr.remote_cb.isChecked() \
                or self.BorrowFr.hdmi_cb.isChecked() \
                or self.BorrowFr.laser_cb.isChecked() \
                or self.BorrowFr.micro_cb.isChecked():
            if self.check == 1:
                self.data.update({"ac_remote": "Borrowed" if self.BorrowFr.remote_cb.isChecked() else "_",
                                  "laser_pen": "Borrowed" if self.BorrowFr.laser_cb.isChecked() else "_",
                                  "mcr_phone": "Borrowed" if self.BorrowFr.micro_cb.isChecked() else "_",
                                  "hdmi_wire": "Borrowed" if self.BorrowFr.hdmi_cb.isChecked() else "_", })
                self.bits = ""
                bit0 = "1" if self.BorrowFr.remote_cb.isChecked() else "0"
                bit1 = "1" if self.BorrowFr.hdmi_cb.isChecked() else "0"
                bit2 = "1" if self.BorrowFr.laser_cb.isChecked() else "0"
                bit3 = "1" if self.BorrowFr.micro_cb.isChecked() else "0"
                self.bits = bit0 + bit1 + bit2 + bit3
                self.last = {
                    "Bits_AHLM": self.bits,
                    "LastCheck": self.time_,
                    "LastState": "Borrowed"
                }
                db.collection("History").document(self.mail).collection("EquipmentState") \
                    .document(self.time_).set(self.data)
                db.collection("History").document(self.mail).collection("EquipmentState") \
                    .document("Last").set(self.last)
                self.BorrowDialog.close()
                self.numberB = 0
                self.success.setVisible(True)
                print("ok")
                QtCore.QTimer.singleShot(1000, self.closeSuccess)
            if self.check == 0:
                self.teachingNow = {}
                timenow = datetime.datetime.now().strftime("%H-%M")
                today = str(translateDate[str(datetime.datetime.now().strftime("%A"))])
                ids = JsonFirestore.loadRFID()
                for id in ids:
                    id = JsonFirestore.loadRFID()[id]
                    sections = id[today]
                    for section in sections:
                        section = sections[section]
                        start = str(section["period"]).split("-")[0]
                        end = str(section["period"]).split("-")[1]
                        if (period[int(start)][0]) < timenow:
                            if (period[int(end)][1]) > timenow:
                                self.teachingNow.update({section["room"]: {"name": id["name"],
                                                                           "subject": section["subject"],
                                                                           "period": section["period"],
                                                                           "room": section["room"]}})

                self.WarningDialog = QDialog()
                self.WarningFr = WarningF()
                self.WarningFr.setupUi(self.WarningDialog)

                blur = QGraphicsBlurEffect()
                blur.setBlurRadius(20)
                self.BorrowDialog.setGraphicsEffect(blur)
                self.WarningFr.teacher.setText("")
                self.WarningFr.room.setText("")
                self.WarningDialog.setWindowFlag(Qt.FramelessWindowHint, True)
                self.WarningDialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

                self.resetRemainTime()
                self.WarningFr.room.setText("")
                self.WarningFr.instead_cb.setChecked(False)
                self.WarningFr.compen_cb.setChecked(False)
                # self.WarningDialog.showFullScreen()
                self.WarningDialog.showFullScreen()
                self.numberW = 1

                self.WarningFr.zero.clicked.connect(self.addZero)
                self.WarningFr.one.clicked.connect(self.addOne)
                self.WarningFr.two.clicked.connect(self.addTwo)
                self.WarningFr.three.clicked.connect(self.addThree)
                self.WarningFr.four.clicked.connect(self.addFour)
                self.WarningFr.five.clicked.connect(self.addFive)
                self.WarningFr.six.clicked.connect(self.addSix)
                self.WarningFr.seven.clicked.connect(self.addSeven)
                self.WarningFr.eight.clicked.connect(self.addEight)
                self.WarningFr.nine.clicked.connect(self.addNine)

                self.WarningFr.compensation.clicked.connect(self.changeStateCompen)
                self.WarningFr.instead.clicked.connect(self.changeStateInstead)

                self.WarningFr.Del.clicked.connect(self.DelNum)
                self.WarningFr.OK.clicked.connect(self.pushData)
                self.WarningFr.back.clicked.connect(self.closeWarning)
        else:
            self.BorrowFr.label.setVisible(True)
            QtCore.QTimer.singleShot(1000, self.hideWarn)

    def hideWarn(self):
        self.BorrowFr.label.setVisible(False)

    def pushData(self):
        if self.WarningFr.instead_cb.isChecked():
            if self.WarningFr.teacher.text() != "" and self.WarningFr.teacher.text() != "Phòng học trống tiết!":
                self.WarningFr.OK.setEnabled(False)
                time_ = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
                data = {
                    "ac_remote": "Borrowed" if self.BorrowFr.remote_cb.isChecked() else "_",
                    "laser_pen": "Borrowed" if self.BorrowFr.laser_cb.isChecked() else "_",
                    "mcr_phone": "Borrowed" if self.BorrowFr.micro_cb.isChecked() else "_",
                    "hdmi_wire": "Borrowed" if self.BorrowFr.hdmi_cb.isChecked() else "_",
                    "borrow_nt": "Dạy thay GV." + self.teachingNow[self.WarningFr.room.text()]["name"],
                    "return_nt": "_",
                    "borrow_tm": time_,
                    "return_tm": "_",
                    "period_tm": self.teachingNow[self.WarningFr.room.text()]["period"],
                    "teachroom": self.teachingNow[self.WarningFr.room.text()]["room"],
                    "_subject_": self.teachingNow[self.WarningFr.room.text()]["subject"]
                }

                self.bits = ""
                bit0 = "1" if self.BorrowFr.remote_cb.isChecked() else "0"
                bit1 = "1" if self.BorrowFr.hdmi_cb.isChecked() else "0"
                bit2 = "1" if self.BorrowFr.laser_cb.isChecked() else "0"
                bit3 = "1" if self.BorrowFr.micro_cb.isChecked() else "0"
                self.bits = bit0 + bit1 + bit2 + bit3
                self.last = {
                    "Bits_AHLM": self.bits,
                    "LastCheck": time_,
                    "LastState": "Borrowed"
                }

                db.collection("History").document(self.mail).collection("EquipmentState") \
                    .document(time_).set(data)
                db.collection("History").document(self.mail).collection("EquipmentState") \
                    .document("Last").set(self.last)
                self.WarningDialog.close()
                self.numberW = 0
                self.BorrowDialog.close()
                self.numberB = 0
                self.success.setVisible(True)
                print("ok")
                QtCore.QTimer.singleShot(1000, self.closeSuccess)
            else:
                self.WarningFr.teacher.setText("Phòng học trống tiết!")

        if self.WarningFr.compen_cb.isChecked():
            self.WarningFr.OK.setEnabled(False)
            time_ = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
            data = {
                "ac_remote": "Borrowed" if self.BorrowFr.remote_cb.isChecked() else "_",
                "laser_pen": "Borrowed" if self.BorrowFr.laser_cb.isChecked() else "_",
                "mcr_phone": "Borrowed" if self.BorrowFr.micro_cb.isChecked() else "_",
                "hdmi_wire": "Borrowed" if self.BorrowFr.hdmi_cb.isChecked() else "_",
                "borrow_nt": "Dạy bù",
                "return_nt": "_",
                "borrow_tm": time_,
                "return_tm": "_",
                "period_tm": "_",
                "teachroom": self.WarningFr.room.text(),
                "_subject_": "_"
            }

            self.bits = ""
            bit0 = "1" if self.BorrowFr.remote_cb.isChecked() else "0"
            bit1 = "1" if self.BorrowFr.hdmi_cb.isChecked() else "0"
            bit2 = "1" if self.BorrowFr.laser_cb.isChecked() else "0"
            bit3 = "1" if self.BorrowFr.micro_cb.isChecked() else "0"
            self.bits = bit0 + bit1 + bit2 + bit3
            self.last = {
                "Bits_AHLM": self.bits,
                "LastCheck": time_,
                "LastState": "Borrowed"
            }

            db.collection("History").document(self.mail).collection("EquipmentState") \
                .document(time_).set(data)
            db.collection("History").document(self.mail).collection("EquipmentState") \
                .document("Last").set(self.last)

            self.WarningDialog.close()
            self.numberW = 0
            self.BorrowDialog.close()
            self.numberB = 0
            self.success.setVisible(True)
            print("ok")
            QtCore.QTimer.singleShot(1000, self.closeSuccess)

    def changeStateCompen(self):
        self.WarningFr.compen_cb.setChecked(not self.WarningFr.compen_cb.isChecked())
        if self.WarningFr.instead_cb.isChecked():
            self.WarningFr.instead_cb.setChecked(not self.WarningFr.instead_cb.isChecked())
            self.WarningFr.teacher.setText("")

    def changeStateInstead(self):
        self.WarningFr.instead_cb.setChecked(not self.WarningFr.instead_cb.isChecked())
        if self.WarningFr.compen_cb.isChecked():
            self.WarningFr.compen_cb.setChecked(not self.WarningFr.compen_cb.isChecked())

    def addZero(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "0"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addOne(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "1"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addTwo(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "2"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addThree(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "3"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addFour(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "4"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addFive(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "5"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addSix(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "6"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addSeven(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "7"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addEight(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "8"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def addNine(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) < 3:
            text = self.WarningFr.room.text() + "9"
            self.WarningFr.room.setText(text)
        if len(text) == 3:
            if self.WarningFr.instead_cb.isChecked():
                try:
                    self.WarningFr.teacher.setText("GV." + self.teachingNow[text]["name"])
                except:
                    pass

    def DelNum(self):
        self.WarningFr.teacher.setText("")
        text = str(self.WarningFr.room.text())
        if len(text) > 0:
            self.WarningFr.room.setText(text[:-1])

    def closeWarning(self):
        self.resetRemainTime()
        self.numberW = 0
        self.WarningDialog.close()
        self.numberW = 0
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(0)
        self.BorrowDialog.setGraphicsEffect(blur)

    def setupRdialog(self):
        self.ReturnFr.refirm.setText("")
        self.ReturnFr.name.setText(self.name)
        self.ReturnFr.email.setText("Email: " + self.mail.replace("_", ".").replace(".sis", "@sis"))
        # setup interface
        note = ""
        if str(self.Last["Bits_AHLM"])[0] == "1":
            note = note + "     01 ĐIỀU KHIỂN" + "\n"
            self.ReturnFr.remote_cb.setChecked(True)
        if str(self.Last["Bits_AHLM"])[2] == "1":
            note = note + "     01 BÚT LASER" + "\n"
            self.ReturnFr.laser_cb.setChecked(True)
        if str(self.Last["Bits_AHLM"])[3] == "1":
            note = note + "     01 MÍC DI ĐỘNG" + "\n"
            self.ReturnFr.micro_cb.setChecked(True)
        if str(self.Last["Bits_AHLM"])[1] == "1":
            note = note + "     01 CÁP HDMI" + "\n"
            self.ReturnFr.hdmi_cb.setChecked(True)
        note = note + self.reformTime(str(self.Last["LastCheck"]))

        re_minute = int(datetime.datetime.now().strftime("%M"))
        re_hour = int(datetime.datetime.now().strftime("%H"))
        i_minute = re_minute + 30 if re_minute < 30 else re_minute - 30
        i_hour = re_hour if re_minute < 30 else re_hour + 1
        str_minute = str(i_minute) if i_minute > 9 else f"0{i_minute}"
        str_hour = str(i_hour) if i_hour > 9 else f"0{i_hour}"
        timenow = str_hour + "-" + str_minute
        today = str(translateDate[str(datetime.datetime.now().strftime("%A"))])
        print(today)
        sections = JsonFirestore.readScheToday(self.RFID)
        check = 0
        for section in sections:
            section = JsonFirestore.readScheToday(self.RFID)[section]
            start = str(section["period"]).split("-")[0]
            end = str(section["period"]).split("-")[1]
            if (period[int(start)][0]) < timenow:
                if (period[int(end)][1]) > timenow:
                    check = 1
                    room = section["room"]
                    subject = section["subject"]
                    self.ReturnFr.room.setText("Phòng " + room + " - D6")
                    self.ReturnFr.subject.setText(subject)
                    self.ReturnFr.code.setText(str(random.randrange(100000, 999999)))
                    self.BorrowFr.label_.setText("|")
                    self.ReturnFr.start.setText(period[int(start)][0])
                    self.ReturnFr.end.setText(period[int(end)][1])
        if check == 0:
            self.ReturnFr.start.setText("")
            self.ReturnFr.end.setText("")
            self.ReturnFr.label_.setText("")
            self.ReturnFr.subject.setText("")
            self.ReturnFr.code.setText("")
            self.ReturnFr.room.setText("                  ...")

        self.BorrowFr.refirm.setFontPointSize(9)
        self.ReturnFr.refirm.setText(note)
        self.ReturnFr.back.clicked.connect(self.ReturnDialog_close)
        self.ReturnFr.confirm.clicked.connect(self.Return)
        self.ReturnFr.continue_.clicked.connect(self.resetRemainTime)

        self.resetRemainTime()
        GIF_ = QMovie("Images/countdown.gif")
        self.ReturnFr.remainTime.setMovie(GIF_)
        GIF_.start()
        # self.ReturnDialog.showFullScreen()
        self.ReturnDialog.showFullScreen()
        self.timeShow = datetime.datetime.now().strftime("%M-%S")
        QtCore.QTimer.singleShot(29500, self.closeDialog) # ------------------------------------------------------------
        self.numberR = 1

    def ReturnDialog_close(self):
        self.ReturnDialog.close()
        self.numberR = 0

    def Return(self):
        self.ReturnFr.confirm.setEnabled(False)
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        db.collection("History").document(self.mail).collection("EquipmentState") \
            .document(self.Last["LastCheck"]).update({"return_tm": time})
        db.collection("History").document(self.mail).collection("EquipmentState") \
            .document("Last").update({"LastState": "Returned", "LastCheck": "_", "Bits_AHLM": "_"})

        self.ReturnDialog.close()
        self.numberR = 0
        self.success.setVisible(True)
        print("ok")
        QtCore.QTimer.singleShot(1000, self.closeSuccess)

    def reformTime(self, time):
        rfTime = ""
        time = time.split("-")
        rfTime = f'\n.. ngày {time[2]}/{time[1]}/{time[0]} lúc {time[3]}:{time[4]}'
        return rfTime

    def changeStateRemoteCheckbox(self):
        print(datetime.datetime.now())
        self.BorrowFr.remote_cb.setChecked(not self.BorrowFr.remote_cb.isChecked())
        today = VieDate[datetime.datetime.now().strftime("%A")]
        self.BorrowFr.today.setText(today)
        date = datetime.datetime.now().strftime("ngày %d tháng %m năm 2022")
        self.BorrowFr.date.setText(date)
        note = ""
        if self.BorrowFr.remote_cb.isChecked():
            note = note + "     01 ĐIỀU KHIỂN" + "\n"
        if self.BorrowFr.laser_cb.isChecked():
            note = note + "     01 BÚT LASER" + "\n"
        if self.BorrowFr.hdmi_cb.isChecked():
            note = note + "     01 CÁP HDMI" + "\n"
        if self.BorrowFr.micro_cb.isChecked():
            note = note + "     01 MÍC DI ĐỘNG" + "\n"

        if self.BorrowFr.remote_cb.isChecked() or self.BorrowFr.laser_cb.isChecked() or self.BorrowFr.micro_cb.isChecked() or self.BorrowFr.hdmi_cb.isChecked():
            self.BorrowFr.you_borrowed.setVisible(True)
            self.BorrowFr.refirm.setFontPointSize(9)
            self.BorrowFr.refirm.setText(note)
        else:
            self.BorrowFr.you_borrowed.setVisible(False)
            self.BorrowFr.refirm.setText(" ...")

    def changeStateLaserCheckbox(self):
        self.BorrowFr.laser_cb.setChecked(not self.BorrowFr.laser_cb.isChecked())
        today = VieDate[datetime.datetime.now().strftime("%A")]
        date = datetime.datetime.now().strftime(today + ", ngày %d/%m, lúc %H:%M")
        self.BorrowFr.timeline.setText(date)
        note = ""
        if self.BorrowFr.remote_cb.isChecked():
            note = note + "     01 ĐIỀU KHIỂN" + "\n"
        if self.BorrowFr.laser_cb.isChecked():
            note = note + "     01 BÚT LASER" + "\n"
        if self.BorrowFr.hdmi_cb.isChecked():
            note = note + "     01 CÁP HDMI" + "\n"
        if self.BorrowFr.micro_cb.isChecked():
            note = note + "     01 MÍC DI ĐỘNG" + "\n"

        if self.BorrowFr.remote_cb.isChecked() or self.BorrowFr.laser_cb.isChecked() or self.BorrowFr.micro_cb.isChecked() or self.BorrowFr.hdmi_cb.isChecked():
            self.BorrowFr.you_borrowed.setVisible(True)
            self.BorrowFr.refirm.setFontPointSize(9)
            self.BorrowFr.refirm.setText(note)
        else:
            self.BorrowFr.you_borrowed.setVisible(False)
            self.BorrowFr.refirm.setText(" ...")

    def changeStateMicroCheckbox(self):
        self.BorrowFr.micro_cb.setChecked(not self.BorrowFr.micro_cb.isChecked())
        today = VieDate[datetime.datetime.now().strftime("%A")]
        date = datetime.datetime.now().strftime(today + ", ngày %d/%m, lúc %H:%M")
        self.BorrowFr.timeline.setText(date)
        note = ""
        if self.BorrowFr.remote_cb.isChecked():
            note = note + "     01 ĐIỀU KHIỂN" + "\n"
        if self.BorrowFr.laser_cb.isChecked():
            note = note + "     01 BÚT LASER" + "\n"
        if self.BorrowFr.hdmi_cb.isChecked():
            note = note + "     01 CÁP HDMI" + "\n"
        if self.BorrowFr.micro_cb.isChecked():
            note = note + "     01 MÍC DI ĐỘNG" + "\n"

        if self.BorrowFr.remote_cb.isChecked() or self.BorrowFr.laser_cb.isChecked() or self.BorrowFr.micro_cb.isChecked() or self.BorrowFr.hdmi_cb.isChecked():
            self.BorrowFr.you_borrowed.setVisible(True)
            self.BorrowFr.refirm.setFontPointSize(9)
            self.BorrowFr.refirm.setText(note)
        else:
            self.BorrowFr.you_borrowed.setVisible(False)
            self.BorrowFr.refirm.setText(" ...")

    def changeStateHdmiCheckbox(self):
        self.BorrowFr.hdmi_cb.setChecked(not self.BorrowFr.hdmi_cb.isChecked())
        today = VieDate[datetime.datetime.now().strftime("%A")]
        date = datetime.datetime.now().strftime(today + ", ngày %d/%m, lúc %H:%M")
        self.BorrowFr.timeline.setText(date)
        note = ""
        if self.BorrowFr.remote_cb.isChecked():
            note = note + "     01 ĐIỀU KHIỂN" + "\n"
        if self.BorrowFr.laser_cb.isChecked():
            note = note + "     01 BÚT LASER" + "\n"
        if self.BorrowFr.hdmi_cb.isChecked():
            note = note + "     01 CÁP HDMI" + "\n"
        if self.BorrowFr.micro_cb.isChecked():
            note = note + "     01 MÍC DI ĐỘNG" + "\n"

        if self.BorrowFr.remote_cb.isChecked() or self.BorrowFr.laser_cb.isChecked() or self.BorrowFr.micro_cb.isChecked() or self.BorrowFr.hdmi_cb.isChecked():
            self.BorrowFr.you_borrowed.setVisible(True)
            self.BorrowFr.refirm.setFontPointSize(9)
            self.BorrowFr.refirm.setText(note)
        else:
            self.BorrowFr.you_borrowed.setVisible(False)
            self.BorrowFr.refirm.setText(" ...")


def main():
    window = QMainWindow()
    ui = MainF()
    ui.setupUi(window)
    # window.showFullScreen()
    window.showFullScreen()
    ui.pushButton.clicked.connect(window.close)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
