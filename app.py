from flask import Flask, abort, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Movie, Review, ReviewLike

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ——— ÖRNEK FİLM EKLEME ———
@app.route('/add-sample-movies')
def add_sample_movies():
    sample_movies = [
        Movie(
            title="Inception",
            year=2010,
            certificate="PG-13",
            runtime="148 min",
            genre="Action, Adventure, Sci-Fi",
            imdb_rating=8.8,
            overview="A thief who steals corporate secrets through use of dream-sharing technology.",
            meta_score=74,
            director="Christopher Nolan",
            star1="Leonardo DiCaprio",
            star2="Joseph Gordon-Levitt",
            star3="Elliot Page",
            star4="Tom Hardy",
            no_of_votes=2000000,
            gross="$829.89M",
            image_url="images/1.jpg"
        ),
        Movie(
            title="The Matrix",
            year=1999,
            certificate="R",
            runtime="136 min",
            genre="Action, Sci-Fi",
            imdb_rating=8.7,
            overview="A computer hacker learns about the true nature of his reality.",
            meta_score=73,
            director="The Wachowskis",
            star1="Keanu Reeves",
            star2="Laurence Fishburne",
            star3="Carrie-Anne Moss",
            star4="Hugo Weaving",
            no_of_votes=1800000,
            gross="$463.52M",
            image_url="images/2.jpg"
        ),
        Movie(
            title="The Shawshank Redemption",
            year=1994,
            certificate="R",
            runtime="142 min",
            genre="Drama",
            imdb_rating=9.3,
            overview="Two imprisoned men bond over a number of years.",
            meta_score=80,
            director="Frank Darabont",
            star1="Tim Robbins",
            star2="Morgan Freeman",
            star3="Bob Gunton",
            star4="William Sadler",
            no_of_votes=2500000,
            gross="$28.34M",
            image_url="images/3.jpg"
        ),
        Movie(
            title="The Godfather",
            year=1972,
            certificate="R",
            runtime="175 min",
            genre="Crime, Drama",
            imdb_rating=9.2,
            overview="The aging patriarch of an organized crime dynasty transfers control to his son.",
            meta_score=100,
            director="Francis Ford Coppola",
            star1="Marlon Brando",
            star2="Al Pacino",
            star3="James Caan",
            star4="Robert Duvall",
            no_of_votes=1700000,
            gross="$134.97M",
            image_url="images/4.jpg"
        ),
        Movie(
            title="The Dark Knight",
            year=2008,
            certificate="PG-13",
            runtime="152 min",
            genre="Action, Crime, Drama",
            imdb_rating=9.0,
            overview="Batman battles the Joker in Gotham City.",
            meta_score=84,
            director="Christopher Nolan",
            star1="Christian Bale",
            star2="Heath Ledger",
            star3="Aaron Eckhart",
            star4="Michael Caine",
            no_of_votes=2300000,
            gross="$534.86M",
            image_url="images/5.jpg"
        ),
        Movie(
            title="Pulp Fiction",
            year=1994,
            certificate="R",
            runtime="154 min",
            genre="Crime, Drama",
            imdb_rating=8.9,
            overview="The lives of two mob hitmen intertwine in a series of tales.",
            meta_score=94,
            director="Quentin Tarantino",
            star1="John Travolta",
            star2="Uma Thurman",
            star3="Samuel L. Jackson",
            star4="Bruce Willis",
            no_of_votes=1900000,
            gross="$213.92M",
            image_url="images/6.jpg"
        ),
        Movie(
            title="Fight Club",
            year=1999,
            certificate="R",
            runtime="139 min",
            genre="Drama",
            imdb_rating=8.8,
            overview="An insomniac office worker forms an underground fight club.",
            meta_score=66,
            director="David Fincher",
            star1="Brad Pitt",
            star2="Edward Norton",
            star3="Helena Bonham Carter",
            star4="Meat Loaf",
            no_of_votes=1800000,
            gross="$100.85M",
            image_url="images/7.jpg"
        ),
        Movie(
            title="Forrest Gump",
            year=1994,
            certificate="PG-13",
            runtime="142 min",
            genre="Drama, Romance",
            imdb_rating=8.8,
            overview="Forrest Gump's life story from childhood to adulthood.",
            meta_score=82,
            director="Robert Zemeckis",
            star1="Tom Hanks",
            star2="Robin Wright",
            star3="Gary Sinise",
            star4="Sally Field",
            no_of_votes=1900000,
            gross="$330.25M",
            image_url="images/8.jpg"
        ),
        Movie(
            title="Interstellar",
            year=2014,
            certificate="PG-13",
            runtime="169 min",
            genre="Adventure, Drama, Sci-Fi",
            imdb_rating=8.6,
            overview="A team travels through a wormhole to find a new home for humanity.",
            meta_score=74,
            director="Christopher Nolan",
            star1="Matthew McConaughey",
            star2="Anne Hathaway",
            star3="Jessica Chastain",
            star4="Michael Caine",
            no_of_votes=1700000,
            gross="$677.47M",
            image_url="images/9.jpg"
        ),
        Movie(
            title="Gladiator",
            year=2000,
            certificate="R",
            runtime="155 min",
            genre="Action, Adventure, Drama",
            imdb_rating=8.5,
            overview="A former Roman General seeks revenge after being betrayed.",
            meta_score=67,
            director="Ridley Scott",
            star1="Russell Crowe",
            star2="Joaquin Phoenix",
            star3="Connie Nielsen",
            star4="Oliver Reed",
            no_of_votes=1400000,
            gross="$460.50M",
            image_url="images/10.jpg"
        ),
    ]

    db.session.add_all(sample_movies)
    db.session.commit()
    return "10 sample movies added!"


# ——— KAYIT ———
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            username   = request.form['username'],
            email      = request.form['email'],
            password   = bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
            full_name  = request.form['full_name'],
            birth_year = request.form['birth_year'],
            gender     = request.form['gender'],
            country    = request.form['country']
        )
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect(url_for('login'))
    return render_template("register.html")


# ——— GİRİŞ ———
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        flash('Kullanıcı adı veya şifre hatalı.')
    return render_template("login.html")


# ——— ÇIKIŞ ———
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ——— ANA SAYFA (Film Listesi) ———
@app.route('/')
def home():
    query = request.args.get('query', '')  # URL'den ?query=... parametresi alınıyor
    if query:
        movies = Movie.query.filter(Movie.title.ilike(f"%{query}%")).all()
    else:
        movies = Movie.query.all()
    return render_template("home.html", movies=movies)



# ——— FİLM DETAY & YORUMLAR/REPLY ———
@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        parent_id = request.form.get('parent_id') or None
        comment   = request.form['comment']

        # Eğer parent_id varsa bu bir REPLY, rating formda yok
        if parent_id:
            # Reply’ler için biz rating=0 atıyoruz (model nullable değilse)
            review = Review(
                user_id   = current_user.id,
                movie_id  = movie.id,
                rating    = 0,
                comment   = comment,
                parent_id = parent_id
            )
        else:
            # Normal yeni yorum
            rating = int(request.form['rating'])
            review = Review(
                user_id   = current_user.id,
                movie_id  = movie.id,
                rating    = rating,
                comment   = comment,
                parent_id = None
            )

        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie_detail', movie_id=movie.id))

    # Sadece ana yorumları getir
    reviews = Review.query.filter_by(movie_id=movie.id, parent_id=None).all()
    return render_template("movie_detail.html", movie=movie, reviews=reviews)


# ——— LIKE / DISLIKE ———
@app.route('/review/<int:review_id>/react', methods=['POST'])
@login_required
def react_review(review_id):
    review = Review.query.get_or_404(review_id)
    is_like = request.form.get('is_like') == '1'
    existing = ReviewLike.query.filter_by(
        user_id=current_user.id,
        review_id=review_id
    ).first()

    if existing:
        if existing.is_like == is_like:
            db.session.delete(existing)
        else:
            existing.is_like = is_like
    else:
        like = ReviewLike(
            user_id   = current_user.id,
            review_id = review_id,
            is_like   = is_like
        )
        db.session.add(like)

    db.session.commit()
    return redirect(url_for('movie_detail', movie_id=review.movie_id))


# ——— YORUM GÜNCELLE ———
@app.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        review.rating  = int(request.form['rating'])
        review.comment = request.form['comment']
        db.session.commit()
        flash("Yorumunuz güncellendi.")
        return redirect(url_for('movie_detail', movie_id=review.movie_id))

    return render_template("edit_review.html", review=review)


# ——— YORUM SİL ———
@app.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        abort(403)

    # önce bağlı reply ve like kayıtlarının silinmesi için cascade ayarlanmışsa doğrudan:
    db.session.delete(review)
    db.session.commit()
    flash("Yorumunuz silindi.")
    return redirect(url_for('movie_detail', movie_id=review.movie_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
