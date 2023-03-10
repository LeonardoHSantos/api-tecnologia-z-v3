import json


class ConvertData:
    def convert_to_json(data):
        return json.loads(data)
    
    def convert_to_dumps(data):
        return json.dumps(data).replace("'", '"')
    
    def convert_to_dict(**kwargs):
        return kwargs