import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .parser import parse_content
from .repository import UrlRepository
from .validator import url_validate

load_dotenv()
# читаем путь до БД (url) из .env
DATABASE_URL = os.getenv('DATABASE_URL')
# используется для условия сохранения результатов запроса
ERROR_CODE = 500

# подгружает данные из .env
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

repo = UrlRepository(DATABASE_URL)


# Обработчит главной страницы
@app.get("/") 
def index():
    return render_template(
        "index.html", 
        url={'name': ''},
        errors={}
    )


# Обработчик формы на главной странице
@app.post("/urls")
def urls_add():
    url = {
        'name': request.form.get("url", "")
    }
    errors = url_validate(url["name"])
    if errors:
        return render_template(
            "index.html",
            url=url,
            errors=errors,
        ), 422
    
    flash_type, url_id = repo.save(url)
    
    if flash_type == "success":
        flash("Страница успешно добавлена", "success")
    elif flash_type == "exist":
        flash("Страница уже существует", "primary")
   
    return redirect(url_for('urls_show', id=url_id), code=302) 


# вывод проверенных сайтов (таблица)
@app.get("/urls")
def urls_index():
    urls = repo.get_all_urls()

    return render_template(
        "urls/index.html",
        urls=urls,
    )


# вывод конкретного сайта
@app.route("/urls/<int:id>")
def urls_show(id):
    url = repo.find_by_id(id)
    checks = repo.get_all_checks(id)
    return render_template(
        "urls/show_url.html",
        url=url,
        checks=checks
    )


# обработчик кнопки "запустить проверку"
@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_check(id):
    url = repo.find_by_id(id)['name']
    data = parse_content(url, id)

    if data['status_code'] < ERROR_CODE:
        repo.check_url_save(data)
        flash("Страница успешно проверена", "success")
    else:
        flash("Произошла ошибка при проверке", "danger")
    
    return redirect(url_for('urls_show', id=id), code=302)
    
