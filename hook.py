from flask import Flask, send_file, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def base():
    return 'nothing hear'

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    # Обработка полученных данных, если нужно

    # Путь к файлу, который надо отдать
    filepath = 'data.xlsx'

    # Отдаём файл клиенту
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)