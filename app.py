import os
import requests
import json
import psycopg2
from flask import Flask, render_template, request, flash, redirect, session, jsonify, g, abort
from mypackage.models import Category, connect_db, db, Article, User, Favorite, CategoryArticle, Source
from mypackage.forms import RegisterForm, LoginForm, DeleteForm
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
from mypackage.apidata import SUPER_SECRET_KEY
API_SECRET_KEY = SUPER_SECRET_KEY
API_BASE_URL = "https://newsapi.org/v2"

CURR_USER_KEY = "username"

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('data_url', 'postgresql:///capstone_database')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.filter_by(username=session[CURR_USER_KEY]).first()

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

##############################################################################################################
# API ROUTE BELOW HERE
####### Route For Query Parameters ############

# search news by title, description or content 
# Multiple options can be specified by separating them with a comma, for example: title,content.
@app.route('/api/get_articles/<qvalue>')
def search_data(qvalue):
    response = requests.get("https://newsapi.org/v2/everything", 
    params={'q':qvalue, 'apiKey':API_SECRET_KEY})
    res = response.json()
    return res

@app.route('/api/cat_articles/<categoryvalue>')
def search_category(categoryvalue):
    response = requests.get("https://newsapi.org/v2/top-headlines/sources", 
    params={'category':categoryvalue, 'apiKey':API_SECRET_KEY})
    res = response.json()
    return res

@app.route('/api/get_articles/<qvalue>/<sortvalue>')
def sort_data(qvalue, sortvalue):
    response = requests.get("https://newsapi.org/v2/everything", 
    params={'q':qvalue, 'sortBy':sortvalue, 'apiKey':API_SECRET_KEY})
    res = response.json()
    return res

### search news by date. (from -to)date are required in the format of (YYYY-MM-DD)
@app.route('/api/get_articles/<qvalue>/<fromdate>/<todate>')
def date_Article(qvalue,fromdate,todate ):
    response = requests.get("https://newsapi.org/v2/everything", 
    params={'q':qvalue, 'from':fromdate, 'to':todate, 'apiKey':API_SECRET_KEY})
    res = response.json()
    return res

################### route for user #############
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """Returns JSON w/ a user"""
    user= User.query.get_or_404(user_id)
    return jsonify(user=user.user_serialize())



@app.route('/api/users', methods=["POST"])
def create_user():
    """Creates a new user and returns JSON of that created user"""
    data = request.json
    new_user = User.register(email=data["email"], 
                       username=data["username"],
                       password=data["password"],
                       image=data["image_url"]
    )
    db.session.add(new_user)
    db.session.commit()
    response_json = jsonify(user=new_user.user_serialize())
    return (response_json, 201)


@app.route('/api/users/<int:user_id>', methods=["PATCH"])
def update_user(user_id):
    """Updates a particular user and responds w/ JSON of that updated user"""
    user = User.query.get_or_404(user_id)
    user.email = request.json.get('email', user.email)
    user.username = request.json.get('username',  user.username)
    user.password = request.json.get('password',  user.password)
    user.image_url = request.json.get('image_url',  user.image_url)
    db.session.commit()
    return jsonify(user=user.user_serialize())

@app.route('/api/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    """Deletes a particular user"""
    user = Article.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="Deleted")

###################### ('/api/users/<int:user_id>/categories')####################
@app.route('/api/categories')
def list_categories():
    """Returns JSON w/ all categories"""
    category = [category.category_serialize() for category in Category.query.all()]
    return jsonify(categories=category)

@app.route('/api/categories/<int:cate_id>')
def get_category(cate_id):
    """Returns JSON for one category in particular"""
    category = Category.query.get_or_404(cate_id)
    return jsonify(category=category.category_serialize()) 

@app.route('/api/categories', methods=["POST"])
def create_category():
    """Creates a new category and returns JSON of that created category"""
    data = request.json
    new_category = Category(name=data["name"])

    db.session.add(new_category)
    db.session.commit()
    response_json = jsonify(category=new_category.category_serialize())
    return (response_json, 201)

@app.route('/api/categories/<int:category_id>', methods=["PATCH"])
def update_category(category_id):
    """Updates a particular category and responds w/ JSON of that updated category"""
    category = Category.query.get_or_404(category_id)
    category.name = request.json.get('name', category.name)
    db.session.commit()
    return jsonify(category=category.serialize())


@app.route('/api/categories/<int:category_id>', methods=["DELETE"])
def delete_category(category_id):
    """Deletes a particular category"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(message="Deleted")

#################################################################################################
#######getting an artcile###########
@app.route('/api/articles/<int:article_id>')
def get_article(article_id):
    """Returns JSON for one article in particular"""
    article = Article.query.get_or_404(article_id)
    return jsonify(article=article.article_serialize())

############getting articles for a specific category############
@app.route('/api/categories/<int:cate_id>/articles')
def list_articles(cate_id):
    """Returns JSON w/ all articles"""
    category = Category.query.get(cate_id)
    article_for_category = category.category_article
    all_articles = [article.article_serialize() for article in article_for_category]
    return jsonify(articles=all_articles)



@app.route('/api/categories/articles', methods=["POST"])
def create_article():
    """Creates a new article and returns JSON of that created article"""
    data = request.json
    article = Article.query.filter_by(title=data["title"]).first()
    if article != None:
        print("alreday in the database")
        response_json = "hello"
    else:
        new_article = Article(author=data["author"], 
                           title=data["title"],
                           description=data["description"],
                           url=data["url"], 
                           Image_URL=data["Image_URL"],                    
                           published_date=data["published_date"]
                           )
        db.session.add(new_article)
        db.session.commit()
        domainvalue = data["url"].split("/")[2]
        res = requests.get(f"{API_BASE_URL}/top-headlines/sources",
                            params={'apiKey':API_SECRET_KEY})
        results = res.json()    
        def name_list1():
            return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="general" if x['language']=='en' ]
        def name_list2(): 
            return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="business" if x['language']=='en']
        def name_list3(): 
            return[x['url'].split("/")[2] for x in results['sources'] if x['category']=="technology" if x['language']=='en']
        def name_list4(): 
            return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="entertainment" if x['language']=='en']
        def name_list5(): 
            return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="science" if x['language']=='en']
        def name_list6(): 
            return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="sports" if x['language']=='en']
        def name_list7(): 
            return[x['url'].split("/")[2]  for x in results['sources'] if x['category']=="health" if x['language']=='en']
        g= [*set(name_list1())]
        b= [*set(name_list2())]
        t= [*set(name_list3())]
        e= [*set(name_list4())]
        s= [*set(name_list5())]
        sp= [*set(name_list6())]    
        h = [*set(name_list7())]

        article = Article.query.filter_by(title=data["title"]).first()
        if domainvalue in g:
            category = Category.query.filter_by(name="general").first()              
            new_cat_article = CategoryArticle(category_id=category.id, article_id=article.id)
            db.session.add(new_cat_article)
            db.session.commit() 

        if domainvalue in b:
            category = Category.query.filter_by(name="business").first()
            new_cat_article = CategoryArticle(category_id=category.id, article_id=article.id)
            db.session.add(new_cat_article)
            db.session.commit() 

        if domainvalue in t:
            category = Category.query.filter_by(name="technology").first()
            new_cat_article = CategoryArticle(category_id=category.id, article_id=article.id)
            db.session.add(new_cat_article)
            db.session.commit() 

        if domainvalue in e:
            category = Category.query.filter_by(name="entertainment").first()
            new_cat_article = CategoryArticle(category_id=category.id, article_id=article.id)
            db.session.add(new_cat_article)
            db.session.commit() 

        if domainvalue in s:
            category = Category.query.filter_by(name="science").first()
            new_cat_article = CategoryArticle(category_id=category.id, article_id=article.id)
            db.session.add(new_cat_article)
            db.session.commit() 
    
        if domainvalue in sp:
            category = Category.query.filter_by(name="sports").first()
            new_cat_article = CategoryArticle(category_id=category.id, article_id=article.id)
            db.session.add(new_cat_article)
            db.session.commit() 

        if domainvalue in h:
            category = Category.query.filter_by(name="health").first()
            new_cat_article = CategoryArticle(category_id=category.id, article_id=article.id)
            db.session.add(new_cat_article)
            db.session.commit() 


        response_json = jsonify(article = new_article.article_serialize())
    return (response_json, 201)

def create_category_article(cat,art):
    new_cat_article = CategoryArticle(category_id=cat.id, article_id=art.id)
    db.session.add(new_cat_article)
    db.session.commit() 


@app.route('/api/categories/<int:cate_id>/articles/<int:article_id>', methods=["PATCH"])
def update_article(article_id):
    """Updates a particular article and responds w/ JSON of that updated article"""
    article = Article.query.get_or_404(article_id)
    article.author = request.json.get('author', article.author)
    article.title = request.json.get('title',  article.title)
    article.description = request.json.get('description',  article.description)
    article.url = request.json.get('url',  article.url)
    article.published_date = request.json.get('published_date',  article.published_date)
    article.content = request.json.get('content',  article.content)
    db.session.commit()
    return jsonify(articles=article.serialize())


@app.route('/api/categories/articles/<int:article_id>', methods=["DELETE"])
def delete_article(article_id):
    """Deletes a particular article"""
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify(message="Deleted")



#################################################################################################

# FLASK APP ROUTE BELOW HERE


@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    category = Category.query.all()
    article = Article.query.limit(41).all()
    source = Source.query.limit(33).all()
    c=Category.query.filter_by(name="general").first()
    catart = c.category_article
    return render_template('homepage.html', article=article, category=category, source=source, catart=catart)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect("/articles")

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            email = form.email.data
            username = form.username.data
            image_url = form.image_url.data
            password = form.password.data  
            user = User.register(email, username, password, image_url)
            db.session.commit()
            session['username'] = user.username

        except IntegrityError as e:
            flash("Username already taken.", 'danger')            
            return render_template("user/register.html", form=form)

        flash("Signup successful.", 'success') 
        return redirect("/login")


    else:
        return render_template("user/register.html", form=form) 



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect("article")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            flash(f"Hello, {user.username}!", "success")
             return redirect("article")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("user/login.html", form=form)

    return render_template("user/login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""
    do_logout()
    flash("You have successfully logged out.", 'success')
    return redirect("/login")



@app.route('/articles')
def show_article():
    if "username" not in session:
        raise Unauthorized()
    username = session['username']
    article = Article.query.all()
    user = User.query.filter_by(username=username).first()
    favart = Favorite.query.filter_by(user_id=user.id)
    found_article = [a.favoriteArticle_id for a in favart]
    category = Category.query.all()
    return render_template('article/show.html', 
                            article=article, category=category, found_article=found_article)


@app.route('/categories')
def show_categories():
    if "username" not in session:
        raise Unauthorized()
    category = Category.query.all()
    article = Article.query.all()
    return render_template('category/show.html', category=category, article=article)

@app.route('/sources')
def show_sources():
    if "username" not in session:
        raise Unauthorized()
    category = Category.query.all()
    source_data = Source.query.all()
    source = db.session.query(Source.category).distinct().all()
    return render_template('category/source.html', category=category, 
            sources=source, source_data=source_data)


@app.route('/categories/<cat_name>/articles')
def show_category(cat_name):
    if "username" not in session:
        raise Unauthorized()
    username = session['username']
    category=Category.query.all()
    c=Category.query.filter_by(name=cat_name).first()
    catart = c.category_article
    user = User.query.filter_by(username=username).first()
    favart = Favorite.query.filter_by(user_id=user.id)
    found_article = [a.favoriteArticle_id for a in favart]
    return render_template('category/article.html', 
                            allarticle=catart, cat=cat_name, category=category, found_article=found_article)


@app.route('/users/favorites/<username>')
def favorite_page(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    category=Category.query.all()
    user = User.query.filter_by(username=username).first()
    article = user.user_article
    return render_template("/user/favorites.html", 
                         user=user, category=category, article=article)

@app.route('/favorites/articles/<int:id>')
def add_favorite(id):
    """Creates a new article and returns JSON of that created article"""
    if "username" not in session:
        raise Unauthorized()
    username = session['username']
    user = User.query.filter_by(username=username).first()    
    favart =  user.user_article 
    found_article = [a.id for a in favart]
    article = Favorite.query.filter_by(favoriteArticle_id=id).filter_by(user_id=user.id).first()
    if id in found_article:
        db.session.delete(article)
        db.session.commit()    
    else:
        new_fav = Favorite(user_id=user.id, 
                       favoriteArticle_id=id
                       )
        db.session.add(new_fav)
        db.session.commit()

    return redirect (f"/users/favorites/{username}")


@app.route('/search')
def search_page():
    return render_template("/searchform.html")
    
@app.route('/sortdata')
def sort_page():
    qvalue = request.form['q']
    return render_template("/filterpage.html", qvalue=qvalue)


@app.route('/demo')
def demo_page():
    return render_template('/demo.html')



@app.route('/filter')
def filter_date():
    return render_template("/filterpage.html")
    
