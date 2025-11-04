import sqlite3
from datetime import datetime, date
from typing import List


class Employee:
    def __init__(self, full_name: str, birth_date: str, gender: str):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def save_to_db(self, conn: sqlite3.Connection):
        """Сохраняет сотрудника в базу данных"""
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)",
            (self.full_name, self.birth_date, self.gender)
        )
        conn.commit()

    def calculate_age(self) -> int:
        """Рассчитывает полных лет на текущую дату"""
        try:
            birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birth_date.year

            # Проверяем, был ли уже день рождения в этом году
            try:
                # Пробуем создать дату дня рождения в текущем году
                birthday_this_year = birth_date.replace(year=today.year)
            except ValueError:
                # Если день рождения 29 февраля, а текущий год не високосный,
                # используем 28 февраля
                if birth_date.day == 29 and birth_date.month == 2:
                    birthday_this_year = date(today.year, 2, 28)
                else:
                    raise

            if today < birthday_this_year:
                age -= 1

            return age
        except Exception as e:
            print(f"Error calculating age for {self.birth_date}: {e}")
            return 0

    @staticmethod
    def save_batch(conn: sqlite3.Connection, employees: List['Employee']):
        """Пакетное сохранение сотрудников в базу данных"""
        cursor = conn.cursor()
        data = [(emp.full_name, emp.birth_date, emp.gender) for emp in employees]
        cursor.executemany(
            "INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)",
            data
        )
        conn.commit()