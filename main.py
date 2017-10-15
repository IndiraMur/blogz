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
    error_title =""
    error_body=""
   
    if request.method == 'POST':
        title= request.form['title']
        body = request.form['body']
        addedBlog = Blog(title,body)
        
        
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