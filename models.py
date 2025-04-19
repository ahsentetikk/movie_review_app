from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    country = db.Column(db.String(50))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    year = db.Column(db.Integer)
    certificate = db.Column(db.String(20))
    runtime = db.Column(db.String(50))
    genre = db.Column(db.String(100))
    imdb_rating = db.Column(db.Float)
    overview = db.Column(db.Text)
    meta_score = db.Column(db.Integer)
    director = db.Column(db.String(100))
    star1 = db.Column(db.String(100))
    star2 = db.Column(db.String(100))
    star3 = db.Column(db.String(100))
    star4 = db.Column(db.String(100))
    no_of_votes = db.Column(db.Integer)
    gross = db.Column(db.String(50))
    image_url = db.Column(db.String(300))  

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='reviews')
    movie = db.relationship('Movie', backref='reviews')

    # Cevaplar (kendiyle ilişkili yorumlar)
    replies = db.relationship(
        'Review',
        backref=db.backref('parent', remote_side=[id]),
        cascade='all, delete-orphan'
    )

    # ❌ BURAYA review ya da likes adında başka relationship eklenmeyecek!

class ReviewLike(db.Model):
    __tablename__ = 'review_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', backref='review_likes')

    # ✅ Burada Review.likes tanımını sağlıyoruz
    review = db.relationship('Review', backref=db.backref('likes', cascade='all, delete-orphan'))
