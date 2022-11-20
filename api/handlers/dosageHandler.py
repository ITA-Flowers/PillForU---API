from flask import request, Response
from flask_restful import Resource
import json

import api.codes.errors as errors
import api.codes.successes as successes
import api.database.db as db
import api.models.dosage as mddos

# @app.route('/dosages')
class DosageManager(Resource):
    @staticmethod
    def get():
        try: id = request.json.get('id').strip()
        except Exception as _ : id = None
        
        if not id:
        
            try: device_uid = request.json.get('device_uid').strip()
            except Exception as _: device_uid = None

            if not device_uid:
                try: caretaker_uuid = request.json.get('caretaker_uuid').strip()
                except Exception as _: caretaker_uuid = None

                if not caretaker_uuid:
                    try: pupil_uuid = request.json.get('pupil_uuid').strip()
                    except Exception as _: pupil_uuid = None

                    if not pupil_uuid:
                        # Get all users
                        dosages = db.get_dosages()
                        if dosages is None:
                            resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
                        else:
                            resp = Response(json.dumps(dosages), status=200)
                            
                        resp.headers.set('Access-Control-Allow-Origin', '*')
                        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
                        return resp

                    dosages = db.get_dosages_by_pupil_uuid(pupil_uuid)
                    if dosages is None:
                        resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
                    else:
                        resp = Response(json.dumps(dosages), status=200)
                    
                    resp.headers.set('Access-Control-Allow-Origin', '*')
                    resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                    resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
                    return resp

                dosages = db.get_dosages_by_caretaker_uuid(caretaker_uuid)
                if dosages is None:
                    resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
                else:
                    resp = Response(json.dumps(dosages), status=200)
                
                resp.headers.set('Access-Control-Allow-Origin', '*')
                resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
                return resp

            dosages = db.get_dosages_by_devuid(device_uid)

            if dosages is None:
                resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
            else:
                resp = Response(json.dumps(dosages), status=200)
            
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
            
        dosage = db.get_dosage_by_id(id)
            
        if dosage is None:
            resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
        else:
            resp = Response(json.dumps(dosage), status=200)
        
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp
        
        
    @staticmethod
    def post():
        try:
            # Get user data
            caretaker_uuid, pupil_uuid, device_uid, med_name, pills_count, when_day, when_time, until_date = (
                request.json.get('caretaker_uuid').strip(),
                request.json.get('pupil_uuid').strip(),
                request.json.get('device_uid').strip(),
                request.json.get('med_name').strip(),
                request.json.get('pills_count'),
                request.json.get('when_day').strip(),
                request.json.get('when_time').strip(),
                request.json.get('until_date').strip()
            )
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        if id is None or caretaker_uuid is None or pupil_uuid is None or device_uid is None or med_name is None or pills_count is None or when_day is None or when_time is None or until_date is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        if when_day == 'monday':        when_day = mddos.DAY.MONDAY
        elif when_day == 'tuesday':     when_day = mddos.DAY.TUESDAY
        elif when_day == 'wednesday':   when_day = mddos.DAY.WEDNESDAY
        elif when_day == 'thursday':    when_day = mddos.DAY.THURSDAY
        elif when_day == 'friday':      when_day = mddos.DAY.FRIDAY
        elif when_day == 'saturday':    when_day = mddos.DAY.SATURDAY
        elif when_day == 'sunday':      when_day = mddos.DAY.SUNDAY
        else: 
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
            
        # valid_role, role = Register._validate_role(role)
        # valid_phone_number = Register._validate_phone_number(phone_number)
        
        # if not valid_role or not valid_phone_number:
        #     return errors.INVALID_INPUT_422

        dosage = mddos.Dosage(caretaker_uuid, pupil_uuid, device_uid, med_name, int(pills_count), when_day, when_time, until_date)

        db.add_dosage(dosage)
        
        resp = Response(json.dumps(successes.RESOURCE_ADDED[0]), status=successes.RESOURCE_ADDED[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp
    
    @staticmethod
    def put():
        try:
            # Get user data
            id, caretaker_uuid, pupil_uuid, device_uid, med_name, pills_count, when_day, when_time, until_date = (
                request.json.get('id'),
                request.json.get('caretaker_uuid').strip(),
                request.json.get('pupil_uuid').strip(),
                request.json.get('device_uid').strip(),
                request.json.get('med_name').strip(),
                request.json.get('pills_count'),
                request.json.get('when_day').strip(),
                request.json.get('when_time').strip(),
                request.json.get('until_date').strip()
            )
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        if id is None or caretaker_uuid is None or pupil_uuid is None or device_uid is None or med_name is None or pills_count is None or when_day is None or when_time is None or until_date is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        if when_day == 'monday':        when_day = mddos.DAY.MONDAY
        elif when_day == 'tuesday':     when_day = mddos.DAY.TUESDAY
        elif when_day == 'wednesday':   when_day = mddos.DAY.WEDNESDAY
        elif when_day == 'thursday':    when_day = mddos.DAY.THURSDAY
        elif when_day == 'friday':      when_day = mddos.DAY.FRIDAY
        elif when_day == 'saturday':    when_day = mddos.DAY.SATURDAY
        elif when_day == 'sunday':      when_day = mddos.DAY.SUNDAY
        else: 
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
            
        # valid_role, role = Register._validate_role(role)
        # valid_phone_number = Register._validate_phone_number(phone_number)
        
        # if not valid_role or not valid_phone_number:
        #     return errors.INVALID_INPUT_422

        dosage = mddos.Dosage(caretaker_uuid, pupil_uuid, device_uid, med_name, int(pills_count), when_day, when_time, until_date, id)

        if db.update_dosage(dosage):
            resp = Response(json.dumps(successes.RESOURCE_UPDATED[0]), status=successes.RESOURCE_UPDATED[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp
    
    
    @staticmethod
    def delete():
        try:
            id = request.json.get('id')
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Check if any param is none
        if id is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Get user if it is existed
        dosage = db.get_dosage_by_id(id)

        # Check if user is not existed
        if dosage is None:
            resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        id = dosage['id']
        
        db.delete_dosage(id)
        
        resp = Response(json.dumps(successes.RESOURCE_DELETED[0]), status=successes.RESOURCE_DELETED[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp