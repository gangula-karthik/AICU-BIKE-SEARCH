from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


# base template testing
@app.route('/test')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
