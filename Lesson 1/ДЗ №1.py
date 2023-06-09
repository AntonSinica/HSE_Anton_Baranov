# Задание 1

# Поработайте с переменными, создайте несколько, выведите на экран.
# Запросите у пользователя некоторые числа и строки и сохраните в переменные, а затем выведите на экран.
# Используйте функции для консольного ввода input() и консольного вывода print().

# Попробуйте также в ходе выполнения задания через встроенную функцию id() понаблюдать,
# какие типы объектов могут изменяться и сохранять за собой адрес в оперативной памяти.

print("Задание 1")
print()

Integer = 37
Float = 12.5
String = "Hello, World!"
Bool = True
List = [4, 8, 15, 16, 23, 42, 'Lost']
Tuple = (2, 3, 5, 7, 11)
Dict = {'name': 'Anton', 'age': 24}
Set = {'a', 'b', 'b', 'a'}

print("В переменной 'Integer' содержится:", Integer)
print("В переменной 'Float' содержится:", Float)
print("В переменной 'String' содержится:", String)
print("В переменной 'Bool' содержится:", Bool)
print("В переменной 'List' содержится:", List)
print("В переменной 'Tuple' содержится:", Tuple)
print("В переменной 'Dict' содержится:", Dict)
print("В переменной 'Set' содержится:", Set)

print()

Integer = int(input("Введите число: "))
String = input("Введите текст: ")

print()

print("В переменной 'Integer' теперь содержится:", Integer)
print("В переменной 'String' теперь содержится:", String)

print()


# Задание 2

# Пользователь вводит время в секундах.
# Рассчитайте время и сохраните отдельно в каждую переменную количество часов, минут и секунд.
# Переведите время в часы, минуты, секунды и сохраните в отдельных переменных.

# Используйте приведение типов для перевода строк в числовые типы.
# Предусмотрите проверку строки на наличие только числовых данных через встроенный строковый метод .isdigit()

# Выведите рассчитанные часы, минуты и секунды по отдельности в консоль.

print("Задание 2")
print()

times = input("Введите время в секундах: ")

while times.isdigit() != True:
    times = input("Введите время в секундах: ")

times = int(times)
sec = times % 60
minutes = times // 60 % 60
hours = times // 3600

print(f'''Количество часов: {hours}
Количество минут: {minutes}
Количество секунд: {sec}''')

print()


# Задание 3

# Запросите у пользователя через консоль число n (от 1 до 9). Найдите сумму чисел n + nn + nnn. Выведете данные в консоль.

print("Задание 3")
print()

n = input("Введите число от 1 до 9: ")

ans = int(n) + int(n * 2) + int(n * 3)

print(ans)