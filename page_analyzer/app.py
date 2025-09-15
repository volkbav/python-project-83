import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .repository import UrlRepository
from .validator import url_validate

DATABASE_URL = os.getenv('DATABASE_URL')

load_dotenv()
app = Flask(__name__)
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


@app.post("/")
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
   
    return redirect(url_for('urls_show', id=url["id"]), code=302) 

# тут надо поправить вывод данных в таблицу
@app.route("/urls")
def urls_index():
    urls = repo.get_all_urls()

    return render_template(
        "urls/index.html",
        urls=urls,
    )
#---

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

    status_code = None
    h1 = None
    title = None
    description = None
    
    data = {
        'url_id': id,
        'status_code': status_code,
        'h1': h1,
        'title': title,
        'description': description
    }

    repo.check_url_save(data)
    return redirect(url_for('urls_show', id=id), code=302)
