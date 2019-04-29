from tools import get_predict_salary, create_dict_language_statistics
import requests


def get_predict_rub_salary_hh(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
        return get_predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])


def provide_params_hh(page, area_id, text=''):
    return {
        'text': 'Программист {}'.format(text),
        'area': area_id,
        'period': 30,  # last month
        'page': page
    }


def get_statistics_language_hh(api_url, area_id, language):

    vacancies_found = 0
    all_salaries_vacancies = []

    page = 0
    number_pages = 1
    while page < number_pages:
        response = requests.get(api_url, params=provide_params_hh(page, area_id, language))
        response.raise_for_status()

        number_pages = response.json()['pages']
        page += 1
        vacancies_language = response.json()['items']
        vacancies_found = response.json()['found']

        salaries_vacancies = [get_predict_rub_salary_hh(vacancy) for vacancy in vacancies_language]
        all_salaries_vacancies.extend(salaries_vacancies)

    is_salary = list(filter(lambda x: x is not None, all_salaries_vacancies))
    vacancies_processed = len(is_salary)
    if vacancies_processed:
        average_salary = sum(is_salary) // vacancies_processed
    else:
        average_salary = 0

    return create_dict_language_statistics(language, vacancies_found, vacancies_processed, average_salary)


def parse_areas_hh(data):
    id_name_areas = []
    if isinstance(data, dict):
        id = data.get('id', None)
        name = data.get('name', None)
        areas = data.get('areas', list())
        id_name_areas = id_name_areas + [(id, name)] + parse_areas_hh(areas)
        return id_name_areas
    elif isinstance(data, list):
        area_exists = []
        for row in data:
            area_exists = area_exists + parse_areas_hh(row)
        return area_exists
    return id_name_areas


def get_area_id_hh(area):
    url = 'https://api.hh.ru/salary_statistics/dictionaries/salary_areas'
    response = requests.get(url)
    response.raise_for_status()
    for row in response.json():
        for id, name in parse_areas_hh(row):
            if area.lower() == name.lower():
                return id


def get_data_from_head_hunter(city, programming_languages):
    api_url = 'https://api.hh.ru/vacancies?'
    dict_languages_statistics = {}

    area_id = get_area_id_hh(city)
    if area_id:
        for language in programming_languages:
            dict_languages_statistics.update(get_statistics_language_hh(api_url, area_id, language))

        return dict_languages_statistics
