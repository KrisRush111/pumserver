from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

# Файл для хранения пользователей
USERS_FILE = "users.json"

# Загружаем пользователей
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}


@app.route("/start", methods=["POST"])
def start():
    data = request.json
    user_id = str(data.get("user_id"))
    username = data.get("username", "Гость")

    if user_id:
        users[user_id] = username
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        return jsonify({"status": "ok", "message": "Username сохранен"})
    return jsonify({"status": "error", "message": "Некорректные данные"})


@app.route("/get_user/<user_id>", methods=["GET"])
def get_user(user_id):
    username = users.get(user_id, "Гость")
    return jsonify({"name": username})


@app.route("/menu")
def menu():
    with open("menu.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return render_template_string(html_content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
