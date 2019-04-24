import os
from hh import hh
from superjob import superjob
from dotenv import load_dotenv

def main():
    load_dotenv()
    programming_languages = ['Javascript', 'Java', 'Python', 'Ruby', 'Php', 'C++', 'C#', 'C', 'Go', 'Scala']
    secret_key = os.getenv('SECRET_KEY')

    hh(programming_languages)
    superjob(secret_key, programming_languages)


if __name__ == '__main__':
    main()
