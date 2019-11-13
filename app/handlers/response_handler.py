import json


class ResponseHandler(object):

    @staticmethod
    def return_result(message, code, data):
        result = {
            "code": code,
            "msg": message,
            "data": data
        }
        return json.dumps(result)

    @staticmethod
    def success_json(data):
        result = {
            "code": 200,
            "msg": 'ok',
            "data": data
        }
        return result
