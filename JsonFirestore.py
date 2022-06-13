import datetime
import json

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

def readScheToday(rfid):
    fS = open("JsonFile/Schedule.json", "r")
    data = json.load(fS)[rfid][translateDate[datetime.datetime.now().strftime("%A")]]
    fS.close()
    return data


def loadRFIDname(rfid):
    fS = open("JsonFile/Schedule.json", "r")
    data = json.load(fS)[rfid]["name"]
    fS.close()
    return data


def loadRFIDmail(rfid):
    fS = open("JsonFile/Schedule.json", "r")
    data = json.load(fS)[rfid]["mail"]
    fS.close()
    return data


def loadRFID():
    fS = open("JsonFile/Schedule.json", "r")
    data = json.load(fS)
    fS.close()
    return data
