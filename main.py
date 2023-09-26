from flask import Flask, render_template, request, redirect, url_for
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# from wtf_forms import

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    books = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"],
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit/<int:num>", methods=["GET", "POST"])
def edit(num):
    to_edit = db.session.execute(db.select(Book).filter_by(id=num)).scalar()
    if request.method == "POST":
        to_edit = db.session.execute(db.select(Book).filter_by(id=num)).scalar()
        to_edit.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", book=to_edit)


@app.route("/delete")
def delete():
    num = request.args.get('id')
    book = db.get_or_404(Book, num)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)

