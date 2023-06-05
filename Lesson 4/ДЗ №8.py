# Задание

# Описать любую абстракцию с помощью инструментов ООП.
# Придумать атрибуты и методы для абстракции.

class HSE_Student:

    def __init__(self, name: str, age: int, campus: str, average_grade: str):
        self.name = name
        self.age = age
        self.campus = campus
        self.average_grade = average_grade
        self.is_try_to_study = False

    def start_study(self):
        self.is_try_to_study = True
        print("Студент начал стараться на учебе")

    def stop_study(self):
        self.is_try_to_study = False
        print("Студент перестал стараться в учебных делах")

    def student_description(self):
        print(f"{self.name} ({self.age} лет от роду), обучающийся в корпусе: {self.campus} "
              f"и учащийся в среднем на {self.average_grade} баллов.")


student_1 = HSE_Student('Антон', 23, 'Покровка', '9.8')
