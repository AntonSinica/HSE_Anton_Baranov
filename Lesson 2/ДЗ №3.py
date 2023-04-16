from lesson_2_data import repondents, courts

# Задание 1

# Создайте ряд функций для проведения математических вычислений:

# Функция вычисления факториала числа (произведение натуральных чисел от 1 до n).
# Принимает в качестве аргумента число, возвращает его факториал.

def f(x: int):
    ans = 1
    for i in range(1, x + 1):
        ans *= i
    return ans

print(f(6))


# Поиск наибольшего числа из трёх.
# Принимает в качестве аргумента кортеж из трёх чисел, возвращает наибольшее из них.

def mx(x):
    ans = 0
    for i in x:
        if i > ans:
            ans = i
    return ans

print(mx((9, 4, 8)))


# Расчёт площади прямоугольного треугольника.
# Принимает в качестве аргумента размер двух катетов треугольника.
# Возвращает площадь треугольника.

def tr(a, b):
    return a * b / 2

print(tr(4, 5))


# Задание 2

# Создайте функцию для генерации текста с адресом суда.

# Функция должна по шаблону генерировать шапку для процессуальных документов с реквизитами сторон для отправки.
# Функция должна принимать в качестве аргумента словарь с данными ответчика и номером дела.

def document_header(respondent):

    if respondent.get('case_number'):

        for i in courts:
            if i['court_code'] == respondent['case_number'][:3]:
                correct_court = i
                break

        header = f'''
---
В Арбитражный суд {correct_court['court_name'][18:]}
Адрес: {correct_court['court_address']}
    
Истец: {plaintiff['name']}
ИНН: {plaintiff['inn']} ОГРНИП: {plaintiff['ogrnip']}
Адрес: {plaintiff['address']}
    
Ответчик: {respondent['short_name']}
ИНН: {respondent['inn']} ОГРНИП: {respondent['ogrn']}
Адрес: {respondent['address']}
    
Номер дела: {respondent['case_number']}'''

        return header

    else:
        return f'''
---
По Ответчику {respondent['short_name']} невозможно определить суд, так как отсутствует номер дела.'''

plaintiff = {'name': 'Баранов Антон Константинович',
             'inn': '1236182357',
             'ogrnip': '218431927812733',
             'address': '123534, г. Москва, ул. Опущенных водников, 13'}

print(document_header({'full_name': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ГОРИЗОНТ"', 'short_name': 'ООО "ГОРИЗОНТ"',
     'inn': '7723428305', 'ogrn': '1167746099784', 'region': 'г. Москва', 'category': 'Обычная организация',
     'category_code': 'SimpleOrganization', 'bankruptcy_id': '145960', 'case_number': 'А40-55871/2017',
     'address': '115088, г Москва, р-н Печатники, ул Южнопортовая, д 15 стр 2, ком 32'}))


# Создайте ещё одну функцию, которая принимает в себя список словарей с данными ответчика.
# Используйте цикл for для генерации всех возможных вариантов этой шапки с вызовом первой функции внутри тела цикла for
# и выводом данных, которые она возвращает в консоль.

def document_headers(lst):
    text = ''
    for i in repondents:
        text += document_header(i)
        text += '\n'
    return text

print(document_headers(repondents))