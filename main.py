from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog-a-build@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/blog", methods = ['POST','GET'])
def blog():


    return render_template('blog.html')

@app.route("/newpost", methods=['POST','GET'])
def new_blog():
   
    if request.method == 'POST':
        return "<h1>sdfsf</h1>"
        title= request.form['title']
        body = request.form['body']
        new_blog = Blog(title,body)
        db.session.add(new_blog)
        db.session.commit()
        new_title = Blog.query.filter_by(title=title).first()
        blog_id= new_title.id
        
        return redirect('/display?id={}'.format(blog_id))
    
    
    return render_template("newpost.html")
    
@app.route("/display", methods=['POST','GET'])
def display():
    
    blog_id=request.args.get("id")
    blogs = Blog.query.all()
    if blog_id:

        blog=Blog.query.get(blog_id)
        return render_template("display.html",blog=blog)
    else:
        return render_template("blog.html",blogs=blogs)
    
    
    
    



@app.route("/", methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html',blogs=blogs)



if __name__ == '__main__':
    app.run()