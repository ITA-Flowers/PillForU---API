from flask import request, Response
from flask_restful import Resource
import json

import api.database.db as db
import api.codes.errors as errors
import api.codes.successes as successes
import api.models.device as mddev

class DeviceManager(Resource):
    @staticmethod
    def get():
        try: uuid = request.json.get('uid').strip()
        except Exception as _: uuid = None

        if not uuid:
            devices = db.get_devices()
            resp = Response(json.dumps(devices), status=200)
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        # Get user by uuid
        device = db.get_device_by_uid(uuid)
        
        # If user does not exists
        if device is None:
            resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        else:
            resp = Response(json.dumps(device), status=200)
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
    @staticmethod
    def post():
        try: uid = request.json.get('uid').strip()
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        if uid is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        dev = db.get_device_by_uid(uid)

        if dev is not None:
            resp = Response(json.dumps(errors.ALREADY_EXIST[0]), status=errors.ALREADY_EXIST[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp
        
        dev = mddev.Device(uid=uid)
        
        db.add_device(dev)

        resp = Response(json.dumps(successes.RESOURCE_ADDED[0]), status=successes.RESOURCE_ADDED[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp
        
    @staticmethod
    def delete():
        try:
            uid = request.json.get('uid').strip()
        except Exception as why:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        if uid is None:
            resp = Response(json.dumps(errors.INVALID_INPUT[0]), status=errors.INVALID_INPUT[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        dev = db.get_device_by_uid(uid)

        if dev is None:
            resp = Response(json.dumps(errors.NOT_FOUND[0]), status=errors.NOT_FOUND[1])
            resp.headers.set('Access-Control-Allow-Origin', '*')
            resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
            return resp

        uid = dev['uid']
        
        db.delete_device(uid)
        
        resp = Response(json.dumps(successes.RESOURCE_DELETED[0]), status=successes.RESOURCE_DELETED[1])
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return resp
    