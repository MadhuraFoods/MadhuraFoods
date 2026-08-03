from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect("madhurafoods.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        father_name TEXT,
        mother_name TEXT,
        dob TEXT,

        door_no TEXT,
        house_name TEXT,
        street TEXT,
        landmark TEXT,
        city TEXT,
        state TEXT,
        pincode TEXT,

        phone TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup', methods=['POST'])
def signup():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    father_name = request.form['father_name']
    mother_name = request.form['mother_name']
    dob = request.form['dob']

    door_no = request.form['door_no']
    house_name = request.form['house_name']
    street = request.form['street']
    landmark = request.form['landmark']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']

    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect("madhurafoods.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (
        first_name,last_name,father_name,mother_name,dob,
        door_no,house_name,street,landmark,city,state,pincode,
        phone,email,password
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        first_name,last_name,father_name,mother_name,dob,
        door_no,house_name,street,landmark,city,state,pincode,
        phone,email,password
    ))

    conn.commit()
    conn.close()

    return redirect('/signin')


@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect("madhurafoods.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return f"Welcome {user[1]} 🎉"

    return "Invalid Email or Password"


if __name__ == '__main__':
    app.run(debug=True)