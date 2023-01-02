"""SQLAlchemy models for Capstone."""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)



class Favorite(db.Model):
    """user can save article as favourite"""

    __tablename__ = 'favorites'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    favoriteArticle_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")


    def user_serialize(self):
        return{
            'id':self.id,
            'email':self.email,
            'username':self.username,
            'password': self.password,
            'image_url':self.image_url
        }

    @classmethod
    def register(cls, email,  username, password, image):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            email=email,
            username=username,
            password=hashed_utf8,
            image_url=image            
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False        

    user_article = db.relationship("Article",  secondary='favorites', backref="users")
    



class Category(db.Model):
    """Categories"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

   
    def category_serialize(self):
        return{
            'id':self.id,
            'name':self.name
        }
    category_article = db.relationship('Article', secondary="categories_articles", 
                        backref='categories', cascade='all, delete')


class Article(db.Model):
    """Article"""
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    url = db.Column(db.Text)
    Image_URL =db.Column(db.Text)
    published_date = db.Column(db.DateTime, nullable=False)

    def article_serialize(self):
        return{
            'author':self.author,
            'title':self.title,
            'description': self.description,
            'url':self.url,
            'Image_URL':self.Image_URL,
            'published_date':self.published_date
        }



class CategoryArticle(db.Model):
    """unique row for category and article"""

    __tablename__ = 'categories_articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)

    def category_article_serialize(self):
        return{
            'category_id':self.category_id,
            'article_id':self.article_id
        }



class Source(db.Model):
    
    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    url = db.Column(db.Text)
    category = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)



