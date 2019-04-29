from tools import get_predict_salary, create_dict_language_statistics
import requests


def get_predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        return get_predict_salary(vacancy['payment_from'], vacancy['payment_to'])


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


def parse_areas_sj(data, area):
    for town in data['towns']:
        if area.capitalize() == town['title']:
            return town['id']

    for region in data['regions']:
        for town in region['towns']:
            if area.lower() == town['title'].lower():
                return town['id']


def get_area_id_sj(area):
    url = 'https://api.superjob.ru/2.0/regions/combined/'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()[0]

    return parse_areas_sj(response, area)


def get_data_from_superjob(secret_key, city, programming_languages):
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    dict_languages_statistics = {}

    area_id = get_area_id_sj(city)
    if area_id:
        for language in programming_languages:
            dict_languages_statistics.update(get_statistics_language_sj(api_url, secret_key, area_id, language))

        return dict_languages_statistics

