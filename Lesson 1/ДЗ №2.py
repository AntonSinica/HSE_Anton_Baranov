ans = [{'name': 1, 'status': 2, 'inn': 3}, {'name': 1, 'status': 2, 'inn': 3}, {'name': 1, 'status': 2, 'inn': 3}]
statuses = ['Истец', 'Ответчик', 'Третье лицо']
statuses_RP = ['Истца', 'Ответчика', 'Третьего лица']

for i in range(len(ans)):
    ans[i]['name'] = input(f"Введите наименование {statuses_RP[i]}: ")
    ans[i]['status'] = statuses[i]
    ans[i]['inn'] = int(input(f"Введите ИНН {statuses_RP[i]}: "))

for el in ans:
    print(el)
