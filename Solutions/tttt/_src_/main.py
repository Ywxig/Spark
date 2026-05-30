from flask import Flask, render_template

# Инициализация приложения
app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    # Можно вернуть просто строку или отрендерить HTML-шаблон
    return render_template("index.html")

# Запуск сервера
if __name__ == '__main__':
    # debug=True позволяет серверу перезагружаться при изменении кода
    app.run(debug=True)