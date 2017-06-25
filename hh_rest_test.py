# -*- coding: utf-8 -*-

import hh_api_handling as hh
import nose
DOMAIN_NAME = 'api.hh.ru'


def test1():
    """
    test1: Positive: send valid GET https://api.hh.ru/areas
    validate the structure of response
    """
    response = hh.create_and_send_get_request('https', DOMAIN_NAME + '/areas', 200).json()
    region_template = {'name': u"", 'id': u"", 'parent_id': "", 'areas': [{'name': u"", 'id': u"", 'parent_id': u"", 'areas': []}]}
    hh.validate_response(response, region_template)


def test2():
    """
    test2: Negative: try to update https://api.hh.ru/areas with POST
    """
    # why 405?
    hh.create_and_send_post_request('https', DOMAIN_NAME + '/areas', 405)


def test3():
    """test3: validate that Russia region is presented"""
    country_to_find = u"Россия"
    response = hh.create_and_send_get_request('https', DOMAIN_NAME + '/areas', 200).json()
    for todo_item in response:
        if todo_item['name'] == country_to_find:
            country_is_found = 1
    if country_is_found != 1:
        raise AssertionError('expected country is not presented in list')


def test4():
    """
    test4: Positive: GET https://api.hh.ru/employers?area=113&text='Новые Облачные технологии'
    validate the structure of response
    """
    russia_id = hh.get_country(u"Россия", DOMAIN_NAME)
    if russia_id == -1:
        raise AssertionError('verify containment')
    response = hh.create_and_send_get_request('https', DOMAIN_NAME + '/employers', 200, area=russia_id, text=u"Новые облачные").json()

    employers_template = {'found': 0, 'per_page': 0, 'page': 0, 'pages': 0, 'items': [{'name': u"", 'id': u"",
                                                                                       'url': u"", 'alternate_url': u"", 'vacancies_url': u"",
                                                                                       'open_vacancies': 0, 'logo_urls': {}}]}
    hh.validate_response([response], employers_template)


def test5():
    """
    test5: Negative: GET https://api.hh.ru/employers?area='and'&text='Новые Облачные технологии
    400 not found should return
    """
    hh.create_and_send_get_request('https', DOMAIN_NAME + '/employers', 400, area="ndfrfr", text=u"Новые облачные").json()


def test6():
    """
    test6: Positive: GET https://api.hh.ru/employers?area=113&text='Новые Облачные технологии
    parameter with incorrect name should be skipped
    """
    hh.create_and_send_get_request('https', DOMAIN_NAME + '/employers', 200, arwwwwea=113, text=u"Новые облачные").json()


def test7():
    """
    test7: Positive:
    GET https://api.hh.ru/vacancies?text = 'QA Automation engineer'&area = 113&employer_id = 213397
    validate the structure of response
    """
    city_id = hh.get_district_by_country(u"Россия", u"Санкт-Петербург", DOMAIN_NAME)
    empl_id = hh.get_employer_id(u"Новые Облачные технологии", DOMAIN_NAME)
    if city_id != -1 and empl_id != -1:
        response = hh.create_and_send_get_request('https', DOMAIN_NAME + '/vacancies', 200, area=city_id, text="QA Automation engineer",
                                               employer_id=empl_id).json()

        eployer_template = {"per_page": 1, "items": [{"salary": {}, "name": "", "area": {},"url": "", "published_at": "", "relations": [],
                                                      "employer": {}, "address": "", "alternate_url": "", "apply_alternate_url": "",
                                                      "department": {"id": "", "name": ""}, "type": { }, "id": "", "snippet": {}, }]}
        hh.validate_response(response, eployer_template)


def test8():
    """
    test7: Negative:
    GET https://api.hh.ru/vacancies?text = 'QA Automation engineer'&area = 113&employer_id = -1
    400 not found should return
    """
    hh.create_and_send_get_request('https', DOMAIN_NAME + '/vacancies', 400, area=113, text="QA Automation engineer",
                                               employer_id=-1).json()