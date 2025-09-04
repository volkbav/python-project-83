import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from .repository import conn, UrlRepository

load_dotenv()
app = Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
repo = UrlRepository(conn)


@app.get("/") 
def index():
    return render_template(
        "index.html", 
        url={"name": ""},
        errors={}
    )

@app.post("/")
def urls_add():
    url = {
        "name": request.form.get("name", "")
    }
    errors = repo.validate(url)
    if errors:
        return render_template(
            "/",
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
    url = repo.find(id)
    pass

