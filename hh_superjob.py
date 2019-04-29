import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city', default='Москва')
    parser.add_argument('-a', '--add', nargs='+', default=None)
    return parser


def get_predict_salary(from_salary, to_salary):
    if from_salary and to_salary:
        expected_salary = (from_salary + to_salary) / 2
    elif from_salary and not to_salary:
        expected_salary = from_salary * 1.2
    elif to_salary and not from_salary:
        expected_salary = to_salary * 0.8
    else:
        expected_salary = None

    return expected_salary


def get_predict_rub_salary_hh(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
        return get_predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])


def get_predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        return get_predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def provide_params_hh(page, area_id, text=''):
    return {
        'text': 'Программист {}'.format(text),
        'area': area_id,
        'period': 30,  # last month
        'page': page
    }


def provide_headers_sj(secret_key):
    return {
        'X-Api-App-Id': secret_key
    }


def provide_params_sj(page, area_id, text=''):
    return {
        'town': area_id,
        'catalogues': 48,  # Develop, programing
        'count': 100,  # vacancies on page
        'page': page,
        'keyword': text,
    }


def create_dict_language_statistics(language, vac_found, vac_processed, avg_salary):
    return {
        language: {
            'vacancies_found': vac_found,
            'vacancies_processed': vac_processed,
            'average_salary': int(avg_salary)
        }
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


def get_statistics_language_sj(api_url, secret_key, area_id, language):
    vacancies_found = 0
    all_salaries_vacancies = []

    page = 0
    more = True
    while more:
        response = requests.get(api_url,
                                headers=provide_headers_sj(secret_key),
                                params=provide_params_sj(page, area_id, text=language))
        response.raise_for_status()

        page += 1
        more = response.json()['more']
        vacancies_found = response.json()['total']
        vacancies_language = response.json()['objects']
        salaries_vacancies = [get_predict_rub_salary_sj(vacancy) for vacancy in vacancies_language]
        all_salaries_vacancies.extend(salaries_vacancies)

    is_salary = list(filter(lambda x: x is not None, all_salaries_vacancies))
    vacancies_processed = len(is_salary)

    if vacancies_processed:
        average_salary = sum(is_salary) // vacancies_processed
    else:
        average_salary = 0

    return create_dict_language_statistics(language, vacancies_found, vacancies_processed, average_salary)


def get_data_from_head_hunter(area_id, programming_languages):
    api_url = 'https://api.hh.ru/vacancies?'
    dict_languages_statistics = {}
    for language in programming_languages:
        dict_languages_statistics.update(get_statistics_language_hh(api_url, area_id, language))

    return dict_languages_statistics


def get_data_from_superjob(secret_key, area_id, programming_languages):
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    dict_languages_statistics = {}
    for language in programming_languages:
        dict_languages_statistics.update(get_statistics_language_sj(api_url, secret_key, area_id, language))

    return dict_languages_statistics


def create_table(title, languages_statistics):

    table_data = [
        ['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата']
    ]
    for language, statistics in languages_statistics:
        table_data.append([language] + list(statistics.values()))

    table = AsciiTable(table_data, title)
    print(table.table)


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
            if area.capitalize() == name:
                return id


def parse_areas_sj(data, area):
    for town in data['towns']:
        if area.capitalize() == town['title']:
            return town['id']

    for region in data['regions']:
        for town in region['towns']:
            if area.capitalize() == town['title']:
                return town['id']


def get_area_id_sj(area):
    url = 'https://api.superjob.ru/2.0/regions/combined/'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()[0]

    return parse_areas_sj(response, area)


def main():
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')
    programming_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'Php', 'C++', 'C#', 'C', 'Go', 'Scala']

    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.add:
        programming_languages.extend(namespace.add)

    try:
        area_id_hh = get_area_id_hh(namespace.city)
        if area_id_hh is None:
            exit('City {} not found'.format(namespace.city))

        data_from_hh = get_data_from_head_hunter(area_id_hh, programming_languages)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server HeadHunter:\n{0}".format(error))

    try:
        area_id_sj = get_area_id_sj(namespace.city)
        if area_id_sj is None:
            exit('City {} not found'.format(namespace.city))

        data_from_sj = get_data_from_superjob(secret_key, area_id_sj, programming_languages)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server SuperJob:\n{0}".format(error))

    data_from_hh = sorted(data_from_hh.items(), key=lambda x: x[1]['average_salary'], reverse=True)
    data_from_sj = sorted(data_from_sj.items(), key=lambda x: x[1]['average_salary'], reverse=True)

    create_table('HeadHunter', data_from_hh)
    create_table('SuperJob', data_from_sj)


if __name__ == '__main__':
    main()
