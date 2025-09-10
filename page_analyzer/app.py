import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request

from .repository import UrlRepository
from .validator import url_validate

DATABASE_URL = os.getenv('DATABASE_URL')

load_dotenv()
app = Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = psycopg2.connect(DATABASE_URL)
repo = UrlRepository(conn)


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
    
    repo.save(url)
    flash("Страница успешно добавлена", "success")
    # --- to delete
    """
    неправильный redirect - нужно направить на "/urls/<id>" через url_for. 
    Но пока нет этого обработчика...
    """
    # --- to delete
    return redirect("/urls", code=302) 


@app.route("/urls")
def urls_index():
    urls = repo.get_all()

    return render_template(
        "urls/index.html",
        urls=urls,
    )


@app.route("/urls/<int:id>")
def urls_show(id):
    return render_template(
        "urls/show_url.html"
    )

