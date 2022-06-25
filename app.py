from curses.ascii import FF
import os
from tracemalloc import start
from attr import fields

from cs50 import SQL
from flask import Flask, flash, redirect, url_for, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from help import Error, login_required
from datetime import datetime

# Configure application
app = Flask(__name__)

app.config['SECRET_KEY'] = '#$%^&*'



# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///clinic.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show today's appointments"""
    today = datetime.today().strftime('%Y-%m-%d')
    work = db.execute("select * from appointments where day = ? and user= ?", today, session["user_name"])
    if len(work) == 0:
        return render_template('appointments.html')
    return render_template('appointments.html', work = work)



@app.route("/finance", methods=["GET", "POST"])
@login_required
def indexes():
    # showing all procedures and the total income of a specific time range
    history = db.execute("SELECT * FROM procedures WHERE user = ? ", session["user_name"])
    total = db.execute("select sum(price) from procedures where user = ?", session["user_name"])
    return render_template("finance.html", history=history, total = total)


@app.route("/finance_m", methods=["GET", "POST"])
@login_required
def finance_m():
    """Show clinic's logs this month"""
    dateM = datetime.today().strftime("%Y-%m")
    history = db.execute("select patient, procedure, date, price from procedures where date like ? and user = ?", f"{dateM}%", session["user_name"])
    total = db.execute("select sum(price) from procedures where user = ? and date like ? ", session["user_name"], f"{dateM}%")
    return render_template("finance.html", history=history, total = total)

@app.route("/finance_y", methods=["GET", "POST"])
@login_required
def finance_y():
    """Show clinic's logs this year"""
    dateM = datetime.today().strftime("%Y")
    history = db.execute("select patient, procedure, date, price from procedures where date like ? and user = ?",  f"{dateM}%", session["user_name"])
    total = db.execute("select sum(price) from procedures where user = ? and date like ? ", session["user_name"], f"{dateM}%")
    return render_template("finance.html", history=history, total = total)

@app.route("/finance_special", methods=["GET", "POST"])
@login_required
def finance_special():
    """Show clinic's logs in a certain date"""
    date = request.form.get("date")
    history = db.execute("select patient, procedure, date, price from procedures where date = ? and user = ?", date, session["user_name"])
    total = db.execute("select sum(price) from procedures where user = ? and date like ? ", session["user_name"], date)
    return render_template("finance.html", history=history, total = total)

@app.route("/finance_special_m", methods=["GET", "POST"])
@login_required
def finance_special_m():
     # showing all procedures and the total income of a specific time range in a certain month
    date =  request.form.get("date_m")
    history = db.execute("select patient, procedure, date, price from procedures where date like ? and user = ?", f"{date}%", session["user_name"])
    total = db.execute("select sum(price) from procedures where user = ? and date like ? ", session["user_name"], f"{date}%")
    return render_template("finance.html", history=history, total = total)

@app.route("/finance_special_y", methods=["GET", "POST"])
@login_required
def finance_special_y():
    # showing all procedures and the total income of a specific time range in a certain year
    date = request.form.get("date_y")
    history = db.execute("select patient, procedure, date, price from procedures where date like ? and user = ?", f"{date}%", session["user_name"])
    total = db.execute("select sum(price) from procedures where user = ? and date like ? ", session["user_name"], f"{date}%")
    return render_template("finance.html", history=history, total = total)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return Error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return Error("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return Error("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add_new",  methods=["GET", "POST"])
@login_required
def add_new():
    #adding new patient
    if request.method == "POST":
        patient =  request.form.get("name")
        date = request.form.get("date")
        hour = request.form.get("Time")
        procedure = request.form.get("pro")
        db.execute("insert into appointments(patient, day, hour, procedure, user) values(?, ?, ?, ?, ?)", patient, date, hour, procedure, session["user_name"])
        return redirect("/")
    else:
        return render_template("new.html")

@app.route("/certain_date", methods=["GET", "POST"])
@login_required
def date():
    # getting appointments from a certain date
    certain_date = request.form.get("certain_day")
    certain_appointments = db.execute("select * from appointments where day = ? and user= ?", certain_date, session["user_name"])
    if not certain_date:
        return Error("empty date", 403)
    if not certain_appointments:
        return Error("no appointments on that day", 403)
    return render_template("certainDate.html", certain_appointments = certain_appointments)

@app.route("/staff", methods=["GET", "POST"])
@login_required
def staff():
    #adding a new employee
    if request.method == "POST":
        Name = request.form.get("Name")
        Role = request.form.get("Role")
        Age = request.form.get("Age")
        Salary = request.form.get("Salary")
        db.execute("insert into staff (Name, Role, Age, Salary, user) values(?, ?, ?, ?, ?)", Name, Role, Age, Salary, session["user_name"])
        return redirect("/staff")
    else:
        #showing staff
        staff = db.execute("select * from staff where user = ?", session["user_name"])
        return render_template("staff.html", staff = staff)

@app.route("/pro", methods=["GET", "POST"])
@login_required
def pro():
    #adding procedure
    if request.method == "POST":
        patient = request.form.get("patient")
        operator = request.form.get("operator")
        if request.form.get("date"):
            date = request.form.get("date")
        else:
            date = datetime.today().strftime('%Y-%m-%d')
        procedure = request.form.get("procedure")
        comments = request.form.get("comments")
        price = request.form.get("price")
        db.execute("insert into procedures (patient, operator, procedure, comments, price, user, date) values(?, ?, ?, ?, ?, ?, ?)", patient, operator, procedure, comments, price, session["user_name"], date)
        return redirect("/pro")
    else:
        #showing procedures
         procedures = db.execute("select * from procedures where user = ?", session["user_name"])
         return render_template("procedure.html", procedures = procedures)

@app.route("/Sign-up", methods=["GET", "POST"])
def sign_up():
    """Register user"""
    if request.method == "POST":
        clinic_name = request.form.get("clinic_name")
        Owner = request.form.get("Owner")
        user_name = request.form.get("username")
        password = request.form.get("password")
        password1 = request.form.get("confirmation")
        check = db.execute("select username FROM users WHERE username= ?", user_name)
        if check:
            return Error("username already taken")
        elif password != password1:
            return Error("passwords don't match")
        hashed = generate_password_hash(password)
        db.execute("INSERT INTO users(username, password, clinic_name, Owner) VALUES(?, ?, ?, ?)", user_name, hashed, clinic_name, Owner)
        return redirect("/")
    else:
        return render_template("register.html")



@app.route("/new_password", methods=["GET", "POST"])
@login_required
def change():
    #changing password
    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            return Error("NEW Password REQUIRED")
        hashed1 = generate_password_hash(password)
        
        old = db.execute("SELECT * FROM users WHERE username = ?", session["user_name"])
        if check_password_hash(old[0]["password"], password):
            return Error("don't use the same old password")

        db.execute("UPDATE users SET password = ? WHERE username = ?", hashed1, session["user_name"])
        return redirect("/")
    else:
        return render_template("pass.html")

@app.route("/delete", methods=["POST"])
def delete():
    #delete an appointment
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM appointments WHERE id = ?", id)
    return redirect("/")

@app.route("/contact")
def contact():
    # directing to contact info page
    return render_template("contact.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    #searching patient's logs in procedures table
    session["search"] = request.form.get("search")
    patient_log = db.execute("select * from procedures where patient = ? and user = ?", session["search"], session["user_name"])
    return render_template("search.html", patient_log = patient_log)