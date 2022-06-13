import json

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class CreateScheduleJson:
    def runit(self):
        Schedule = {}
        rfids = db.collection("RFID").get()
        for rfid in rfids:
            data = {}
            name = db.collection("RFID").document(rfid.id).get().to_dict()["name"]
            mail = db.collection("RFID").document(rfid.id).get().to_dict()["email"]
            data.update({"name": name})
            data.update({"mail": mail})
            try:
                sections = db.collection("RFID").document(rfid.id).collection("Teaching") \
                    .document("schedule").collection("Monday").get()
                thisdata = {}
                for section in sections:
                    schedule = section.to_dict()
                    thisdata.update({section.id: schedule})
                data.update({"Monday": thisdata})
            except:
                pass

            try:
                sections = db.collection("RFID").document(rfid.id).collection("Teaching") \
                    .document("schedule").collection("Tuesday").get()
                thisdata = {}
                for section in sections:
                    schedule = section.to_dict()
                    thisdata.update({section.id: schedule})
                data.update({"Tuesday": thisdata})
            except:
                pass

            try:
                sections = db.collection("RFID").document(rfid.id).collection("Teaching") \
                    .document("schedule").collection("Wednesday").get()
                thisdata = {}
                for section in sections:
                    schedule = section.to_dict()
                    thisdata.update({section.id: schedule})
                data.update({"Wednesday": thisdata})
            except:
                pass

            try:
                sections = db.collection("RFID").document(rfid.id).collection("Teaching") \
                    .document("schedule").collection("Thursday").get()
                thisdata = {}
                for section in sections:
                    schedule = section.to_dict()
                    thisdata.update({section.id: schedule})
                data.update({"Thursday": thisdata})
            except:
                pass

            try:
                sections = db.collection("RFID").document(rfid.id).collection("Teaching") \
                    .document("schedule").collection("Friday").get()
                thisdata = {}
                for section in sections:
                    schedule = section.to_dict()
                    thisdata.update({section.id: schedule})
                data.update({"Friday": thisdata})
            except:
                pass

            try:
                sections = db.collection("RFID").document(rfid.id).collection("Teaching") \
                    .document("schedule").collection("Saturday").get()
                thisdata = {}
                for section in sections:
                    schedule = section.to_dict()
                    thisdata.update({section.id: schedule})
                data.update({"Saturday": thisdata})
            except:
                pass

            try:
                sections = db.collection("RFID").document(rfid.id).collection("Teaching") \
                    .document("schedule").collection("Sunday").get()
                thisdata = {}
                for section in sections:
                    schedule = section.to_dict()
                    thisdata.update({section.id: schedule})
                data.update({"Sunday": thisdata})
            except:
                pass
            Schedule.update({rfid.id: data})

        f = open("JsonFile/Schedule.json", "w")
        f.write(json.dumps(Schedule, indent=2))
        f.close()


def loadSche():
    dt = CreateScheduleJson()
    dt.runit()


loadSche()
