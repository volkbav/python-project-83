import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .parser import parse_content
from .repository import UrlRepository
from .validator import url_validate

DATABASE_URL = os.getenv('DATABASE_URL')
ERROR_CODE = 500

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

repo = UrlRepository(DATABASE_URL)


@app.get("/") 
def index():
    return render_template(
        "index.html", 
        url={'name': ''},
        errors={}
    )


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
    
    flash_type = repo.save(url)
    
    if flash_type == "success":
        flash("Страница успешно добавлена", "success")
    elif flash_type == "exist":
        flash("Страница уже существует", "primary")
   
    return redirect(url_for('urls_index'), code=302) 


@app.get("/urls")
def urls_index():
    urls = repo.get_all_urls()

    return render_template(
        "urls/index.html",
        urls=urls,
    )


@app.route("/urls/<int:id>")
def urls_show(id):
    url = repo.find_by_id(id)
    checks = repo.get_all_checks(id)
    return render_template(
        "urls/show_url.html",
        url=url,
        checks=checks
    )


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
    
