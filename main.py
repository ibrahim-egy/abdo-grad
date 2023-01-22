from flask import Flask, render_template, url_for, request, redirect, flash
import datetime
from PIL import Image
from detect import Detect, validate_image

# detect = Detect()

app = Flask(__name__)
app.secret_key = "serakfbeerkbeer"

# get year for copyright
today = datetime.date.today()
year = today.strftime("%Y")



from pymongo import MongoClient

mongo_atlas_url = "mongodb+srv://ibrahim:ibrahim123@cluster0.n66dv.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_atlas_url)

db = client.get_database('abdoDB')
users = db.get_collection('users')





@app.route('/')
def home():
    return render_template('index.html', year=year)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        user_found = users.find_one({'name': username})

        print(f"Username: {username}\nPassword: {password}")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Username: {username}\nEmail: {email}\nPassword: {password}")
    return render_template('register.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':

        image = request.files['img']
        if validate_image(image):
            return redirect(url_for('home'))

        image_path = f'static/images/{image.filename}'
        image.save(image_path)
        data = detect.detect(image_path)

        return render_template('result.html', img="static/outputs/result.png", data=data, year=year)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
