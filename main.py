from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Movies.db"
Bootstrap5(app)
# CREATE DB
class Base(DeclarativeBase):
    pass
db = SQLAlchemy()
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

#Manually create a record
#with app.app_context():
#    db_new_book = Movie(
#    title="Avatar The Way of Water",
#    year=2022,
#    description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#    rating=7.3,
#    ranking=9,
#    review="I liked the water.",
#    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#)
#    db.session.add(db_new_book)
#    db.session.commit()

@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie))
        movies = result.scalars().all()
    return render_template("index.html", movies = movies)


if __name__ == '__main__':
    app.run(debug=True)
