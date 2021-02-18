import os
from flask import Flask, render_template

working_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(working_dir, 'templates')
static_dir = os.path.join(working_dir, 'static')
app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

@app.route('/' , methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/signin' , methods=['POST','GET'])
def signup():
    return render_template('index.html')

@app.route('/signup' , methods=['POST','GET'])
def signin():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
