import requests


def provide_headers(secret_key):
    return {
        'X-Api-App-Id': secret_key
    }


def provide_params():
    return {
        'towns': 4,
        'catalogues': 48
    }


def superjob(secret_key, programming_languages=None):
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    response = requests.get(api_url, headers=provide_headers(secret_key), params=provide_params())
    for i in response.json()['objects']:
        print(i['profession'], i['town']['title'])

secret_key = 'v3.r.129948218.738491434325e16a7d84d12bd43d3054954f0799.795f399ccb65509fc87c15ed48ad05a259dbce19'
superjob(secret_key)
