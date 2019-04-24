import requests
import os
from dotenv import load_dotenv


def get_predict_salary(from_salary, to_salary):
    if from_salary and to_salary:
        expected_salary = (from_salary + to_salary) / 2
    elif from_salary and to_salary is None:
        expected_salary = from_salary * 1.2
    elif to_salary and from_salary is None:
        expected_salary = to_salary * 0.8
    else:
        expected_salary = None

    return expected_salary


def get_predict_rub_salary_hh(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
        return get_predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])
    return None


def provide_params_hh(page, text=''):
    params = {
        'text': 'Программист {}'.format(text),
        'area': 1,
        'period': 30,
        'page': page
    }
    return params


def create_dict_language(language, vac_found, vac_processed, avg_salary):
    dict_result = {
        language: {
            'vacancies_found': vac_found,
            'vacancies_processed': vac_processed,
            'average_salary': int(avg_salary)
        }
    }

    return dict_result


def calculation_salaries_vacancies(vacancies):
    return [get_predict_rub_salary_hh(vacancy) for vacancy in vacancies]


def get_statistics_language(api_url, language):

    vacancies_found = 0
    vacancies_processed = 0
    average_salary = 0
    all_salaries_vacancies = []

    page = 0
    number_pages = 1
    while page < number_pages:
        print(page, language)
        response = requests.get(api_url, params=provide_params_hh(page, language)).json()
        number_pages = response['pages']
        page += 1
        vacancies_language = response['items']

        all_salaries_vacancies.extend(calculation_salaries_vacancies(vacancies_language))

        vacancies_found = response['found']

    is_salary = list(filter(lambda x: x is not None, all_salaries_vacancies))
    vacancies_processed += len(is_salary)
    average_salary += sum(is_salary) // vacancies_processed

    return create_dict_language(language, vacancies_found, vacancies_processed, average_salary)


def hh(programming_languages):
    api_url = 'https://api.hh.ru/vacancies?'
    d = {}
    for language in programming_languages:
        d.update(get_statistics_language(api_url, language))

    print(d)


def get_predict_rub_salary_sj(vacancy):
    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
        return get_predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])
    return None


def provide_headers_sj(secret_key):
    return {
        'X-Api-App-Id': secret_key
    }


def provide_params_sj():
    return {
        'towns': 4,
        'catalogues': 48
    }


def superjob(secret_key, programming_languages=None):
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    response = requests.get(api_url, headers=provide_headers_sj(secret_key), params=provide_params_sj())
    for i in response.json()['objects']:
        print(i)
        # print(i['profession'], i['town']['title'])


def main():
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')

    # programming_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'Php', 'C++', 'C#', 'C', 'Go', 'Scala']
    programming_languages = ['Scala']
    # hh(programming_languages)
    superjob(secret_key, programming_languages)


if __name__ == '__main__':
    main()
