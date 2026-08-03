from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "madhurafoods_secret_key"


# =========================
# DATABASE SETUP
# =========================

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
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    action TEXT,
    date_time TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# REGISTER PAGE
# =========================

@app.route("/register")
def register():
    return render_template("register.html")


# =========================
# SIGN IN PAGE
# =========================

@app.route("/signin")
def signin():
    return render_template("signin.html")


# =========================
# SIGN UP
# =========================

@app.route("/signup", methods=["POST"])
def signup():

    conn = sqlite3.connect("madhurafoods.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users (
            first_name,last_name,
            father_name,mother_name,
            dob,
            door_no,house_name,street,landmark,
            city,state,pincode,
            phone,email,password
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (

            request.form["first_name"],
            request.form["last_name"],

            request.form["father_name"],
            request.form["mother_name"],

            request.form["dob"],

            request.form["door_no"],
            request.form["house_name"],
            request.form["street"],
            request.form["landmark"],

            request.form["city"],
            request.form["state"],
            request.form["pincode"],

            request.form["phone"],

            request.form["email"],
            request.form["password"]

        ))

        conn.commit()

        cursor.execute("""
        INSERT INTO activity_logs
        (name,email,action,date_time)
        VALUES (?,?,?,?)
        """,
        (
            request.form["first_name"],
            request.form["email"],
            "Registered Account",
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()
        return "Email already registered!"

    conn.close()

    return redirect("/signin")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("madhurafoods.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        log_conn = sqlite3.connect("madhurafoods.db")
        log_cursor = log_conn.cursor()

        log_cursor.execute("""
        INSERT INTO activity_logs
        (name,email,action,date_time)
        VALUES (?,?,?,?)
        """,
        (
            user[1],
            user[14],
            "Logged In",
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))

        log_conn.commit()
        log_conn.close()

        session["user_email"] = user[14]

        return redirect("/profile")

    return """
    <h1>Login Failed ❌</h1>
    <p>Invalid Email or Password</p>
    <a href="/signin">Try Again</a>
    """


# =========================
# PROFILE PAGE
# =========================

@app.route("/profile")
def profile():

    if "user_email" not in session:
        return redirect("/signin")

    conn = sqlite3.connect("madhurafoods.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (session["user_email"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        username=user[1],
        user=user
    )


# =========================
# EDIT PROFILE
# =========================

@app.route("/edit-profile")
def edit_profile():

    if "user_email" not in session:
        return redirect("/signin")

    return render_template("edit_profile.html")


# =========================
# MENU
# =========================

@app.route("/menu")
def menu():

    if "user_email" not in session:
        return redirect("/signin")

    return render_template("menu.html")


# =========================
# ORDERS
# =========================

@app.route("/orders")
def orders():

    if "user_email" not in session:
        return redirect("/signin")

    return render_template("orders.html")


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# CONTACT
# =========================

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/send-message", methods=["POST"])
def send_message():

    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = sqlite3.connect("madhurafoods.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO messages (name, email, message)
    VALUES (?, ?, ?)
    """, (name, email, message))

    conn.commit()
    conn.close()

    return render_template("message_sent.html")
# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    if "user_email" in session:

        conn = sqlite3.connect("madhurafoods.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (session["user_email"],)
        )

        user = cursor.fetchone()

        if user:

            cursor.execute("""
            INSERT INTO activity_logs
            (name,email,action,date_time)
            VALUES (?,?,?,?)
            """,
            (
                user[1],
                user[14],
                "Logged Out",
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            ))

        conn.commit()
        conn.close()

    session.clear()

    return redirect("/")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)