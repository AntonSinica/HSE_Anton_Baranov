# Задание

# Напишите класс SirotinskyAPI для взаимодействия с API, размещённым по адресу https://api.sirotinsky.com/.

# Класс должен содержать в себе функционал для работы со всеми методами, указанными в документации к API,
# которые размещены по адресу https://api.sirotinsky.com/docs.

# Метод инициализации экземпляра класса должен принимать в качестве аргументов
# логин и пароль для получения токена авторизации
# и сразу производить вызов приватного метода для получения токена в целях его сохранения как аргумента экземпляра.

# Метод получения токена должен быть приватным и не доступен для вызова вне класса.

# Методы для получения данных из ЕФРСБ должны быть публичными

import requests


class SirotinskyAPI:

    URL = 'https://api.sirotinsky.com'
    LOGIN = {
        "username": "HSE_student",
        "password": "123123123"
    }

    def __init__(self):
        self.__get_token()

    def __get_token(self):
        url = f"{self.URL}/token"
        r = requests.post(url, data=self.LOGIN)
        result = r.json()["access_token"]
        self.token = result

    def hello(self, name):
        url = f'{self.URL}/hello/{name}'
        r = requests.get(url)
        result = r.json()
        return result

    def __request(self, search, inn):
        url = f"{self.URL}/{self.token}/efrsb/{search}/{inn}"
        r = requests.get(url)
        result = r.json()
        return result

    def get_manager(self, inn):
        return self.__request('manager', inn)

    def get_trader(self, inn):
        return self.__request('trader', inn)

    def get_person(self, inn):
        return self.__request('person', inn)

    def get_organisation(self, inn):
        return self.__request('organisation', inn)

    def get_party(self, inn):
        url = f"{self.URL}/{self.token}/dadata/party/{inn}"
        r = requests.get(url)
        result = r.json()
        return result


if __name__ == "__main__":
    s_api = SirotinskyAPI()
    x = s_api.hello('Anton')
