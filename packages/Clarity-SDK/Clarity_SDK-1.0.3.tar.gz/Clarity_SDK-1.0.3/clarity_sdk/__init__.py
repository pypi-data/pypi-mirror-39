import requests
import json

API_KEY = ''


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
