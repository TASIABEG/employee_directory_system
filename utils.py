import random
from datetime import datetime, timedelta
from models import Employee


def generate_random_employee() -> Employee:
    """Генерирует случайного сотрудника"""
    first_names = ["John", "Michael", "Robert", "David", "William", "James", "Thomas",
                   "Christopher", "Daniel", "Matthew", "Elizabeth", "Mary", "Jennifer",
                   "Linda", "Patricia", "Susan", "Barbara", "Jessica", "Sarah", "Karen"]

    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
                  "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
                  "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

    # Случайное ФИО
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    middle_name = random.choice(first_names)
    full_name = f"{last_name} {first_name} {middle_name}"

    # Случайная дата рождения (от 18 до 65 лет назад)
    end_date = datetime.now() - timedelta(days=365 * 18)
    start_date = end_date - timedelta(days=365 * 47)
    # Генерируем случайную дату, избегая 29 февраля
    while True:
        random_days = random.randint(0, (end_date - start_date).days)
        birth_date = start_date + timedelta(days=random_days)

        # Проверяем, не 29 февраля ли это
        if not (birth_date.month == 2 and birth_date.day == 29):
            break

    gender = random.choice(["Male", "Female"])

    return Employee(full_name, birth_date.strftime('%Y-%m-%d'), gender)

def generate_specific_employees(count: int = 100) -> list:
    """Генерирует сотрудников мужского пола с фамилией на 'F'"""
    f_last_names = ["Fisher", "Foster", "Fox", "Ford", "Fleming", "Fletcher", "Fields",
                    "Ferguson", "Farmer", "Fowler", "Franklin", "Freeman", "Fulton"]

    first_names = ["John", "Michael", "Robert", "David", "William", "James", "Thomas"]

    employees = []
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(f_last_names)
        middle_name = random.choice(first_names)
        full_name = f"{last_name} {first_name} {middle_name}"

        # Дата рождения (от 18 до 65 лет назад)
        end_date = datetime.now() - timedelta(days=365 * 18)
        start_date = end_date - timedelta(days=365 * 47)
        random_days = random.randint(0, (end_date - start_date).days)
        birth_date = start_date + timedelta(days=random_days)

        employees.append(Employee(full_name, birth_date.strftime('%Y-%m-%d'), "Male"))

    return employees