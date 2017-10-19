from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
 
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(120), unique=True)
     password = db.Column(db.String(120))
     blogs = db.relationship('Blog', backref='owner')
 
     def __init__(self, username, password):
       
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','display','newpost','blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route("/blog", methods=['POST', 'GET'])
def blog():

    blogs = Blog.query.all()
    return render_template('allpost.html',blogs=blogs)

@app.route("/newpost", methods=['POST','GET'])
def new_blog():
    error_title =""
    error_body=""
    
    owner = User.query.filter_by(username=session['username']).first()
    

    if request.method == 'POST':
        title= request.form['title']
        body = request.form['body']
        addedBlog = Blog(title,body,owner)
        
        
        if title == "":
            error_title ="Please fill in the title"
        if body == "":
                error_body = "Please fill in the content"
        if not error_title and not error_body:
            db.session.add(addedBlog)
            db.session.commit()
            new_title = Blog.query.filter_by(title=title).first()
            blog_id= new_title.id
            
            return redirect('/display?id={0}'.format(blog_id))
        
    

    return render_template("newpost.html",error_title=error_title,error_body=error_body)

    
    
@app.route("/display", methods=['POST','GET'])
def display():
    add_columns = []
    blogs1 = Blog.query.join(User).add_columns(Blog.id,Blog.title,Blog.body,User.username).filter(Blog.owner_id==User.id).all()    
    blogs = Blog.query.all()

    blog_user = request.args.get('user')
    if blog_user :
        blog_user_id = User.query.filter_by(username=blog_user).first().id
#   User Blogs    
        blogs2 = Blog.query.join(User).add_columns(Blog.id,Blog.title,Blog.body,User.username).filter(Blog.owner_id==blog_user_id).all()
        return render_template('singleUser.html',blogs2=blogs2,blog_user = blog_user)

    blog_id=request.args.get("id")
    blogs = Blog.query.all()
    if blog_id:

        blog=Blog.query.get(blog_id)
        return render_template("display.html",blog=blog)
    else:
        
        return render_template("allpost.html",blogs1=blogs1)

    
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if verify!=password:
            flash("password is not matching")
        else:

        # TODO - validate user's data

            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                # TODO - "remember" the user
                return redirect('/newpost')
            else:
                # TODO - user better response messaging
                flash("username already exist",'error')

    

    
    return render_template("signup.html")

    #@app.route("/index")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("logged in")
            # TODO - "remember" that the user has logged in
            return redirect('/newpost')
        else:
            flash("password incorrect or username does not exist",'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
   




@app.route("/", methods=['POST', 'GET'])
def index():
    user = request.args.get('username')
    if request.method == 'GET' :

        users = User.query.all()
    return render_template('index.html',users=users)



if __name__ == '__main__':
    app.run()