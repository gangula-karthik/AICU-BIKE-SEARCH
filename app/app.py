from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)


# base template testing
@app.route('/test')
def index():
    return render_template('index.html')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/qr_code')
def qr_code():
    return render_template('qr_code.html')


@app.route('/approving_login')
def approving_login():
    return render_template('approving_login.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
