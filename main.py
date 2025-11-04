import sys
import time
from database import Database
from models import Employee
from utils import generate_random_employee, generate_specific_employees


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <mode> [arguments]")
        sys.exit(1)

    mode = sys.argv[1]
    db = Database()

    if mode == "1":
        # Режим 1: Создание таблицы (с удалением существующей)
        db.create_table()

    elif mode == "2":
        # Режим 2: Создание записи сотрудника
        if len(sys.argv) != 5:
            print("Usage: python main.py 2 \"Full Name\" YYYY-MM-DD Gender")
            sys.exit(1)

        full_name = sys.argv[2]
        birth_date = sys.argv[3]
        gender = sys.argv[4]

        employee = Employee(full_name, birth_date, gender)
        conn = db.get_connection()
        employee.save_to_db(conn)
        conn.close()

        age = employee.calculate_age()
        print(f"Employee saved successfully. Age: {age} years")

    elif mode == "3":
        # Режим 3: Вывод всех уникальных сотрудников
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT full_name, birth_date, gender 
            FROM employees 
            ORDER BY full_name
        ''')

        employees = cursor.fetchall()
        conn.close()

        print("Employees (unique by full_name + birth_date):")
        print("Full Name | Birth Date | Gender | Age")
        print("-" * 50)

        for full_name, birth_date, gender in employees:
            employee = Employee(full_name, birth_date, gender)
            age = employee.calculate_age()
            print(f"{full_name} | {birth_date} | {gender} | {age}")

    elif mode == "4":
        # Режим 4: Автоматическое заполнение
        conn = db.get_connection()

        # Генерация 1,000,000 случайных сотрудников
        print("Generating 1,000,000 random employees...")
        batch_size = 10000
        total_employees = 1000000

        for i in range(0, total_employees, batch_size):
            batch = [generate_random_employee() for _ in range(min(batch_size, total_employees - i))]
            Employee.save_batch(conn, batch)
            print(f"Generated {i + len(batch)} employees...")

        # Генерация 100 специфических сотрудников
        print("Generating 100 specific employees (Male, last name starts with 'F')...")
        specific_employees = generate_specific_employees(100)
        Employee.save_batch(conn, specific_employees)

        conn.close()
        print("Data generation completed successfully")

    elif mode == "5":
        # Режим 5: Вывод данных и замер времени выполнения запроса
        conn = db.get_connection()
        cursor = conn.cursor()

        start_time = time.time()

        cursor.execute('''
            SELECT * FROM employees 
            WHERE gender = 'Male' AND full_name LIKE 'F%'
        ''')

        results = cursor.fetchall()
        end_time = time.time()

        execution_time = end_time - start_time

        print(f"Query execution time: {execution_time:.4f} seconds")
        print(f"Found {len(results)} records:")

        # Ограничим вывод до первых 20 записей, чтобы не засорять консоль
        if len(results) > 20:
            print(f"Showing first 20 of {len(results)} records:")
            results = results[:20]

        print("ID | Full Name | Birth Date | Gender")
        print("-" * 60)

        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

        conn.close()

    elif mode == "6":
        # Режим 6: Оптимизация и повторный замер
        print("Creating index for optimization...")
        db.create_index()

        # Повторный замер времени
        conn = db.get_connection()
        cursor = conn.cursor()

        start_time = time.time()

        cursor.execute('''
            SELECT * FROM employees 
            WHERE gender = 'Male' AND full_name LIKE 'F%'
        ''')

        results = cursor.fetchall()
        end_time = time.time()

        conn.close()

        execution_time = end_time - start_time
        print(f"Query execution time after optimization: {execution_time:.4f} seconds")
        print(f"Found {len(results)} records")

    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: 1, 2, 3, 4, 5, 6")


if __name__ == "__main__":
    main()