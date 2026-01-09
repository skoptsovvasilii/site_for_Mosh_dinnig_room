'''

Вот основные **SQL-команды** для работы с базой данных в твоём проекте (SQLite). Я приведу их с примерами именно под твою схему (таблица `users` и другие). Ты можешь выполнять эти команды либо напрямую в Python через `sqlite3`, либо в инструментах вроде DB Browser for SQLite для тестов.

### 1. Создание таблиц (один раз, при инициализации БД)
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('ученик', 'повар', 'администратор')),
    class TEXT,
    allergies TEXT
);

CREATE TABLE IF NOT EXISTS menu ( ... );  -- остальные таблицы аналогично
```

### 2. Добавление данных (INSERT)
```sql
-- Добавить ученика
INSERT INTO users (full_name, login, password_hash, role, class, allergies)
VALUES ('Иванов Иван', 'ivanov123', 'хэш_пароля', 'ученик', '10А', 'орехи');

-- Добавить блюдо в меню
INSERT INTO menu (date, meal_type, dish_name, price)
VALUES ('2026-01-03', 'обед', 'Котлета с пюре', 150.00);
```

### 3. Просмотр данных (SELECT)
```sql
-- Все пользователи
SELECT * FROM users;

-- Только ученики
SELECT * FROM users WHERE role = 'ученик';

-- Ученики 10А класса
SELECT full_name, allergies FROM users WHERE role = 'ученик' AND class = '10А';

-- Меню на сегодня
SELECT * FROM menu WHERE date = '2026-01-03';
```

### 4. Изменение данных (UPDATE)
```sql
-- Изменить аллергии ученика
UPDATE users SET allergies = 'орехи, молоко' WHERE login = 'ivanov123';

-- Изменить пароль (новый хэш)
UPDATE users SET password_hash = 'новый_хэш' WHERE id = 5;

-- Согласовать заявку на закупку
UPDATE purchase_requests SET status = 'согласовано', admin_id = 3 WHERE id = 10;
```

### 5. Удаление данных (DELETE)
```sql
-- Удалить пользователя (осторожно!)
DELETE FROM users WHERE id = 5;

-- Удалить старое меню
DELETE FROM menu WHERE date < '2025-01-01';

-- Удалить отзыв
DELETE FROM reviews WHERE id = 7;
```

### 6. Проверка существования данных
```sql
-- Проверить, занят ли логин при регистрации
SELECT id FROM users WHERE login = 'ivanov123';

-- Проверить, взял ли ученик еду сегодня (чтобы запретить повтор)
SELECT id FROM meal_records
WHERE user_id = 42 AND date(received_at) = '2026-01-03';
```

### 7. Полезные дополнительные команды
```sql
-- Посчитать количество учеников
SELECT COUNT(*) FROM users WHERE role = 'ученик';

-- Сумма оплат за период
SELECT SUM(amount) FROM payments
WHERE paid_at BETWEEN '2026-01-01' AND '2026-01-31';

-- Статистика посещаемости по классам
SELECT class, COUNT(*) as visits
FROM users u
JOIN meal_records m ON u.id = m.user_id
WHERE m.received_at >= '2026-01-01'
GROUP BY class;

-- Поиск по фамилии (для интерфейса повара)
SELECT id, full_name FROM users
WHERE role = 'ученик' AND full_name LIKE '%Иванов%';
```

### Как выполнять эти команды в Python (sqlite3)
```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Пример выполнения любой команды
cursor.execute("SELECT * FROM users WHERE role = ?", ('ученик',))
results = cursor.fetchall()  # получить все строки

for row in results:
    print(row)

# Для INSERT/UPDATE/DELETE не забудь сохранить изменения
conn.commit()

conn.close()
```

### Полезные советы
- Всегда используй **параметризованные запросы** (`?` и кортеж значений) — это защита от SQL-инъекций.
- Добавляй **индексы** для ускорения:
  ```sql
  CREATE INDEX idx_users_role ON users(role);
  CREATE INDEX idx_meal_records_date ON meal_records(received_at);
  ```
- Для тестов создай файл `init_db.py` с созданием таблиц и тестовыми данными.

Эти команды покрывают **99%** того, что тебе понадобится в проекте. Если нужно — могу дать готовый скрипт инициализации всей БД с тестовыми данными. Удачи на олимпиаде!

'''

import sqlite3
"""
#conect = sqlite3.connect("database/data_students.db")
cur = conect.cursor()

cur.execute('''
    CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('ученик', 'повар', 'администратор')),
    wont TEXT,
    allergies TEXT,
    balance REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
''')

conect.commit()
#cur.execute('INSERT INTO users (username, email) VALUES ("Vasy", "skoptsov.vasilii@yandex.ru")')
conect.commit()



"""


cur.execute('''
    CREATE TABLE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('ученик', 'повар', 'администратор')),
    wont TEXT,
    allergies TEXT,
    balance REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
''')
