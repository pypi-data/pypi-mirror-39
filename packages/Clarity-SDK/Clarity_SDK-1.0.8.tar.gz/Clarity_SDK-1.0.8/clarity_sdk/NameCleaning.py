import requests
import json
from clarity_sdk import API_KEY
def clean_name(source_string, exist_prefix=True, exist_suffix=True, exist_middle_name=True):
    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string, exist_prefix, exist_suffix, exist_middle_name]
    parametersTypeList = ['System.String', 'System.Boolean', 'System.Boolean', 'System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload = {"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/cleanname'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    name_object = NameEntity(parsed_json)
    return name_object

class NameEntity(object):
    """docstring for ParsedName"""
    first_name = ''
    first_initial = ''
    last_name = ''
    last_initial = ''
    middle_name = ''
    middle_initial = ''
    name_string = ''
    prefix = ''
    suffix = ''

    def __init__(self, myjson):
        myjson['output']
        name_dict = {}
        for val in myjson['output']:
            for key,value in val.items():
                name_dict[key]=value

        self.first_name = name_dict['First']
        self.first_initial = name_dict['FirstInitial']
        self.last_name = name_dict['Last']
        self.last_initial = name_dict['LastInitial']
        self.middle_name = name_dict['Middle']
        self.middle_initial = name_dict['MiddleInitial']
        self.name_string = name_dict['NameString']
        self.prefix = name_dict['Prefix']
        self.suffix = name_dict['Suffix']
