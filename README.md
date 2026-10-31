# Skill-Utilization-Imbalance-Analysis-in-Organizations

An analytical web application and machine learning dashboard designed to assess, measure, and visualize skill utilization imbalances across teams and departments, helping leadership optimize workforce allocation and bridge competency gaps.

---

## 🚀 Overview
The **Skill Utilization Imbalance Analysis** tool is a Flask-based web application backed by a machine learning classifier (`RandomForestClassifier`). It evaluates employees' current skill sets against project requirements across key technical and management competencies, categorizing workforce deployment into three distinct statuses:
1. **Balanced**: Skills perfectly match project requirements.
2. **Underutilized**: Employees possess advanced skills far beyond current project requirements (risk of disengagement).
3. **Overloaded**: Project requirements exceed employees' current competencies (risk of burnout/skill gaps).

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug
* **Machine Learning:** Scikit-Learn (`RandomForestClassifier`), Joblib, NumPy, Pandas
* **Database:** SQLite (`database.db`)
* **Frontend:** HTML5, CSS / Bootstrap, Template-based dashboard rendering

---

## 📁 Project Structure
```text
├── app.py                # Main Flask application (routes, authentication, ML inference)
├── generate_data.py      # Synthetic organizational dataset generator (dataset.csv)
├── model.pkl             # Serialized trained Machine Learning classifier
├── dataset.csv           # Training and evaluation data source
├── requirements.txt      # Project dependencies
└── templates/            # HTML templates (dashboard, login, employees, add_employee, register)
