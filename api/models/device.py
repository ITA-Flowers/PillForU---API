from flask import jsonify

class Device:
    def __init__(self, uid = None):
        self.uid = uid

    def get_json(self, json_obj = True):
        json_data = []
        content = {'uuid': self.uid}
        
        json_data.append(content)

        if json_obj:
            return jsonify(json_data)

        return content
