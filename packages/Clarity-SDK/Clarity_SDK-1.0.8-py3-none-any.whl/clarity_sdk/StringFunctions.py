import requests
import json
from clarity_sdk import API_KEY

def after(source_string, regex_pattern, return_all_on_no_match = False):
    """Returns a string containing everything in SourceString after the first instance of RegExPattern."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_pattern = regex_pattern.replace("\\","\\\\")
    parametersValueList = [source_string, regex_pattern, return_all_on_no_match]
    parametersTypeList = ['System.String', 'System.String', 'System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/after'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def before(source_string, regex_pattern, return_all_on_no_match = False):
    """Returns a string containing everything in SourceString before the first instance of RegExPattern."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_pattern = regex_pattern.replace("\\","\\\\")
    parametersValueList = [source_string, regex_pattern,return_all_on_no_match]
    parametersTypeList = ['System.String', 'System.String','System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/before'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def best_match(source_string, string_list):
    """Determines the best match betwring the supplied MatchString and a List(of String) based on the levenstein distance between the strings."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    string_list = [s.replace('\\', '\\\\') for s in string_list]
    parametersValueList = [source_string, string_list]
    parametersTypeList = ['System.String', 'LS']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload = {'parameters': jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/bestmatch'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json

def clean_html(source_string):
    """Returns the HTMLData string with all HTML tags removed and escaped characters converted."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/cleanhtml'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def html_decode(source_string):
    """Returns the HTMLData string with all HTML tags removed and escaped characters converted."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/htmldecode'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def html_encode(source_string):
    """Returns a String with HTML special characters replaced with their encode characters."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/htmlencode'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def lev_distance(source_string, compare_string):
    """Returns the Levenstein distance between two strings.  If strings are over 1000 characters, only the first 1000 will be evaluated."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    compare_string = compare_string.replace("\\","\\\\")
    parametersValueList = [source_string, compare_string]
    parametersTypeList = ['System.String','System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/levdistance'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def md5(source_string):
    """Returns an MD5 hash of the specified string."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/md5'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def regex_chunk(source_string, regex_string, case_sensitive=False, RemoveEmpty=False):
    """If RegExPattern contains a capture group the returned values will alternate between data between the pattern and the pattern."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, case_sensitive, RemoveEmpty]
    parametersTypeList = ['System.String','System.String', 'System.Boolean', 'System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexchunk'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)

    #Parse the values in the array
    output = []
    for val in parsed_json['output']:
        output.append(val['value'])

    return output

def regex_count(source_string, regex_string, case_sensitive=False):
    """Returns an integer containing the number of times a RegEx pattern is found in the source."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, case_sensitive]
    parametersTypeList = ['System.String','System.String', 'System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexcount'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def regex_extract_each(source_string, regex_string, case_sensitive=False, reverse_search=False, return_nothing_on_pattern_fail=False):
    """Returns an array of strings extracted from SourceString using RegExPattern, one value for each capture group defined in the pattern"""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, case_sensitive, reverse_search,return_nothing_on_pattern_fail]
    parametersTypeList = ['System.String','System.String', 'System.Boolean', 'System.Boolean','System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexextracteach'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)

    #Parse the values in the array
    output = []
    for val in parsed_json['output']:
        output.append(val['value'])

    return output

def regex_extract(source_string, regex_string, outputstring="", case_sensitive=False, reverse_search=False, return_nothing_on_pattern_fail=False):
    """Returns a string extracted from SourceString using RegExPattern."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    outputstring = outputstring.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, outputstring, case_sensitive, reverse_search,return_nothing_on_pattern_fail]
    parametersTypeList = ['System.String','System.String','System.String','System.Boolean','System.Boolean','System.Boolean']

    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexextract'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def regex_extract_all(source_string, regex_string, outputstring="", case_sensitive=False):
    """Returns an array of strings extracted from SourceString using RegExPattern"""
    if type(outputstring) is bool:
        case_sensitive = outputstring
        outputstring = ""
    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, outputstring, case_sensitive]
    parametersTypeList = ['System.String','System.String', 'System.String','System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexextractall'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)

    #Parse the values in the array
    output = []
    for val in parsed_json['output']:
        output.append(val['value'])
    return output


def regex_extract_int(source_string, regex_string, case_sensitive=False):
    """regexextractint"""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, case_sensitive]
    parametersTypeList = ['System.String','System.String', 'System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexextractint'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def regex_is_match(source_string, regex_string, case_sensitive=False):
    """Returns a boolean indicating if RegExPattern is a match for SourceString."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, case_sensitive]
    parametersTypeList = ['System.String','System.String', 'System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexismatch'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def regex_replace(source_string, regex_string, replaceString, case_sensitive=False):
    """Returns SourceString after replacing any matches found with RegExPattern with ReplaceString."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    regex_string = regex_string.replace("\\","\\\\")
    replaceString = replaceString.replace("\\","\\\\")
    parametersValueList = [source_string, regex_string, replaceString, case_sensitive]
    parametersTypeList = ['System.String','System.String','System.String', 'System.Boolean']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexreplace'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def regex_escape(source_string):
    """Returns string with common regex chars escaped out."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/regexescape'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def remove_diacritics(source_string):
    """Removes characters with diacritics and replaces them with the closest ASCII character(s)"""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/removediacritics'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def remove_duplicate_whitespace_chars(source_string):
    """Removes blocks of whitespace from the text and replaces it with a single newline, tab, or space."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/removeduplicatewhitespacechars'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def remove_extra_whitespace(source_string):
    """Removes any whitespace chars in a string an returns a string that contains only single spaces in place of multi-spaces, newlines, tabs, etc."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/removeextrawhitespace'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def remove_invalid_filepathcharacters(source_string):
    """Returns a string with any invalid characters replaced with the Replacement string"""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/removeinvalidfilepathcharacters'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']

def remove_whitespace(source_string):
    """Removes any whitespace chars in a string."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/removewhitespace'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']


def sha(source_string):
    """Returns an SHA512 hash of a string."""

    # Create JSON Payload to send
    source_string = source_string.replace("\\","\\\\")
    parametersValueList = [source_string]
    parametersTypeList = ['System.String']
    jsonInputList = [{"type": pt ,"value": pv} for pt, pv in zip(parametersTypeList, parametersValueList)]
    payload ={"parameters": jsonInputList}

    # Send Request
    url = 'https://vfgwrongyh.execute-api.us-east-1.amazonaws.com/Production/clarity/sha'
    headers = {'content-type': 'application/json', 'X-API-KEY': API_KEY}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    parsed_json = json.loads(response.text)
    return parsed_json['value']
