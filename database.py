import sqlite3
import os


class Database:
    def __init__(self, db_path: str = 'employees.db'):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Возвращает соединение с базой данных"""
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """Создает таблицу сотрудников (удаляет существующую)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Удаляем таблицу если она существует
        cursor.execute('DROP TABLE IF EXISTS employees')

        # Создаем новую таблицу
        cursor.execute('''
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                gender TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
        print("Table 'employees' created successfully (old table dropped if existed)")


    def create_index(self):
        """Создает индекс для оптимизации запросов"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_gender_name 
            ON employees(gender, full_name)
        ''')

        conn.commit()
        conn.close()