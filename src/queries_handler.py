import requests
import json


##
# Constructs GET query url from given base url and params.
#
# @param: base_url - string containing base url
# @param: request_params - dict containing ordered query params, keys in dict stand for keys in query params
# @returns: response of get request
def build_get_request(base_url, request_params, stream_response=False):
    if request_params is not None and len(request_params) > 0:
        if base_url[len(base_url) - 1] != '?':
            base_url += '?'
        param_key, param_value = request_params.popitem()
        base_url += f'{param_key}={param_value}'

    for param_key, param_value in request_params.items():
        base_url += f'&{param_key}={param_value}'

    return requests.get(url=base_url, stream=stream_response)


##
# Constructs POST query url from given base url and params.
#
# @param: base_url - string containing base url
# @param: post_params - dict containing ordered query params, keys in dict stand for keys in query params
# @returns: response of get request
def build_post_request(base_url, post_params):
    return requests.post(url=base_url, data=post_params)


##
# Draws response content and returns it as encoded json.
#
# @param: requests_response - response object, received by executing request by requests library
# @returns: encoded response contents, usually json
def fetch_text_response(requests_response):
    return requests_response.text


##
# Decodes json content to string.
#
# @param: json_response - encoded json
# @returns: string with json contents
def get_json_string(json_response):
    return json.loads(json_response)
