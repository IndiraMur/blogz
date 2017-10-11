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
        
        title= request.form['title']
        body = request.form['body']
        new_blog = Blog(title,body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/')
        
        
    
    return render_template('/newpost.html')

@app.route("/display", methods=['GET'])
def display():
#    form_value = request.args.get("blog.title")
   
    
    
    return render_template("display.html")
    



@app.route("/", methods=['POST', 'GET'])
def index():
    titles = Blog.query.all()
    return render_template('blog.html',titles=titles)



if __name__ == '__main__':
    app.run()