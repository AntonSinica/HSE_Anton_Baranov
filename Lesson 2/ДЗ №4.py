# Задание

# Напишите функцию для валидации ИНН (идентификационного номера налогоплательщика),
# которая принимает в качестве аргумента строку, содержащую ИНН или просто набор цифр, похожий на ИНН.

# Функция возвращает True в случае, если ИНН прошёл проверку, и False, если проверка не пройдена.

# Для удобства лучше разбить код на несколько взаимосвязанных функций.

def valid_inn(inn):
    if len(str(inn)) == 10 and str(inn).isdigit():
        return valid_inn_org(inn)
    elif len(str(inn)) == 12 and str(inn).isdigit():
        return valid_inn_fl(inn)
    else:
        return False

def valid_inn_org(inn):
    coefficient = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum = 0
    for i in range(len(coefficient)):
        checksum += coefficient[i] * int(str(inn)[i])

    control_number = checksum % 11
    if control_number > 9:
        control_number %= 10

    return control_number == int(inn) % 10

def valid_inn_fl(inn):
    coefficient1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum1 = 0
    for i in range(len(coefficient1)):
        checksum1 += coefficient1[i] * int(str(inn)[i])

    control_number1 = checksum1 % 11
    if control_number1 > 9:
        control_number1 %= 10

    coefficient2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum2 = 0
    for i in range(len(coefficient2)):
        checksum2 += coefficient2[i] * int(str(inn)[i])

    control_number2 = checksum2 % 11
    if control_number2 > 9:
        control_number2 %= 10

    return control_number1 == int(inn) % 100 // 10 and control_number2 == int(inn) % 10


print(valid_inn(input()))