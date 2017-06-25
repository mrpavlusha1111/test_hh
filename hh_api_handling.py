# -*- coding: utf-8 -*-
import requests


def create_and_send_get_request(protocol, request_line, response_code, **kwargs):
    if kwargs is None:
        resp = requests.get('{}://{}'.format(protocol, request_line))
    else:
        parameters_line = ''
        for item in kwargs:
            if item == 'text':
                parameters_line += '' + str(item) + '=' + str(kwargs[item].encode('utf8')) + '&'
            else:
                parameters_line += ''+str(item)+'='+str(kwargs[item])+'&'
        resp = requests.get('{}://{}?{}'.format(protocol, request_line, parameters_line[0:-1]))
    if resp.status_code != response_code:
        raise AssertionError('Unexpected response code {}'.format(resp.status_code))
    return resp


def create_and_send_post_request(protocol, request_line, response_code):
    resp = requests.post('{}://{}'.format(protocol, request_line))
    if resp.status_code != response_code:
        raise AssertionError('Unexpected response code {}'.format(resp.status_code))
    return resp


def get_district_by_country(country_to_find, district_to_find, DOMAIN_NAME):
    response1 = create_and_send_get_request('https', DOMAIN_NAME + '/areas', 200).json()
    for todo_item in response1:
        if todo_item['name'] == country_to_find:
            for district in todo_item['areas']:
                if district['name'] == district_to_find:
                    return district['id']
    return -1


def get_employer_id(company_name, DOMAIN_NAME):
    response = create_and_send_get_request('https', DOMAIN_NAME + '/employers', 200, text=u"Новые облачные").json()
    for item in response['items']:
        if item['name'] == company_name:
            return item['id']
    return -1


def get_country(country_to_find, DOMAIN_NAME):
    response1 = create_and_send_get_request('https', DOMAIN_NAME + '/areas', 200).json()
    for todo_item in response1:
        if todo_item['name'] == country_to_find:
            return todo_item['id']
    return -1


def validate_response(response, expected_template):
    for parameter_name in expected_template.keys():
        if parameter_name not in response[0]:
            raise AssertionError('failed format: check the {} parameter {}'.format(parameter_name, response[0]))
        if response[0][parameter_name]:
            if type(expected_template[parameter_name]) != type(response[0][parameter_name]):
                raise AssertionError(
                    'failed type of {}: {} != {}parameter'.format(parameter_name, type(expected_template[parameter_name]),
                                                                  type(response[0][parameter_name])))
            if expected_template[parameter_name] and type(expected_template[parameter_name]) == list:
                for in_value in response[0][parameter_name][0].keys():
                    if in_value not in expected_template[parameter_name][0]:
                        raise AssertionError('failed format: check the {} parameter'.format(in_value))
                    if response[0][parameter_name][0][in_value]:
                        if type(expected_template[parameter_name][0][in_value]) != type(
                                response[0][parameter_name][0][in_value]):
                            raise AssertionError('failed type of {}:'
                                                 '!= {}parameter'.format(in_value,
                                                                         type(expected_template[parameter_name][0][in_value]),
                                                                         type(response[0][parameter_name][0][in_value])))

