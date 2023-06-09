# Задание

# Напишите скрипт, который будет производить сбор данных с выбранной страницы на сайте ЦБ РФ,
# либо осуществлять загрузку xsl, xslx, pdf, csv или иного файла с данными
# в рабочую директорию с последующим его парсингом.

# У класса должен быть только один публичный метод start().
# Все остальные методы, содержащие логику по выгрузке и сохранению данных, должны быть приватными.

# Определите структуру для хранения. Например, для ключевой ставки ЦБ РФ это может быть словарь (dict),
# где ключом будет выступать дата, а значением — размер ключевой ставки на указанную дату.

# Оберните весь написанный код парсера в класс ParserCBRF

from datetime import date
import requests
from bs4 import BeautifulSoup
import openpyxl


# класс с единственным публичным методом start(), который создает excel-таблицу и возвращает словарь с данными с cbr.ru
class ParserCBRF:

    # метод возвращает ответ на запрос к сайту
    def __get_page(self):
        today = date.today().strftime("%d.%m.%Y")
        url = f"https://www.cbr.ru/hd_base/KeyRate/?" \
              f"UniDbQuery.Posted=True&" \
              f"UniDbQuery.From=17.09.2013&" \
              f"UniDbQuery.To={today}"
        r = requests.get(url)
        return r.text

    # метод возвращает список с чередующимися датами и ключевыми ставками ЦБ
    def __cb_parser(self):
        html = self.__get_page()
        soup = BeautifulSoup(html, "html.parser")
        table = [i.text for i in soup.find("table", {"class": "data"}).find_all("td")]
        return table

    # метод возвращает словарь: где ключ - дата, значение - ключевая ставка ЦБ
    def __cb_dict(self):
        cb_date_rate = self.__cb_parser()
        cb_date = cb_date_rate[::2]
        cb_rate = cb_date_rate[1::2]
        table_dict = {cb_date[i]: cb_rate[i] for i in range(len(cb_date))}
        return table_dict

    # метод создает excel-таблицу, со значениями дата - ключевая ставка
    def __cb_excel(self):
        cb_date_rate = self.__cb_parser()
        cb_date = cb_date_rate[::2]
        cb_rate = cb_date_rate[1::2]

        # реализовывал без контекстного менеджера with (с ним не получалось)
        book = openpyxl.Workbook()
        sheet = book.active
        for i in range(len(cb_date)):
            sheet[f'A{i + 1}'] = cb_date[i]
            sheet[f'B{i + 1}'] = cb_rate[i]
        book.save('cb_rate.xlsx')
        book.close()

    # метод вызывает создание excel-таблицы и возвращает словарь
    def start(self):
        self.__cb_excel()
        return self.__cb_dict()


print(ParserCBRF().start())
