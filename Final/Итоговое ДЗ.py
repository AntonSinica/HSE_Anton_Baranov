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
import json
import os
from decimal import Decimal
# Для возможности вызова метода cb_excel() требуется дополнительная библиотека.
# Больше зависимостей у нее нет, используется только в одном методе.
import openpyxl


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
            return 'Возможно Вы ошиблись в написании наименования валюты.'

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

    # метод возвращает словарь: где ключ - дата, значение - курс валюты и количество единиц
    def __cb_dict(self, cur):
        cb_date_rate = self.__cb_parser(cur)
        cb_date = cb_date_rate[0::3]
        cb_measure = cb_date_rate[1::3]
        cb_rate = cb_date_rate[2::3]
        if cb_date == cb_measure == cb_rate:
            table_dict = {cb_date[i]: (cb_rate[i], cb_measure[i]) for i in range(len(cb_date))}
        else:
            table_dict = {cb_date[i]: (cb_rate[i], cb_measure[i])
                          for i in range(min(len(cb_date), len(cb_measure), len(cb_rate)))}
        return table_dict

    # метод создает excel-таблицу, со значениями дата - курс валюты - количество валюты за указанную цену
    def cb_excel(self, cur):
        if self.__currency(cur) != 'Возможно Вы ошиблись в написании наименования валюты.':
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

            if cb_date == cb_measure == cb_rate:
                for i in range(len(cb_date)):
                    sheet[f'A{i + 2}'] = cb_date[i]
                    sheet[f'B{i + 2}'] = cb_rate[i]
                    sheet[f'C{i + 2}'] = cb_measure[i]
                book.save(f'{name_currency}.xlsx')
                book.close()
            else:
                for i in range(min(len(cb_date), len(cb_measure), len(cb_rate))):
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
            return 'Создание Excel-таблицы прошло успешно.'
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты.'

    # метод осуществляет сериализацию данных в json-файл
    def cb_json(self, cur):
        if self.__currency(cur) != 'Возможно Вы ошиблись в написании наименования валюты.':
            cb_date_rate = self.__cb_dict(cur)
            name_currency = cur
            if not os.path.exists('parsed_data'):
                os.mkdir('parsed_data')
            with open(f"{name_currency}.json", "w") as json_file:
                json.dump(cb_date_rate, json_file, indent=4)

            if os.path.exists(f'./parsed_data/{name_currency}.json'):
                os.remove(f'./parsed_data/{name_currency}.json')
            os.rename(f'./{name_currency}.json', f'./parsed_data/{name_currency}.json')
            return 'Сериализация данных в json-файл прошла успешно.'
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты.'

    # метод осуществляет десериализацию данных из json-файла
    @staticmethod
    def cb_djson(cur):
        name_currency = cur
        if os.path.exists(f"./parsed_data/{name_currency}.json"):
            with open(os.path.join(f"./parsed_data/{name_currency}.json"), "r") as json_file:
                s = json.load(json_file)
            return s
        else:
            return f'Перепроверьте название json-файла. ' \
                   f'Возможно файла с названием "{name_currency}.json" не существует.'

    # метод для запуска Парсера
    def start(self, cur):
        if self.__currency(cur) != 'Возможно Вы ошиблись в написании наименования валюты.':
            return self.__cb_dict(cur)
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты.'


# класс для работы с собранными данными
class CurrencyCBRF:

    # метод возвращает курс заданной валюты в конкретный день
    @staticmethod
    def inf_currency_date(currency, day):
        cur_dict = ParserCBRF().start(currency)
        if cur_dict != 'Возможно Вы ошиблись в написании наименования валюты.':
            if day in cur_dict.keys():
                i_cur_date = cur_dict[day]
                return f'{i_cur_date[0]} рублей за {i_cur_date[1]} штук(у)'
            else:
                return f'Информация о дате {day} отсутствует на сайте ЦБ РФ. ' \
                       f'Попробуйте указать дату ближайшего к ней рабочего дня.'
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты.'

    # метод возвращает информацию об изменении курса валюты между двумя указанными датами
    @staticmethod
    def comparison(currency, day_old, day_new):
        cur_dict = ParserCBRF().start(currency)
        if cur_dict != 'Возможно Вы ошиблись в написании наименования валюты.':
            if day_old in cur_dict.keys() and day_new in cur_dict.keys():
                do = Decimal(cur_dict[day_old][0].replace(",", "."))
                dn = Decimal(cur_dict[day_new][0].replace(",", "."))
                comparison_result = do - dn
                if comparison_result < 0:
                    return f'Курс упал на {str(comparison_result)[1:]} руб.'
                elif comparison_result > 0:
                    return f'Курс вырос на {comparison_result} руб.'
                else:
                    return f'Величина курса не изменилась'
            elif day_old not in cur_dict.keys() and day_new in cur_dict.keys():
                return f'Информация о дате {day_old} отсутствует на сайте ЦБ РФ. ' \
                       f'Попробуйте указать дату ближайшего к ней рабочего дня.'
            elif day_old in cur_dict.keys() and day_new not in cur_dict.keys():
                return f'Информация о дате {day_new} отсутствует на сайте ЦБ РФ. ' \
                       f'Попробуйте указать дату ближайшего к ней рабочего дня.'
            elif day_old not in cur_dict.keys() and day_new not in cur_dict.keys():
                return f'Информация об указанных датах отсутствует на сайте ЦБ РФ. ' \
                       f'Попробуйте указать даты ближайшим к ним рабочих дней.'
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты.'

    # метод возвращает словарь подобный тому, что возвращает метод start(),
    # но между двумя указанными датами
    @staticmethod
    def range_dates(currency, day_start, day_finish):
        cur_dict = ParserCBRF().start(currency)
        if cur_dict != 'Возможно Вы ошиблись в написании наименования валюты.':
            daf = list(cur_dict.keys()).index(day_start) + 1
            das = list(cur_dict.keys()).index(day_finish)
            exp = cur_dict.values()
            dad = {k: cur_dict[k] for k in list(cur_dict.keys())[das:daf]}
            return dad
        else:
            return 'Возможно Вы ошиблись в написании наименования валюты.'


# =========================================================================================================
# ИНСТРУКЦИЯ!
# =========================================================================================================

# Парсер возвращает данные по курсу заданной валюты,
# начиная с 1 июля 1992 года (самая ранняя дата доступная на сайте ЦБ РФ) и заканчивая сегодняшним днем.
# Чтобы воспользоваться Парсером необходимо ввести название валюты в качестве аргумента метода start().
# Для парсинга доступны все виды валют, представленные на сайте ЦБ РФ.
# Результатом работы Парсера является словарь вида: {Дата: (курс валюты, количество единиц за данную цену)}
# Результаты работы Парсера можно так же поместить в Excel-таблицу, воспользовавшись методом cb_excel().
# Так же для реализованного класса доступны методы cb_json() и cb_dejson(),
# которые позволяют сериализировать данные в json-файл и десериализировать данные из json-файла соответственно.
# Чтобы воспользоваться данными функциями -
# необходимо ввести название валюты в качестве аргумента соответствующего метода.

# Методы класса CurrencyCBRF позволяют:
# 1) получить курс конкретной валюты в конкретный день;
# 2) получить информацию об изменении курса валюты между двумя указанными датами;
# 3) получить словарь, подобный тому, что возвращает метод start(), но между двумя указанными датами.
# В методах, где надо вводить две даты, вторая дата должна быть календарно позже первой.

if __name__ == '__main__':
    print(ParserCBRF().start('Доллар США'))
    print(ParserCBRF().cb_json('Евро'))
    print(ParserCBRF().cb_djson('Евро'))
    print(ParserCBRF().cb_excel('Китайский юань'))

    print(CurrencyCBRF().inf_currency_date('Белорусский рубль', '01.06.2023'))
    print(CurrencyCBRF().comparison('Английский фунт', '04.05.2023', '16.06.2023'))
    print(CurrencyCBRF().range_dates('Турецкая лира', '04.05.2023', '17.05.2023'))
