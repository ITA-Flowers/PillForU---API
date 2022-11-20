import datetime
from enum import Enum
from flask import jsonify

class DAY(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Dosage:
    def __init__(self, caretaker_uuid : str, 
                 pupil_uuid : str, 
                 device_uid : str, 
                 med_name : str, 
                 pills_count : int, 
                 when_day : DAY, 
                 when_time : str, 
                 until_date: str, 
                 id = None):
        self.id = id
        self.caretaker_uuid = caretaker_uuid
        self.pupil_uuid = pupil_uuid
        self.device_uid = device_uid
        self.med_name = med_name
        self.pills_count = pills_count
        self.when_day = when_day
        self.when_time = when_time
        self.until_date = until_date
        
    def get_json(self, json_obj = True):
        json_data = []
        content = {'id': self.id, 
                   'caretaker_uuid': self.caretaker_uuid,
                   'pupil_uuid': self.pupil_uuid,
                   'device_uid': self.device_uid,
                   'med_name': self.med_name,
                   'pills_count': self.pills_count,
                   'when_day': self.when_day,
                   'when_time': self.when_time,
                   'until_date': self.until_date 
                   }
        
        json_data.append(content)

        if json_obj:
            return jsonify(json_data)

        return content
        