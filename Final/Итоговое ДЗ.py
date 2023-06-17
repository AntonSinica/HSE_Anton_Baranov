# Задание

# Необходимо собрать данные с сайта ЦБ РФ с помощью Python.

# Шаг 1

# Выбрать данные с сайта ЦБ:

# Шаг 2

# Определите структуру для хранения и работы.
# Для ключевой ставки ЦБ РФ это может быть словарь (dict), где ключом будет выступать дата,
# а значением — размер ключевой ставки на указанную дату:

# Шаг 3

# Напишите скрипт, который будет производить сбор данных с выбранной страницы на сайте ЦБ РФ
# либо осуществлять загрузку xsl/xslx/pdf/csv или иного файла с данными в рабочую директорию
# с последующим его парсингом.

# Шаг 4

# Сделайте метод сериализации и десериализации данных для сохранения их в JSON-файл
# и подготовки данных для работы модулем из Шага 7. При написании метода используйте dict/list comprehensions.

# Сохранение файла должно производиться в директорию parsed_data внутри папки проекта.
# Путь к директории parsed_data должен быть прописан так, чтобы он был кроссплатформенным.
# Написанный скрипт должен запуститься на любой операционной системе и при запуске скрипта из любой директории.

# Шаг 5

# Необходимо привести данные к рабочим типам.
# Продумайте и реализуйте методологию заполнения пробелов в данных, если это необходимо для работы.

# Шаг 6

# Оберните весь написанный код парсера в класс ParserCBRF.
# Запуск парсера должен осуществляться через вызов метода start().

# Шаг 7

# Создайте отдельный класс для работы с собранными данными.

from datetime import date
import requests
from bs4 import BeautifulSoup
import openpyxl
import json
import os


# класс парсера сайта cbr.ru
class ParserCBRF:

    @staticmethod
    def __currency(cur):
        url = 'https://www.cbr.ru/currency_base/dynamics/'
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        cur_dict = {i.text.strip(): i['value'] for i in soup.find("select").find_all("option")}

        if cur in cur_dict.keys():
            return cur_dict[cur]
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты'

    # метод возвращает ответ на запрос к сайту
    def __get_page(self, cur):
        url_currency = self.__currency(cur)
        today = date.today().strftime("%d.%m.%Y")
        url_cur = f'https://www.cbr.ru/currency_base/dynamics/' \
              f'?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.' \
              f'date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ={url_currency}&UniDbQuery.' \
              f'From=01.07.1992&UniDbQuery.To={today}'
        r_cur = requests.get(url_cur)
        return r_cur.text

    # метод возвращает список с чередующимися датами, единицами и курсами валюты
    def __cb_parser(self, cur):
        html = self.__get_page(cur)
        soup = BeautifulSoup(html, "html.parser")
        table = [i.text for i in soup.find("table", {"class": "data"}).find_all("td")][1:]
        return table

    # метод возвращает словарь: где ключ - дата, значение - курс валюты
    def __cb_dict(self, cur):
        cb_date_rate = self.__cb_parser(cur)
        cb_date = cb_date_rate[0::3]
        cb_measure = cb_date_rate[1::3]
        cb_rate = cb_date_rate[2::3]
        table_dict = {cb_date[i]: (cb_rate[i], cb_measure[i]) for i in range(len(cb_date))}
        return table_dict

    # метод создает excel-таблицу, со значениями дата - курс валюты - количество валюты за указанную цену
    def __cb_excel(self, cur):
        cb_date_rate = self.__cb_parser(cur)
        name_currency = cur
        cb_date = cb_date_rate[0::3]
        cb_measure = cb_date_rate[1::3]
        cb_rate = cb_date_rate[2::3]

        book = openpyxl.Workbook()
        sheet = book.active
        sheet['A1'] = 'Дата'
        sheet['B1'] = 'Курс'
        sheet['C1'] = 'За кол-во'

        for i in range(len(cb_date)):
            sheet[f'A{i + 2}'] = cb_date[i]
            sheet[f'B{i + 2}'] = cb_rate[i]
            sheet[f'C{i + 2}'] = cb_measure[i]
        book.save(f'{name_currency}.xlsx')
        book.close()

        if not os.path.exists('parsed_data'):
            os.mkdir('parsed_data')

        if os.path.exists(f'./parsed_data/{name_currency}.xlsx'):
            os.remove(f'./parsed_data/{name_currency}.xlsx')
        os.rename(f'./{name_currency}.xlsx', f'./parsed_data/{name_currency}.xlsx')

    # метод сериализует данные в json-файл
    def cb_json(self, cur):
        cb_date_rate = self.__cb_dict(cur)
        name_currency = cur
        if not os.path.exists('parsed_data'):
            os.mkdir('parsed_data')
        with open(f"{name_currency}.json", "w") as json_file:
            json.dump(cb_date_rate, json_file, indent=4)

        if os.path.exists(f'./parsed_data/{name_currency}.json'):
            os.remove(f'./parsed_data/{name_currency}.json')
        os.rename(f'./{name_currency}.json', f'./parsed_data/{name_currency}.json')

    # метод десериализует данные из json-файла
    @staticmethod
    def cb_dejson(cur):
        name_currency = cur
        if os.path.exists(f"./parsed_data/{name_currency}.json"):
            with open(os.path.join(f"./parsed_data/{name_currency}.json"), "r") as json_file:
                s = json.load(json_file)
            return s
        else:
            return f'Перепроверьте название json-файла. ' \
                   f'Возможно файла с названием "{name_currency}.json" не существует.'

    # метод вызывает создание excel-таблицы и возвращает словарь
    def start(self, cur):
        if self.__currency(cur) != 'Возможно Вы ошиблись в написании наименования валюты':
            self.__cb_excel(cur)
            return self.__cb_dict(cur)
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты'


# =========================================================================================================
# ИНСТРУКЦИЯ!
# =========================================================================================================

# Парсер возвращает данные по курсу заданной валюты,
# начиная с 1 июля 1992 года (самая ранняя дата доступная на сайте ЦБ РФ) и заканчивая сегодняшним днем.
# Чтобы воспользоваться Парсером необходимо ввести название валюты в качестве аргумента метода start().
# Для парсинга доступны все виды валют, представленные на сайте ЦБ РФ.
# Результатом работы Парсера является словарь вида: {Дата: (курс валюты, количество единиц за данную цену)}
# и Excel-файл со всеми вышеуказанными данными.
# Так же для реализованного класса доступны методы cb_json() и cb_dejson(),
# которые позволяют сериализировать данные в json-файл и десериализировать данные из json-файла соответственно.
# Чтобы воспользоваться данными функциями -
# необходимо ввести название валюты в качестве аргумента соответствующего метода.

if __name__ == '__main__':
    print(ParserCBRF().start('Китайский юань'))
    ParserCBRF().cb_json('Турецкая лира')
    print(ParserCBRF().cb_dejson('Американский доллар'))
