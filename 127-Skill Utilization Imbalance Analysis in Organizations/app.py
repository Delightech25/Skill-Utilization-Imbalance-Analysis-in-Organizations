from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import random


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Load trained model
model = joblib.load("model.pkl")

# -------------------- MODELS --------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    python = db.Column(db.Float)
    ml = db.Column(db.Float)
    sql = db.Column(db.Float)
    management = db.Column(db.Float)
    cloud = db.Column(db.Float)

    r_python = db.Column(db.Float)
    r_ml = db.Column(db.Float)
    r_sql = db.Column(db.Float)
    r_management = db.Column(db.Float)
    r_cloud = db.Column(db.Float)

    status = db.Column(db.String(50))


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100))
    status = db.Column(db.String(50))


# -------------------- LOGIN --------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------- ROUTES --------------------

@app.route("/")
@login_required
def dashboard():
    alerts = Alert.query.all()

    under = Employee.query.filter_by(status="Underutilized").count()
    balanced = Employee.query.filter_by(status="Balanced").count()
    over = Employee.query.filter_by(status="Overloaded").count()

    chart_data = [under, balanced, over]

    accuracy = 93  # manually update if needed

    return render_template(
        "dashboard.html",
        alerts=alerts,
        chart_data=chart_data,
        accuracy=accuracy
    )

@app.route("/generate-data")
@login_required
def generate_data():

    def create_employee(name, status_type):
        if status_type == "Underutilized":
            # Employee strong, required weak
            emp_skills = [random.randint(7, 10) for _ in range(5)]
            req_skills = [random.randint(2, 4) for _ in range(5)]

        elif status_type == "Overloaded":
            # Employee weak, required strong
            emp_skills = [random.randint(2, 4) for _ in range(5)]
            req_skills = [random.randint(7, 10) for _ in range(5)]

        else:  # Balanced
            emp_skills = [random.randint(5, 8) for _ in range(5)]
            req_skills = [
                max(1, min(10, skill + random.randint(-1, 1)))
                for skill in emp_skills
            ]

        features = emp_skills + req_skills
        prediction = model.predict([features])[0]

        emp = Employee(
            name=name,
            python=emp_skills[0],
            ml=emp_skills[1],
            sql=emp_skills[2],
            management=emp_skills[3],
            cloud=emp_skills[4],
            r_python=req_skills[0],
            r_ml=req_skills[1],
            r_sql=req_skills[2],
            r_management=req_skills[3],
            r_cloud=req_skills[4],
            status=prediction
        )

        db.session.add(emp)

        if prediction != "Balanced":
            alert = Alert(employee_name=name, status=prediction)
            db.session.add(alert)

    names = ["Rahul", "Kiran", "Sneha", "Anjali", "Vikram",
             "Priya", "Arjun", "Meena", "Rohit", "Divya"]

    counter = 0

    # 5 Overloaded
    for _ in range(5):
        create_employee(random.choice(names) + f"_O{counter}", "Overloaded")
        counter += 1

    # 7 Underutilized
    for _ in range(7):
        create_employee(random.choice(names) + f"_U{counter}", "Underutilized")
        counter += 1

    # 8 Balanced
    for _ in range(8):
        create_employee(random.choice(names) + f"_B{counter}", "Balanced")
        counter += 1

    db.session.commit()

    return "Generated 5 Overloaded, 7 Underutilized, 8 Balanced employees!"

@app.route("/add-employee", methods=["GET", "POST"])
@login_required
def add_employee():
    if request.method == "POST":
        data = request.form

        # 10 FEATURES ONLY
        features = [
            float(data["python"]),
            float(data["ml"]),
            float(data["sql"]),
            float(data["management"]),
            float(data["cloud"]),
            float(data["r_python"]),
            float(data["r_ml"]),
            float(data["r_sql"]),
            float(data["r_management"]),
            float(data["r_cloud"])
        ]

        prediction = model.predict([features])[0]

        emp = Employee(
            name=data["name"],
            python=data["python"],
            ml=data["ml"],
            sql=data["sql"],
            management=data["management"],
            cloud=data["cloud"],
            r_python=data["r_python"],
            r_ml=data["r_ml"],
            r_sql=data["r_sql"],
            r_management=data["r_management"],
            r_cloud=data["r_cloud"],
            status=prediction
        )

        db.session.add(emp)

        if prediction != "Balanced":
            alert = Alert(employee_name=data["name"], status=prediction)
            db.session.add(alert)

        db.session.commit()

        return redirect("/employees")

    return render_template("add_employee.html")


@app.route("/employees")
@login_required
def employees():
    all_employees = Employee.query.all()
    return render_template("employees.html", employees=all_employees)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed_password = generate_password_hash(request.form["password"])
        new_user = User(
            username=request.form["username"],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# -------------------- RUN --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True,port=5050)