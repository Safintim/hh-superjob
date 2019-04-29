# hh-supejob

## Описание
Скрипт, который показывает статистику вакансий по популярным языкам программирования в Москве.
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

## Как использовать: 

Имеются следующие аргументы:
* -c (или --city) - указать город (по умолчанию Москва)
* -a (или --add) - добавить язык программирования в список (перечислить через пробел)
* -nw (или --new) - задать свой список языков программирования

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