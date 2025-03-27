import os
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from edit_form import EditForm
from add_form import AddForm

URL = "https://api.themoviedb.org/3/search/movie?"
URL_FIND = 'https://api.themoviedb.org/3/movie/'
URL_IMAGE = 'https://image.tmdb.org/t/p/w500'
KEY = os.environ["API_KEY"]
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {KEY}"
}

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

@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating))
        movies = result.scalars().all()

    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i
    db.session.commit()

    return render_template("index.html", movies = movies)

@app.route('/add', methods=["GET", "POST"])
def add():
    form = AddForm()
    if request.method == 'POST':
        movie_title = form.title.data
        response = requests.get(URL, params={"query": movie_title}, headers=HEADERS)
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template('add.html', form=form)

@app.route('/select')
def select_movie():
    # Getting the 'id' from the query params
    movie_api_id = request.args.get("id")
    print(movie_api_id)
    if movie_api_id:
        movie_api_url = f"{URL_FIND}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"language": "en-US"}, headers=HEADERS)
        data = response.json()
        new_movie = Movie(
            title=data["original_title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{URL_IMAGE}{data['poster_path']}",
            description=data["overview"],
            rating=0.0,
            ranking = 0,
            review = " "
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("update", id = new_movie.id))
    return "Movie not found"

@app.route("/update", methods=["GET", "POST"])
def update():
    form = EditForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route(f"/delete/<int:movie_id>")
def delete(movie_id):
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar_one_or_none()
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
