from flask import Flask, render_template, url_for, request, redirect, session
import datetime
from detect import Detect, validate_image
from database import Users

users = Users()
app = Flask(__name__)
app.secret_key = "serakfbeerkbeer"

# get year for copyright
today = datetime.date.today()
year = today.strftime("%Y")

detect = Detect()


@app.route('/')
def home():
    if 'username' in session:
        history = users.get_history(session['username'])
        name = session['username']
        return render_template('index.html', year=year, auth=True, history=history, name=name)
    return render_template('index.html', year=year, auth=False)


@app.route('/read')
def read():
    if 'username' in session:
        history = users.get_history(session['username'])
        name = session['username']
        return render_template('read.html', year=year, auth=True, history=history, name=name)
    return render_template('read.html', year=year, auth=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if users.login_user(username, password):
            session['username'] = username
            print(f"Logged in as: {session['username']}")
            return redirect(url_for('home'))

        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if users.register_user(username, email, password):
            session['username'] = username
            print(f"Logged in as: {session['username']}")
            return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':

        image = request.files['img']
        if validate_image(image):
            return redirect(url_for('home'))

        image_path = f'static/images/{image.filename}'
        image.save(image_path)

        if 'username' in session:
            users.save_image(image_path, session['username'])

        data = detect.detect(image_path)
        history = users.get_history(session['username'])
        print(history)
        if 'username' in session:
            name = session['username']
            print(name)
            return render_template('result.html', img="static/outputs/result.png", data=data, year=year,
                                   history=history, auth=True, name=name)
        return render_template('result.html', img="static/outputs/result.png", data=data, year=year)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
