from flask import Flask, render_template, request, redirect, url_for
from datetime import*
import sqlite3

app = Flask(__name__)

id_man = None

# пример "базы"
RIGHT_EMAIL = "1"
RIGHT_PASSWORD = "1"
email_shef='2'
password_shef='2'
name = 'василий'
do_you_eat = None
@app.route("/")
def start():
    return render_template("start.html")  # всего одна строка!


@app.route("/input_danes", methods=["GET", "POST"])
def input_danes():
    global id_man
    error = None
    print("Запрос пришел:", request.method)  # этот принт должен сработать всегда
    conect = sqlite3.connect("database/data_students.db")
    cur = conect.cursor()
    if request.method == "POST":
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            print(f"Получено: email={email}, password={password}")
            cur.execute("SELECT password_hash, role, id FROM users WHERE login = ?", (email,))
            res = cur.fetchall()
            print(res)
            if res != []:
                if password in res[0][0]:
                    id_man =res[0][2]
                    if res[0][1] == 'ученик':
                    # return redirect(url_for("success"))  # раскомментируйте позже
                        error = "Успешно! (пока просто сообщение)"  # временно, чтобы увидеть
                        return redirect(url_for('index'))  # ПЕРЕНАПРАВЛЯЕМ на главную
                    elif res[0][1] == 'повар':
                        error = "Успешно! (пока просто сообщение)"  # временно, чтобы увидеть
                        return redirect(url_for('shef'))
            else:
                error = "Данные введены некорректно"
                print(error)
    return render_template("input_danes.html", error=error)

error=''

from flask import Flask, request, render_template, redirect, url_for
import sqlite3


@app.route('/regist', methods=["GET", "POST"])
def regist():
    error = None  # Локальная переменная, не global!

    # Создаём соединение внутри функции
    conn = sqlite3.connect("database/data_students.db")
    cur = conn.cursor()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        print(name, password, email)

        if not email or not password or not name:
            error = "Заполните все поля!"
        else:
            # Проверяем, занят ли логин
            cur.execute("SELECT id FROM users WHERE login = ?", (email,))
            x = cur.fetchone()
            print(x)
            if x:  # Если найдено — логин занят
                error = "Данный логин занят"
            else:
                # Хэшируем пароль
                password_hash = password
                # Добавляем пользователя
                cur.execute(f'INSERT INTO users (full_name, login, password_hash, role) VALUES ({name}, {email}, {password_hash}, "ученик")')

                conn.commit()
                conn.close()
                return redirect(url_for('input_danes'))  # Успешная регистрация

    # Если GET или ошибка — показываем форму
    conn.close()  # Закрываем в любом случае
    return render_template("regist.html", error=error)
@app.route('/shef')
def shef():
    return render_template("shef.html")  # всего одна строка!



current_date = datetime.now()
verd = 'Не оплачено'
pays=f' на {current_date.date()}'
@app.route('/index', methods=["GET", "POST"])
def index():
    global verd
    global pays
    global current_date
    global do_you_eat
    global limit
    global id_man
    conn = sqlite3.connect("database/data_students.db")
    cur = conn.cursor()

    cur.execute("SELECT full_name FROM users WHERE id = ?", (id_man,))
    x = cur.fetchone()

    if request.method == "POST":
        action = request.form.get("like")
        if action == "V":
            if do_you_eat==None:
                do_you_eat="Отлично! Вы сказали, что вы поели!"
        if action=="X":
            if do_you_eat==None:
                do_you_eat = "Хорошо! Мы учли это!"
        if action=="Выбрать":
            return render_template("check.html")  # всего одна строка!
        if action=='>':
            current_date = current_date + timedelta(days=1)
            pays = f' на {current_date.date()}'
        if action=='<':
            current_date = current_date - timedelta(days=1)
            pays = f' на {current_date.date()}'
    if limit > timedelta(days=0):
        verd = "Оплачено"
    else:
        verd = "Не оплачено"


    return render_template("index.html", name=x[0], pay=f'{verd}{pays}', eat=do_you_eat)

allerg = None

options = {
    "fish": "Рыба",
    "chic": "Курица",
    "meat": "Мясо",
    "milk": "Молоко",
    "citr": "Цитрус",
    "saxa": "Сахар"
}

limit = timedelta(days=0)
# Страница с чекбоксами
@app.route('/check', methods=['GET', 'POST'])
def check():
    if id_man is None:
        return "Ошибка: пользователь не авторизован"

    # ===== значения по умолчанию =====
    allergies_list = []
    preferences_list = []
    result_text = "Нет данных о твоих предпочтениях и аллергиях."

    options = {
        'fish': 'Рыба',
        'chic': 'Курица',
        'meat': 'Мясо',
        'milk': 'Молоко',
        'citr': 'Цитрус',
        'saxa': 'Сахар'
    }

    conn = sqlite3.connect("database/data_students.db")
    cur = conn.cursor()

    # ===== POST: сохранить данные =====
    if request.method == 'POST':
        allergy = request.form.getlist('allergy')
        preference = request.form.getlist('preference')

        allergy_rus = ','.join([options[a] for a in allergy]) if allergy else None
        preference_rus = ','.join([options[p] for p in preference]) if preference else None

        cur.execute(
            "UPDATE users SET allergies = ?, wont = ? WHERE id = ?",
            (allergy_rus, preference_rus, id_man)
        )
        conn.commit()

    # ===== GET + POST: читаем данные =====
    cur.execute("SELECT allergies, wont FROM users WHERE id = ?", (id_man,))
    row = cur.fetchone()
    conn.close()

    if row:
        allergies_db, wont_db = row

        if allergies_db:
            allergies_list = [
                k for k, v in options.items() if v in allergies_db
            ]

        if wont_db:
            preferences_list = [
                k for k, v in options.items() if v in wont_db
            ]

        # === текст в красном блоке ===
        if not allergies_db and not wont_db:
            result_text = "Нет данных о твоих предпочтениях и аллергиях."
        else:
            a_text = "У тебя нет аллергий." if not allergies_db else f"Аллергии: {allergies_db}."
            w_text = "Нет особых предпочтений." if not wont_db else f"Предпочтения: {wont_db}."
            result_text = f"{a_text} {w_text}"

    return render_template(
        "check.html",
        result_text=result_text,
        allergies_list=allergies_list,
        preferences_list=preferences_list
    )



limit = timedelta(days=0)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    global limit
    global id_man
    cn = 0
    if request.method == "POST":
        action = request.form.get("like")
        conn = sqlite3.connect("database/data_students.db")
        cur = conn.cursor()

        cur.execute("SELECT balance FROM users WHERE id = ?", (id_man, ))
        cn1 = cur.fetchone()[0]

        if action == "Заказать":
            cn1 +=1
        if action == "Заказать ":
            cn1 += 7
        if action == " Заказать":
            cn1 += 30

        limit += timedelta(days=cn1)

        cur.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (cn1, id_man)
        )
        conn.commit()
        conn.close()

    new_date = datetime.now() + limit

    return render_template('pay.html', mes=new_date.strftime("%d.%m.%Y"))  # создай шаблон pay.html

@app.route('/review')
def review():
    return render_template("review.html")  # всего одна строка!


if __name__ == '__main__':
    app.run(debug=True, port=5001)

