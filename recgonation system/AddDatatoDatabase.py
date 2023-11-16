import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-1ab24-default-rtdb.firebaseio.com/"
})

ref = db.reference('staff')

data = {
    "1234":
        {
            "name": "Mahmud Ibrahim",
            "unit": "Automation",
            "Dept": "CIO",
            "last_attendance_time": "2022-12-11 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)