import os
import requests
import argparse
from dotenv import load_dotenv
from terminaltables import AsciiTable
from get_data_hh import get_data_from_head_hunter
from get_data_sj import get_data_from_superjob


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city', default='Москва')
    parser.add_argument('-a', '--add', nargs='+', default=None)
    return parser


def create_table(title, languages_statistics):

    table_data = [
        ['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата']
    ]
    for language, statistics in languages_statistics:
        table_data.append([language] + list(statistics.values()))

    table = AsciiTable(table_data, title)
    print(table.table)


def main():
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')
    programming_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'Php', 'C++', 'C#', 'C', 'Go', 'Scala']

    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.add:
        programming_languages.extend(namespace.add)

    try:
        data_from_hh = get_data_from_head_hunter(namespace.city, programming_languages)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server HeadHunter:\n{0}".format(error))

    try:
        data_from_sj = get_data_from_superjob(secret_key, namespace.city, programming_languages)
    except requests.exceptions.HTTPError as error:
        exit("Can't get data from server SuperJob:\n{0}".format(error))

    if not data_from_hh:
        exit('City {} not found'.format(namespace.city))
    if not data_from_sj:
        exit('City {} not found'.format(namespace.city))

    data_from_hh = sorted(data_from_hh.items(), key=lambda x: x[1]['average_salary'], reverse=True)
    data_from_sj = sorted(data_from_sj.items(), key=lambda x: x[1]['average_salary'], reverse=True)

    create_table('HeadHunter', data_from_hh)
    create_table('SuperJob', data_from_sj)


if __name__ == '__main__':
    main()
