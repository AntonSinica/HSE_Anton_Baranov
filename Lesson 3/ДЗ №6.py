# Задание

# Соберите информацию о судебных заседаниях в деле № А40-183194/2015 (дело о банкротстве ООО «ТрансИнвестХолдинга»).

# Вам необходимо очистить данные от «мусора».
# Для нужно написать скрипт, который соберет информацию только о реальных судебных заседаниях в деле.

# В файле должен присутствовать список всех реальных заседаний с описанием,
# информацией о начале и окончании судебного заседания, а также о месте его проведения.

# По итогу работы скрипта данные должны быть сохранены в файлик «court_dates.json».

import json
import codecs


# функция перевода ics файла в строки для чтения
def from_ics_to_txt(case_number):
    with codecs.open(f'{case_number}.ics', 'r', 'utf_8_sig') as f:
        return f.readlines()


# функция получения данных по всем "непустым" делам
def case_list(case_number):
    BigList = []
    One_case = [f'{case_number}']
    for line in from_ics_to_txt(case_number):
        if 'BEGIN' not in line and 'TRANSP' not in line and 'URL' not in line \
                and 'UID:' not in line and 'END:' not in line and 'Дело:' not in line:
            if 'START' in line or 'END' in line:
                line = line.strip()[-15:]
                line = line[:4] + '-' + line[4:6] + '-' + line[6:11] \
                       + ':' + line[11:13] + ':' + line[13:15]
                One_case.append(line)
            if 'LOCATION' in line:
                line = line.strip().replace('\\', '')
                ind = line.find(':n')
                One_case.append(line[ind + 3:])
            if 'DESCR' in line:
                One_case.append(line.strip()[12:])
            if 'SUMM' in line:
                One_case.append(line.strip()[8:])
        # отграничиваем логический блок, равный одному заседанию
        elif 'BEGIN' in line:
            for j in One_case:
                if 'Судья' in j:
                    BigList.append(One_case)
            One_case = [f'{case_number}']
    BigList.append(One_case)
    return BigList


# создание словаря из ранее полученного списка
def fin_dict(case_number):
    Keys_List = ['case_number', 'start', 'end', 'location', 'description']
    final = []
    for el in case_list(case_number):
        final.append(dict(zip(Keys_List, el)))
    return final


# преобразование полученных данных в json-файл
def to_json(case_number):
    with open(f"court_dates.json", "w") as json_file:
        json.dump(fin_dict(case_number), json_file, indent=4)


# функция для запуска программы
def main(case_number):
    to_json(case_number)


if __name__ == '__main__':
    main('А40-183194-2015')
