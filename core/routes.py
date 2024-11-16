from flask import render_template, request, redirect, url_for


from core import app
from core.db import get_posts, get_post, save_post, del_post, change_post, allowed_file


@app.route("/", methods=["GET"])
def index():
    search = request.args.get("search")
    posts = get_posts(search=search)
    return render_template("index.html", posts=posts)


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        save_post(title, description)
        return redirect(url_for("index"))
    return render_template("add_post.html")


@app.route("/posts/<int:id>")
def post_detail(id):
    post = get_post(id)
    return render_template("post_detail.html", post=post)


@app.route("/delete/<int:id>", methods=["POST"])
def del_post_fr(id):
    del_post(id)
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_post_fr(id):
    if request.method == "POST":
        title_n = request.form.get("title")
        description_n = request.form.get("description")
        change_post(id, title_n, description_n)
        return redirect(url_for("index"))

    post = get_post(id)
    if not post:
        return redirect(url_for("index"))

    return render_template("edit_post.html", post=post)
