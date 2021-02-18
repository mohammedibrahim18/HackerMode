import os
from flask import Flask, render_template
from rich.traceback import pretty
pretty.install()

working_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(working_dir, 'templates')
static_dir = os.path.join(working_dir, 'static')
app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)
# https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxCEvFAEe3ziBvRL7ID-IijbniFupiKJS_nA&usqp=CAU
@app.route('/' , methods=['POST','GET'])
def index_page():
    return render_template('index.html')

@app.route('/login' , methods=['POST','GET'])
def login_page():
    return render_template('login.html')

@app.route('/signup' , methods=['POST','GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/about' , methods=['POST','GET'])
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(
        debug=True,
    )
