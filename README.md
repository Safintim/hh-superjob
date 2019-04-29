# hh-supejob

## Описание
Скрипт, который показывает статистику вакансий по популярным языкам программирования в России.
 Результат выводится в консоль ввиде таблицы.

Статистика по языкам:

Javascript, Java, Python, Ruby, Php, C++, C#, C, Go, Scala


Использованные API:
* [HeadHunter](https://github.com/hhru/api/blob/master/README.md#headhunter-api)
* [SuperJob](https://api.superjob.ru/)
## Требования

Для запуска скрипта требуется:

*Python 3.6*


## Как установить:

1. Установить Python3:

(Windows):[python.org/downloads](https://www.python.org/downloads/windows/)

(Debian):
```sh
sudo apt-get install python3
sudo apt-get install python3-pip
```
2. Установить зависимости и скачать сам проект:

```sh
git clone https://github.com/Safintim/hh-superjob.git
pip3 install -r requirements.txt
```

## Зависимости
* *python-dotenv==0.10.1*
* *requests==2.21.0*
* *terminaltables==3.1.0*

## Как использовать: 

superjob требует регистрацию приложения:
1. [Зарегистрировать приложение](https://api.superjob.ru/info/)
2. Создать в папке с репозиторием .env файл
3. Полученный *Secret key*  от superjob записать в .env файл: SECRET_KEY=*Ваш_Secret_key*

Можно получить данные только от hh (смотрите ниже).

Имеются следующие аргументы:
* -c (или --city) - указать город (по умолчанию Москва)
* -a (или --add) - добавить язык программирования в список (перечислить через пробел)
* -nw (или --new) - задать свой список языков программирования
* -hh (или --only_hh)- (флаг) получить данные только от HeadHunter

Города состоящее из нескольких слов нужно писать в кавычках-> 'Нижний Новгород'

```sh
python3 hh_superjob.py
python3 hh_superjob.py -c Казань
python3 hh_superjob.py -c Казань -a R F#
python3 hh_superjob.py -c Казань -nw Python PHP Java C++
python3 hh_superjob.py --new Python PHP Java C++ R F#
```

## Пример вывода :

```sh
python3 hh_superjob.py
```
![Alt Text](http://ipic.su/img/img7/fs/hh_superjob2.1556540138.png)


```sh
python3 hh_superjob.py -c Казань
```
![Alt Text](http://ipic.su/img/img7/fs/1.1556544929.png)


```sh
python3 hh_superjob.py -c Казань -nw Python PHP Java C++
```
![Alt Text](http://ipic.su/img/img7/fs/2.1556544954.png)


```sh
python3 hh_superjob.py --new Python PHP Java C++ R F#
```
![Alt Text](http://ipic.su/img/img7/fs/3.1556545008.png)