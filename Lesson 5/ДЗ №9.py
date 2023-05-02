# Задание

# Сгенерируйте с использованием функции range (случайный шаг от 3 до 5) массив,
# содержащий отсортированные числа от 10 до 250 млн.

# Сгенерируйте с помощью list comprehensions и функции randomint (встроенный модуль random) 10 случайных чисел.

# Напишите функцию для алгоритма линейного поиска.

# Напишите функцию для алгоритма бинарного поиска.

# Проверьте наличие ранее сгенерированных случайных чисел в массиве с помощью алгоритмов линейного и бинарного поиска,
# замерьте время.

import random as r
from datetime import datetime

# создание функции линейного поиска
def lin_poisk():
    flag = 0
    for i in chisla_na_poisk:
        for j in massiv_chisel:
            if i == j:
                flag += 1

# создание функции бинарного поиска
def bin_poisk(m):
    for i in chisla_na_poisk:
        nachalo = 0
        konec = len(m) - 1
        while nachalo <= konec:
            center = (nachalo + konec) // 2
            if i == m[center]:
                break
            if i > m[center]:
                nachalo = center + 1
            else:
                konec = center - 1

# создание массива чисел
massiv_chisel = [x for x in range(10, 250000000, 3)]

# генерация списка из случайных чисел (гарантированно каждое из них содержится и в раннее созданном массиве чисел)
chisla_na_poisk = []
while len(chisla_na_poisk) != 10:
    x = r.randint(10, 250000000)
    if x in massiv_chisel:
        chisla_na_poisk.append(x)

# вычисление работы времени функции линейного поиска
start_time = datetime.now()
lin_poisk()
print(f'На работу алгоритма линейного поиска уходит: {datetime.now() - start_time} секунд')

# вычисление работы времени функции бинарного поиска
start_time = datetime.now()
bin_poisk(massiv_chisel)
print(f'На работу алгоритма бинарного поиска уходит: {datetime.now() - start_time} секунд')