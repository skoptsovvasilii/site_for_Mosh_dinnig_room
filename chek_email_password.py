from flask import Flask, render_template, request, redirect, url_for, session
from datetime import*
from flask import Flask, render_template, request, redirect, url_for, session

import sqlite3

app = Flask(__name__)
app.secret_key = '26a5d8bc12a7e9f635b1d5c982a4d8eb'


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
    session.pop('id', None)
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
                    session['id'] = id_man

                    if res[0][1] == 'ученик':
                    # return redirect(url_for("success"))  # раскомментируйте позже
                        error = "Успешно! (пока просто сообщение)"  # временно, чтобы увидеть
                        return redirect(url_for('index'))  # ПЕРЕНАПРАВЛЯЕМ на главную
                    elif res[0][1] == 'повар':
                        error = "Успешно! (пока просто сообщение)"  # временно, чтобы увидеть
                        return redirect(url_for('shef'))
                    elif res[0][1] == 'администратор':
                        error = "Успешно! (пока просто сообщение)"  # временно, чтобы увидеть
                        return redirect(url_for('admin'))
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
                cur.execute(
                    'INSERT INTO users (full_name, login, password_hash, role) VALUES (?, ?, ?, ?)',
                    (name, email, password_hash, "ученик")
                )
                conn.commit()
                conn.close()
                return redirect(url_for('input_danes'))  # Успешная регистрация

    # Если GET или ошибка — показываем форму
    conn.close()  # Закрываем в любом случае
    return render_template("regist.html", error=error)

@app.route('/shef', methods=["GET", "POST"])
def shef():
    mes = ''
    flag = None
    conn = sqlite3.connect("database/data_students.db")
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM users')
    count_dano = cur.fetchall()[0][0]
    print(count_dano)
    count_dano-=2

    if request.method == "POST":

        action = request.form.get("like")
        name = request.form.get("name")
        print(name, ' - name')

        if action=="Поиск":
            cur.execute("SELECT id FROM users WHERE full_name = ?", (name, ))
            x = cur.fetchone()
            if x is not None:
                session['search_name'] = name  # Сохраняем имя в сессии

                ides = x[0]
                print(ides)

                return render_template("shef.html", flag=1, full_name=name)  # всего одна строка!
        if action=="V":
            name = session.get('search_name')  # Берём имя из сессии
            print(name, "V - name")

            conn_eat = sqlite3.connect("database/data_students.db")
            cur = conn_eat.cursor()

            cur.execute("SELECT id FROM users WHERE full_name = ?", (name, ))
            x = cur.fetchone()
            conn_eat1 = sqlite3.connect("database/eat_check.db")
            cur1 = conn_eat1.cursor()
            #cur1.execute("SELECT id FROM users WHERE full_name = ?", (name, ))
            #x1 = cur.fetchone()
            print(x, "- x")
            if x is not None:
                ide = x[0]
                #cur1.execute(
                #    f'INSERT INTO eat_check (id, student, sheff, answer) VALUES ({ide}, {1}, {1}, {1})')
                cur1.execute("SELECT date FROM eat_check WHERE id = ?", (ide,))
                try:
                    dat = cur1.fetchall()[-1][0]
                except:
                    dat = '1900-01-01'
                print(dat)
                dt_object = datetime.strptime(dat, "%Y-%m-%d %H:%M:%S").date()
                nw = datetime.now().date()
                if nw==dt_object:
                    cur1.execute("UPDATE eat_check SET answer = 1 WHERE id = ? AND date = ?", (ide, dat))
                else:
                    cur1.execute(
                        f'INSERT INTO eat_check (id, student, sheff,  answer) VALUES ({ide}, {1}, {1}, {1})')
                conn_eat1.commit()
                flag=123
                mes = "Мы отметили, что этот ученик ел"



        if action=='X':
            name = session.get('search_name')  # Берём имя из сессии
            print(name, "V - name")

            conn_eat = sqlite3.connect("database/data_students.db")
            cur = conn_eat.cursor()

            cur.execute("SELECT id FROM users WHERE full_name = ?", (name, ))
            x = cur.fetchone()
            conn_eat1 = sqlite3.connect("database/eat_check.db")
            cur1 = conn_eat1.cursor()
            #cur1.execute("SELECT id FROM users WHERE full_name = ?", (name, ))
            #x1 = cur.fetchone()
            if x is not None:
                ide = x[0]
                # cur1.execute(
                #    f'INSERT INTO eat_check (id, student, sheff, answer) VALUES ({ide}, {1}, {1}, {1})')
                cur1.execute("SELECT date FROM eat_check WHERE id = ?", (ide,))
                try:
                    dat = cur1.fetchall()[-1][0]
                except:
                    dat = "1900-01-01"
                print(dat)
                dt_object = datetime.strptime(dat, "%Y-%m-%d %H:%M:%S").date()
                nw = datetime.now().date()
                if nw == dt_object:
                    cur1.execute("UPDATE eat_check SET answer = 0 WHERE id = ? AND date = ?", (ide, dat))
                else:
                    cur1.execute(
                        f'INSERT INTO eat_check (id, student, sheff,  answer) VALUES ({ide}, {0}, {0}, {0})')

                conn_eat1.commit()
                flag=123
                mes = "Мы отметили, что этот ученик не ел"
        r = {'curret': 'мокровь', 'pottat': 'картошка' , 'apple': 'яблоко','meat': 'мясо', 'fish': 'рыба', 'ion': 'лук', 'tomate': 'помидор', 'check': 'курица' ,'cucamber': 'огурец', "cirle_app":'груша'}
        s = ''
        conect2 = sqlite3.connect("database/data_students.db")
        cur12 = conect2.cursor()






        for key in request.form.keys():
            print(key)
            print(request.form.get(key))
            try:
                if request.form.get(key) != '':
                    s += f'{r[key]}-{request.form.get(key)} '
            except:
                pass
        print(s)
        cur12.execute(
            f'INSERT INTO eat (eat, check1) VALUES (?, ?)', (s, 0))

        conect2.commit()

    conn_eat1 = sqlite3.connect("database/eat_check.db")
    cur1 = conn_eat1.cursor()

    cur1.execute('SELECT * FROM eat_check')
    left = cur1.fetchall()[::-1][:count_dano]
    #print(left)
    for i in left:
        s = datetime.strptime(i[-1], '%Y-%m-%d %H:%M:%S')
        s = s.date()
        print(s)
        print(date.today())
        if date.today()==s:
            count_dano -= i[3]




    if flag == 123:
        return render_template("shef.html", flag=123, mes=mes, cn=count_dano)  # всего одна строка!
    else:
        return render_template("shef.html", flag=flag, mes=mes, cn=count_dano)



current_date = date.today()
print(current_date)
verd = 'Не оплачено'
pays=f' на {current_date}'
@app.route('/index', methods=["GET", "POST"])
def index():
    global verd
    global pays
    global current_date
    global limit
    global do_you_eat
    do_you_eat =None
    conn = sqlite3.connect("database/data_students.db")
    cur = conn.cursor()


    id_man = session.get('id')

    cur.execute("SELECT balance FROM users WHERE id = ?", (id_man,))
    x = cur.fetchone()
    cur.execute("SELECT full_name FROM users WHERE id = ?", (id_man,))
    x123 = cur.fetchone()
    conn1 = sqlite3.connect("database/eat_check.db")
    cur1 = conn1.cursor()
    if request.method == "POST":
        action = request.form.get("like")
        print(current_date)

        cur1.execute("SELECT * FROM eat_check WHERE id = ? ORDER BY date ASC", (id_man,))
        results = cur1.fetchall()
        dt = datetime.now()
        print(dt)
        x1=None

        for row in results[::-1]:
            print()
            s = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            s = s.date()
            print(s)
            if s>=dt.date():
                print(1234567856432456)

                if row[3] in [1, 0]:
                    x1 = row[3]
                    break
        #cur1.execute("SELECT answer FROM eat_check WHERE id = ? AND DATE(date)", (id_man, current_date))
        #x1 = cur.fetchone()
        print(x1)
        print(x)
        if x1 == None:
            if action == "V":
                if x[0]>=1:
                    do_you_eat="Отлично! Вы сказали, что вы поели!"
                    cur.execute(
                        "UPDATE users SET balance = ? WHERE id = ?",
                        (x[0]-1, id_man)
                    )
                    cur1.execute(
                        f'INSERT INTO eat_check (id, student, answer) VALUES ({id_man}, {1},  {1})')
                    conn1.commit()

                else:
                    do_you_eat = "У Вас недостаточно средств"


            if action=="X":
                if x[0]>=1:
                    cur1.execute(
                        f'INSERT INTO eat_check (id, student, answer) VALUES ({id_man}, {0},  {0})')
                    conn1.commit()
                    do_you_eat = "Хорошо! Мы учли это!"
                else:
                    do_you_eat = "У Вас недостаточно средств"

        else:
            if x1 == 1:
                do_you_eat = 'Сегодня Вы у нас по ели'
            if x1==0:
                do_you_eat = "Сегодня Вы у нас не ели"

        if action=="Выбрать":
            return render_template("check.html")  # всего одна строка!
        if action=='>':
            current_date = current_date + timedelta(days=1)
            current_date = current_date
            pays = f' на {current_date}'
        if action=='<':
            current_date = current_date - timedelta(days=1)
            current_date = current_date
            pays = f' на {current_date}'


    if limit > timedelta(days=0):
        verd = "Оплачено"
    else:
        verd = "Не оплачено"
    cur1.execute("SELECT * FROM eat_check WHERE id = ? ORDER BY date ASC", (id_man,))
    results = cur1.fetchall()

    dt = datetime.now()
    x1 = None

    for row in results[::-1]:
        print()
        s = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
        s = s.date()
        print(s)


        if s >= dt.date():
            print(1234567856432456)

            if row[3] in [1, 0]:
                x1 = row[3]
                break

    if x1!=None:
        if x1 == 1:
            do_you_eat = 'Сегодня Вы у нас поели'
        if x1 == 0:
            do_you_eat = "Сегодня Вы у нас не ели"

    cnn = sqlite3.connect("database/eat_check.db")
    cr = cnn.cursor()

    today = date.today()

    weekday_number = current_date.weekday()+1
    cr.execute("SELECT breakfast, lunch FROM menu WHERE day = ?", (weekday_number,))
    et = cr.fetchall()
    print(et[0][0].split(","))
    allergy_replacements = {
        "рыба": [
            ["котлета рыбная", "рыба лук"],
            ["сырники со сгущенным молоком"]
        ],
        "курица": [
            ["суп вермишель курица", "котлеты куриные", "суп куриный", 'лапша домашняя курица', "суп куриный сухарики"],
            ["гречневая каша"]
        ],
        "мясо": [
            ["гуляш свинина гречка", "биточки мясные макароны", "телятина картофель",
             "суфле мясо", "котлета рыбная паровая", "говядина в щах", "свинина в гуляше"],
            ["яблоко свежее"]
        ],
        "молоко": [
            ["творожники сметана", "сырники сгущёнка", "вареники творог",
             "йогурт", "рис молоко", "кефир", "кукурузные хлопья йогурт", 'творог мёд орехи', 'ватрушка творог'],
            ["винегрет овощной"]
        ],
        "цитрус": [
            ["чай лимон", "сок апельсин", "лимонад апельсин"],
            ["компот яблочный"]
        ],
        "сахар": [
            ["компот яблочный", "хлебцы джем", "пирожки капуста", "миндаль", "халва подсолнечник"],
            ["картофель отварной с растительным маслом"]
        ]
    }
    conn3 = sqlite3.connect("database/data_students.db")
    cur3 = conn.cursor()


    cur3.execute("SELECT allergies, wont FROM users WHERE id = ?", (id_man,))
    row = cur3.fetchone()




    br = []
    ln =[]
    for i in range(len(et[0][0].split(","))):
        #print(i)
        br.append([i+1, et[0][0].split(',')[i], et[0][1].split(',')[i]])
    print(br)


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
        print(allergies_db)
        if allergies_db is not None:
            for h in allergies_db.split(','):
                h = h.lower()
                cn = 0

               # print(allergy_replacements[h][0])
                for i, j, k in br:
                    if j[0]== " ":
                        j = j[1:]
                    if j in allergy_replacements[h][0]:
                        print(allergy_replacements[h][1], ' - ', br[cn][1])
                        br[cn][1]=allergy_replacements[h][1][0]

                    if k[0]== " ":
                        k = k[1:]
                    if k in allergy_replacements[h][0]:
                        print(allergy_replacements[h][1], ' - ', br[cn][2])
                        br[cn][2]=allergy_replacements[h][1][0]
                    cn+=1








    return render_template("index.html", name=x123[0], pay=f'{verd}{pays}', eat=do_you_eat, br=br)

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
    id_man = session.get('id')

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
        for i in allergy:
            if i in preference:
                result_text = "Ты предпочитаешь то, на что у тебя аллергия! Это неправильно"
                return render_template(
                    "check.html",
                    result_text=result_text,
                    allergies_list=allergies_list,
                    preferences_list=preferences_list
                )

        allergy_rus = ','.join([options[a] for a in allergy]) if allergy  else None
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
    id_man = session.get('id')
    cn = 0
    if request.method == "POST":
        action = request.form.get("like")
        conn = sqlite3.connect("database/data_students.db")
        cur = conn.cursor()

        cur.execute("SELECT balance FROM users WHERE id = ?", (id_man, ))
        cn1 = cur.fetchone()[0]
        print(cn1)

        if action == "Заказать":
            cn1 +=1
        if action == "Заказать ":
            cn1 += 7
        if action == " Заказать":
            cn1 += 30

        name = request.form.get("total")
        if name is not None:
            cn1+=int(name)//1000

        limit = timedelta(days=cn1)

        cur.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (cn1, id_man)
        )
        conn.commit()
        conn.close()

    new_date = datetime.now() + limit

    return render_template('pay.html', mes=new_date.strftime("%d.%m.%Y"))  # создай шаблон pay.html

@app.route('/review', methods=['GET', 'POST'])
def review():
    id_man = session.get('id')
    conn = sqlite3.connect("database/rev.db")
    cur = conn.cursor()

    if request.method == "POST":
        action = request.form.get("like")
        if action == 'Отправить':
            name = request.form.get("coment")
            print(name)

            if name is not None:
                cur.execute(
                    'INSERT INTO review (id, comment) VALUES (?, ?)', (id_man, name))
                conn.commit()

    cur.execute("SELECT * FROM review")
    # Получаем все строки
    rows = cur.fetchall()
    # Выбираем последние 10 записей
    last_10_records = rows[-10:][::-1]
    lst = []
    for i in last_10_records:
        lst.append(i[1])
    print(lst)

    return render_template("review.html", lst=lst)  # всего одна строка!


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect("database/eat_check.db")
    cur = conn.cursor()
    cur.execute('SELECT * FROM eat_check LIMIT 60')
    cn1 = cur.fetchall()[::-1]
    count = 0
    count_z = 0
    print(cn1)
    count_l = 0
    count_zl = 0
    for i in cn1:
        dt_object = datetime.strptime(i[-1], "%Y-%m-%d %H:%M:%S").date()
        if dt_object>=(datetime.now().date()-timedelta(days=30)):
            count +=i[3]
            if i[3]==0:
                count_z+=1
        if  (datetime.now().date()-timedelta(days=30))>=dt_object>=(datetime.now().date()-timedelta(days=60)):
            count_l+=i[3]
            if i[3]==0:
                count_zl+=1

    conect2 = sqlite3.connect("database/data_students.db")
    cur12 = conect2.cursor()
    cur12.execute("SELECT eat FROM eat WHERE check1 = ?", (0, ))

    print(cn1)
    lst=[]
    flag=None
    cn1 = cur12.fetchall()
    print(cn1)
    if cn1 != []:
        flag='True'
        cn1 = cn1[-1][0]
        for i in cn1.split():
            print(i)
            lst.append([i.split('-')[0], i.split('-')[1]])
        if request.method == "POST":
            action = request.form.get("like")
            if action=='Согласовать':
                cur12.execute("UPDATE eat SET check1 = 1 WHERE eat=?", (cn1, ))
                conect2.commit()
            if action=='Не согласовать':
                cur12.execute("UPDATE eat SET check1 = 1 WHERE eat=?", (cn1, ))
                conect2.commit()
    print(flag)



    return render_template("admin.html", z=count_z, go=count, pays=count*1000, lst=lst, fl=flag, zl = count_zl, gol=count_l, pa=count_l*1000)





if __name__ == '__main__':
    app.run(debug=True, port=5001)

