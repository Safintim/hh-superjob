import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


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


def provide_params_hh(page, text=''):
    return {
        'text': 'Программист {}'.format(text),
        'area': 1,  # Moscow
        'period': 30,  # last month
        'page': page
    }


def provide_headers_sj(secret_key):
    return {
        'X-Api-App-Id': secret_key
    }


def provide_params_sj(page, text=''):
    return {
        'town': 4,  # Moscow
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


def get_statistics_language_hh(api_url, language):

    vacancies_found = 0
    all_salaries_vacancies = []

    page = 0
    number_pages = 1
    while page < number_pages:
        response = requests.get(api_url, params=provide_params_hh(page, language))
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


def get_statistics_language_sj(api_url, secret_key, language):
    vacancies_found = 0
    all_salaries_vacancies = []

    page = 0
    more = True
    while more:
        response = requests.get(api_url,
                                headers=provide_headers_sj(secret_key),
                                params=provide_params_sj(page, text=language))
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


def get_data_from_head_hunter(programming_languages):
    api_url = 'https://api.hh.ru/vacancies?'
    dict_languages_statistics = {}
    for language in programming_languages:
        dict_languages_statistics.update(get_statistics_language_hh(api_url, language))

    return dict_languages_statistics


def get_data_from_superjob(secret_key, programming_languages):
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    dict_languages_statistics = {}
    for language in programming_languages:
        dict_languages_statistics.update(get_statistics_language_sj(api_url, secret_key, language))

    return dict_languages_statistics


def create_table(title, languages_statistics):

    table_data = [
        ['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата']
    ]
    for language, statistics in languages_statistics:
        table_data.append([language] + list(statistics.values()))

    table = AsciiTable(table_data, title)
    print(table.table)


def pars_areas(data):
    id_name_areas = []
    if isinstance(data, dict):
        id = data.get('id', None)
        name = data.get('name', None)
        areas = data.get('areas', list())
        id_name_areas = id_name_areas + [(id, name)] + pars_areas(areas)
        return id_name_areas
    elif isinstance(data, list):
        area_exists = []
        for row in data:
            area_exists = area_exists + pars_areas(row)
        return area_exists
    return id_name_areas


def get_areas_id():
    result = []
    url = 'https://api.hh.ru/salary_statistics/dictionaries/salary_areas'
    response = requests.get(url).json()
    for row in response:
        result += pars_areas(row)
    result.sort(key=lambda x: x[0])
    return result


def main():
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')
    programming_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'Php', 'C++', 'C#', 'C', 'Go', 'Scala']

    try:
        data_from_hh = get_data_from_head_hunter(programming_languages)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server HeadHunter:\n{0}".format(error))
    try:
        data_from_sj = get_data_from_superjob(secret_key, programming_languages)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server SuperJob:\n{0}".format(error))

    data_from_hh = sorted(data_from_hh.items(), key=lambda x: x[1]['average_salary'], reverse=True)
    data_from_sj = sorted(data_from_sj.items(), key=lambda x: x[1]['average_salary'], reverse=True)

    create_table('HeadHunter', data_from_hh)
    create_table('SuperJob', data_from_sj)


if __name__ == '__main__':
    main()

