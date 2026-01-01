from flask import Flask, render_template, request, redirect, url_for
from datetime import*

app = Flask(__name__)

# пример "базы"
RIGHT_EMAIL = "1"
RIGHT_PASSWORD = "1"
name = 'василий'
do_you_eat = None
@app.route("/")
def start():
    return render_template("start.html")  # всего одна строка!


@app.route("/input_danes", methods=["GET", "POST"])
def input_danes():
    error = None
    print("Запрос пришел:", request.method)  # этот принт должен сработать всегда
    if request.method == "POST":
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            print(f"Получено: email={email}, password={password}")

            if email == RIGHT_EMAIL and password == RIGHT_PASSWORD:
                # return redirect(url_for("success"))  # раскомментируйте позже

                error = "Успешно! (пока просто сообщение)"  # временно, чтобы увидеть
                return redirect(url_for('index'))  # ПЕРЕНАПРАВЛЯЕМ на главную

            else:
                error = "Данные введены некорректно"
                print(error)

            # Передаём error в шаблон. Если error=None, можно не показывать
    return render_template("input_danes.html", error=error)

@app.route('/regist')
def regist():
    return render_template("regist.html")  # всего одна строка!


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


    return render_template("index.html", name=name, pay=f'{verd}{pays}', eat=do_you_eat)

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

    result_text = "Твои аллергии и предпочтения появятся здесь после нажатия на кнопку."

    if request.method == 'POST':
        allergy = request.form.getlist('allergy')
        preference = request.form.getlist('preference')

        allergy_rus = [options.get(val, val) for val in allergy]
        preference_rus = [options.get(val, val) for val in preference]

        parts = []
        if allergy_rus:
            parts.append(f"У тебя аллергия на: {', '.join(allergy_rus)}.")
        if preference_rus:
            parts.append(f"Ты особенно любишь: {', '.join(preference_rus)}.")

        if not parts:
            result_text = "У тебя нет аллергии и особых предпочтений. Можно всё! 😊"
        else:
            result_text = " ".join(parts)

    return render_template('check.html', result_text=result_text)
limit = timedelta(days=0)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    global limit
    if request.method == "POST":
        action = request.form.get("like")
        if action == "Заказать":
            limit += timedelta(days=1)
        if action == "Заказать ":
            limit += timedelta(days=7)
        if action == " Заказать":
            limit += timedelta(days=30)
    new_date = datetime.now() + limit

    return render_template('pay.html', mes=new_date.strftime("%d.%m.%Y"))  # создай шаблон pay.html


if __name__ == '__main__':
    app.run(debug=True, port=5001)

