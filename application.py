import os
import sqlite3
from flask import g
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import re
from flask import url_for

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure a database
# Function for a database
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("password_confirmation"):
            return apology("must provide password confirmation", 400)
        if not request.form.get("fullname"):
            return apology("must provide your full name", 400)
        if not request.form.get("gender"):
            return apology("must provide your gender", 400)
        if not request.form.get("age"):
            return apology("must provide your age", 400)
        if not request.form.get("gender"):
            return apology("must provide gender", 400)
        if not request.form.get("experience"):
            return apology("must provide your experience", 400)
        if not request.form.get("specialty"):
            return apology("must provide your specialty", 400)

        if request.form.get("password") != request.form.get("password_confirmation"):
            return apology("passwords do not match", 400)
        if request.form.get("gender") != "male" and request.form.get("gender") != "female":
            return apology("please choose either male or female gender", 400)

        regex_numbers_age = re.search("[^0-9.]", request.form.get("age"))
        regex_fraction_dot_age = re.search("[0-9]+\.[1-9]+", request.form.get("age"))
        if regex_numbers_age != None:
            return apology("only numeric characters accepted", 400)
        if regex_fraction_dot_age != None:
            return apology("fractions are not accepted", 400)
        if float(request.form.get("age")) < 0:
            return apology("negative numbers are not accepted", 400)

        regex_numbers_experience = re.search("[^0-9.]", request.form.get("experience"))
        regex_fraction_dot_experience = re.search("[0-9]+\.[1-9]+", request.form.get("experience"))
        if regex_numbers_experience != None:
            return apology("only numeric characters accepted", 400)
        if regex_fraction_dot_experience != None:
            return apology("fractions are not accepted", 400)
        if float(request.form.get("experience")) < 0:
            return apology("negative numbers are not accepted", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT username FROM doctors WHERE username = ?", (request.form.get("username").lower(),))
        rows = cur.fetchall()
        if len(rows) == 1:
            return apology("username already exists", 400)

        # Insert user into the database
        hashed_password = generate_password_hash(request.form.get("password"))
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO doctors(username, password, full_name, gender, age, experience, specialty) VALUES(?,?,?,?,?,?,?)", (request.form.get("username").lower(), hashed_password, request.form.get("fullname"), request.form.get("gender"), request.form.get("age"), request.form.get("experience"), request.form.get("specialty"),))
        con.commit()
        con.close()

        # Log in user
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM doctors WHERE username = ?", (request.form.get("username").lower(),))
        rows = cur.fetchall()
        session["user_id"] = rows[0]["id"]

        return redirect("/patients")
    else:
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Query database for username
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM doctors WHERE username = ?", (request.form.get("username").lower(),))
        rows = cur.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/patients")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/patients")
@login_required
def patients():
    con = sqlite3.connect('./medical_history.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM medical_encounters WHERE doctor_id = ? ORDER BY date DESC", (session["user_id"],))
    data = cur.fetchall()
    cur.execute("SELECT full_name FROM doctors WHERE id = ?", (session["user_id"],))
    fullname = cur.fetchall()
    return render_template("patients.html", data = data, fullname = fullname)

@app.route("/patient/<patient_id>", methods=["GET", "DELETE", "PUT"])
@login_required
def patient(patient_id):
    if request.method == "GET":
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("SELECT * FROM social_history WHERE id = ?", (patient_id,))
        social_history = cur.fetchall()
        cur.execute("SELECT * FROM family_history WHERE patient_id = ?", (patient_id,))
        family_history = cur.fetchall()
        cur.execute("SELECT * FROM habits WHERE patient_id = ?", (patient_id,))
        habits = cur.fetchall()
        cur.execute("SELECT * FROM diseases WHERE patient_id = ?", (patient_id,))
        diseases = cur.fetchall()
        cur.execute("SELECT * FROM allergies WHERE patient_id = ?", (patient_id,))
        allergies = cur.fetchall()
        cur.execute("SELECT * FROM surgical_history WHERE patient_id = ?", (patient_id,))
        surgical_history = cur.fetchall()
        cur.execute("SELECT * FROM immunization_history WHERE patient_id = ?", (patient_id,))
        immunization_history = cur.fetchall()
        cur.execute("SELECT * FROM tests_results WHERE patient_id = ?", (patient_id,))
        tests_results = cur.fetchall()
        cur.execute("SELECT diseases.id, diseases.name AS disease_name, diseases.medication_id, medications.name AS medication_name, medications.description AS medication_description, diseases.dosage FROM diseases JOIN medications ON diseases.medication_id = medications.id WHERE diseases.patient_id = ?", (patient_id,))
        medications_diseases = cur.fetchall()
        cur.execute("SELECT allergies.id, allergies.name AS allergy_name, allergies.medication_id, medications.name AS medication_name, medications.description AS medication_description, allergies.dosage FROM allergies JOIN medications ON allergies.medication_id = medications.id WHERE allergies.patient_id = ?", (patient_id,))
        medications_allergies = cur.fetchall()
        cur.execute("SELECT immunization_history.id, immunization_history.name AS immunization_name, immunization_history.medication_id, medications.name AS medication_name, medications.description AS medication_description FROM immunization_history JOIN medications ON immunization_history.medication_id = medications.id WHERE immunization_history.patient_id = ?", (patient_id,))
        medications_immunization = cur.fetchall()
        cur.execute("SELECT * FROM medical_encounters WHERE patient_id = ?", (patient_id,))
        encounters = cur.fetchall()

        data = {
            'social_history': social_history,
            'family_history': family_history,
            'habits': habits,
            'diseases': diseases,
            'allergies': allergies,
            'surgical_history': surgical_history,
            'immunization_history': immunization_history,
            'tests_results': tests_results,
            'medications_diseases': medications_diseases,
            'medications_allergies': medications_allergies,
            'medications_immunization': medications_immunization,
            'encounters': encounters
        }
        session['patient_id'] = patient_id
        session['patient_fullname'] = social_history[0]['full_name']
        return render_template("patient.html", data=data)
    elif request.method == "DELETE":
        response = None
        if int(request.get_json()['doctor_id']) == session['user_id']:
            con = sqlite3.connect('./medical_history.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("DELETE FROM medical_encounters WHERE doctor_id = ? AND id = ?", (session["user_id"], int(request.get_json()['encounter_id']),))
            con.commit()
            con.close()
            response = {"encounter_id": request.get_json()['encounter_id']}
        else:
            response = "You can't delete encounters that are not created by you!"
        return jsonify(response)
    elif request.method == "PUT":
        response = None
        # check for empty fields
        if len(request.get_json()['chief_complaint_new_input']) == 0:
            return apology("edited value of chief complaint is empty", 400)
        if len(request.get_json()['history_of_illness_new_input']) == 0:
            return apology("edited value of history of illness is empty", 400)
        if len(request.get_json()['examination_new_input']) == 0:
            return apology("edited value of history of illness is empty", 400)
        if len(request.get_json()['assessment_and_plan_new_input']) == 0:
            return apology("edited value of assessment and plan is empty", 400)

        if int(request.get_json()['doctor_id']) == session['user_id']:
            con = sqlite3.connect('./medical_history.db')
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("UPDATE medical_encounters SET chief_complaint = ?, history_of_illness = ?, examination = ?, assessment_and_plan = ? WHERE doctor_id = ? AND id = ?", (request.get_json()['chief_complaint_new_input'], request.get_json()['history_of_illness_new_input'], request.get_json()['examination_new_input'], request.get_json()['assessment_and_plan_new_input'], session["user_id"], int(request.get_json()['encounter_id']),))
            con.commit()
            cur.execute("SELECT * FROM medical_encounters WHERE id = ?", (int(request.get_json()['encounter_id']),))
            edited_encounter = cur.fetchall()
            #for row in rows:
            #data.append(list(row))

            response = {
                "encounter_id": request.get_json()['encounter_id'],
                "edited_encounter": edited_encounter
            }
        else:
            response = "You can't edit encounters that are not created by you!"
        return jsonify(response)


@app.route("/social_history", methods=["GET", "POST"])
@login_required
def social_history():
    if request.method == "POST":
        if not request.form.get("patient_fullname"):
            return apology("must provide patient's full name", 400)
        if not request.form.get("patient_gender"):
            return apology("must provide patient's gender", 400)
        if not request.form.get("patient_age"):
            return apology("must provide patient's age", 400)
        if not request.form.get("passport_number"):
            return apology("must provide passport number", 400)
        if not request.form.get("patient_address"):
            return apology("must provide patient's address", 400)
        if not request.form.get("patient_religion"):
            return apology("must provide patient's religion", 400)
        if not request.form.get("patient_occupation"):
            return apology("must provide patient's occupation", 400)
        if not request.form.get("patient_race"):
            return apology("must provide patient's race", 400)
        if not request.form.get("patient_nationality"):
            return apology("must provide patient's nationality", 400)
        if not request.form.get("patient_gender"):
            return apology("must provide gender", 400)

        if request.form.get("patient_gender") != "male" and request.form.get("patient_gender") != "female":
            return apology("please choose either male or female gender", 400)

        # age
        regex_numbers_patient_age = re.search("[^0-9.]", request.form.get("patient_age"))
        regex_fraction_dot_patient_age = re.search("[0-9]+\.[1-9]+", request.form.get("patient_age"))

        if regex_numbers_patient_age != None:
            return apology("only numeric characters accepted", 400)
        if regex_fraction_dot_patient_age != None:
            return apology("fractions are not accepted", 400)
        if float(request.form.get("patient_age")) < 0:
            return apology("negative numbers are not accepted", 400)

         # passport number
        regex_numbers_passport_number = re.search("[^0-9.]", request.form.get("passport_number"))
        regex_fraction_dot_passport_number = re.search("[0-9]+\.[1-9]+", request.form.get("passport_number"))

        if regex_numbers_passport_number != None:
            return apology("only numeric characters accepted", 400)
        if regex_fraction_dot_passport_number != None:
            return apology("fractions are not accepted", 400)
        if float(request.form.get("passport_number")) < 0:
            return apology("negative numbers are not accepted", 400)

        # database
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO social_history(full_name, gender, age, passport_number, address, religion, occupation, race, nationality, doctor_id) VALUES(?,?,?,?,?,?,?,?,?,?)", (request.form.get("patient_fullname"),  request.form.get("patient_gender"), request.form.get("patient_age"), request.form.get("passport_number"), request.form.get("patient_address"), request.form.get("patient_religion"), request.form.get("patient_occupation"), request.form.get("patient_race"), request.form.get("patient_nationality"), session["user_id"],))
        con.commit()
        con.close()

        # session
        session['patient_fullname'] = request.form.get("patient_fullname")
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT MAX(id) FROM social_history WHERE doctor_id = ?", (session["user_id"],))
        last_id  = cur.fetchall()[0]['MAX(id)']
        session['patient_id'] = last_id

        return redirect("/family_history")
    else:
        # if another patient was created during existing session, delete their data from the session
        if session.get('section') == True:
            session.pop('section');
        if session.get('link_back') == True:
            session.pop('link_back');
        if session.get('link_forward') == True:
            session.pop('link_forward');
        return render_template("new_patient/social_history.html")


@app.route("/family_history", methods=["GET", "POST"])
@login_required
def family_history():
    if request.method == "POST":
        if not request.form.get("relative_name"):
            return apology("must provide relative full name", 400)
        if not request.form.get("relative_status"):
            return apology("must provide relative status", 400)
        if not request.form.get("relative_gender"):
            return apology("must provide relative gender", 400)
        if not request.form.get("relative_age"):
            return apology("must relative age", 400)
        if request.form.get("relative_gender") != "male" and request.form.get("relative_gender") != "female":
            return apology("relative gender must be 'male' of 'female' ", 400)

        # check age format
        regex_integers_relative_age = re.search("^\d+$", request.form.get("relative_age"))

        if request.form.get("relative_age") and regex_integers_relative_age == None:
            return apology("relative age must be a positive integer", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO family_history(full_name, relative_status, gender, age, allergies, diseases, cause_of_death, patient_id) VALUES(?,?,?,?,?,?,?,?)", (request.form.get("relative_name"),  request.form.get("relative_status"), request.form.get("relative_gender"), request.form.get("relative_age"), request.form.get("relative_allergies"), request.form.get("relative_diseases"), request.form.get("relative_cause_of_death"), session['patient_id'],))
        con.commit()
        con.close()

        session['section'] = "relative"
        session['link_back'] = "/family_history"
        session['link_forward'] = "/habits"
        return redirect('/proposition')
    else:
        return render_template("new_patient/family_history.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/habits", methods=["GET", "POST"])
@login_required
def habits():
    if request.method == "POST":
        if not request.form.get("habit_name"):
            return apology("must provide habit name", 400)
        if not request.form.get("habit_year"):
            return apology("must provide habit year", 400)

        # check year format
        regex_integers_habit_year = re.search("^\d+$", request.form.get("habit_year"))

        if request.form.get("habit_year") and regex_integers_habit_year == None:
            return apology("year must be a positive integer", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO habits(name, year, patient_id) VALUES(?,?,?)", (request.form.get("habit_name"),  request.form.get("habit_year"), session['patient_id'],))
        con.commit()
        con.close()

        session['section'] = "habit"
        session['link_back'] = "/habits"
        session['link_forward'] = "/diseases"
        return redirect('/proposition')
    else:
        return render_template("new_patient/habits.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/diseases", methods=["GET", "POST"])
@login_required
def diseases():
    if request.method == "POST":
        if not request.form.get("disease_name"):
            return apology("must provide name of the disease", 400)
        if not request.form.get("disease_description"):
            return apology("must provide description of the disease", 400)
        if not request.form.get("disease_date_of_diagnosis"):
            return apology("must provide date of disease's diagnosis", 400)

        # check date format
        regex_date_format_date_of_diagnosis = re.search("\d{4}-\d{2}-\d{2}", request.form.get("disease_date_of_diagnosis"))
        regex_date_format_end_of_treatment = re.search("\d{4}-\d{2}-\d{2}", request.form.get("disease_end_of_treatment"))

        if regex_date_format_date_of_diagnosis == None:
            return apology("the date must be in format yyyy-mm-dd", 400)
        if request.form.get("disease_end_of_treatment") and regex_date_format_end_of_treatment == None:
            return apology("the date must be in format yyyy-mm-dd", 400)

        # check id format
        regex_integers_medication_id = None

        if request.form.get("disease_medications_options") != None:
            regex_integers_medication_id = re.search("^\d+$", request.form.get("disease_medications_options"))

        if request.form.get("disease_medications_options") != None and regex_integers_medication_id == None:
            return apology("medication id must be a positive integer", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO diseases(name, description, date, end_of_treatment, medication_id, dosage, patient_id, doctor_id) VALUES(?,?,?,?,?,?,?,?)", (request.form.get("disease_name"),  request.form.get("disease_description"), request.form.get("disease_date_of_diagnosis"), request.form.get("disease_end_of_treatment"), request.form.get("disease_medications_options"), request.form.get("disease_medication_dosage"), session['patient_id'], session["user_id"],))
        con.commit()
        con.close()

        session['section'] = "disease"
        session['link_back'] = "/diseases"
        session['link_forward'] = "/allergies"
        return redirect('/proposition')
    else:
        return render_template("new_patient/diseases.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/diseases_medications", methods=["GET", "POST"])
@login_required
def diseases_medications():
    if request.method == "POST":
        if not request.form.get("disease_medication_name"):
            return apology("must provide name of the medication", 400)
        if not request.form.get("disease_medication_description"):
            return apology("must provide description of the medication", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT name FROM medications WHERE name = ?", (request.form["disease_medication_name"].lower(),))
        medication = cur.fetchall()

        if len(medication) > 0:
            return jsonify({"message": "medication already exists"})
        # insert medication into database
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("INSERT INTO medications(name, description) VALUES(?,?)", (request.form["disease_medication_name"],  request.form["disease_medication_description"],))
        con.commit()
        con.close()
        # refresh the list of available medications
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT * FROM medications")
        medications = cur.fetchall()
        return jsonify(medications)
    else:
        medications = [{"name": "No matches"}]
        if len(request.args.get("disease_medication_input_name")) > 0:
            con = sqlite3.connect('./medical_history.db')
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM medications WHERE name LIKE ?", ("%" + request.args.get("disease_medication_input_name") + "%",))
            medications = cur.fetchall()
            if len(medications) == 0:
                medications = [{"name": "No matches"}]
        return jsonify(medications)


@app.route("/allergies", methods=["GET", "POST"])
@login_required
def allergies():
    if request.method == "POST":
        if not request.form.get("allergy_name"):
            return apology("must provide name of the allergy", 400)
        if not request.form.get("allergy_description"):
            return apology("must provide description of the allergy", 400)
        if not request.form.get("allergy_date_of_diagnosis"):
            return apology("must provide date of disease's diagnosis", 400)

        # check date format
        regex_date_format_date_of_diagnosis = re.search("\d{4}-\d{2}-\d{2}", request.form.get("allergy_date_of_diagnosis"))
        regex_date_format_end_of_treatment = re.search("\d{4}-\d{2}-\d{2}", request.form.get("allergy_end_of_treatment"))

        if regex_date_format_date_of_diagnosis == None:
            return apology("the date must be in format yyyy-mm-dd", 400)
        if request.form.get("disease_end_of_treatment") and regex_date_format_end_of_treatment == None:
            return apology("the date must be in format yyyy-mm-dd", 400)

        # check id format
        regex_integers_medication_id = None

        if request.form.get("allergy_medications_options") != None:
            regex_integers_medication_id = re.search("^\d+$", request.form.get("allergy_medications_options"))

        if request.form.get("allergy_medications_options") != None and regex_integers_medication_id == None:
            return apology("medication id must be a positive integer", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO allergies(name, description, date, end_of_treatment, medication_id, dosage, patient_id, doctor_id) VALUES(?,?,?,?,?,?,?,?)", (request.form.get("allergy_name"),  request.form.get("allergy_description"), request.form.get("allergy_date_of_diagnosis"), request.form.get("allergy_end_of_treatment"), request.form.get("allergy_medications_options"), request.form.get("allergy_medication_dosage"), session['patient_id'], session["user_id"],))
        con.commit()
        con.close()

        session['section'] = "allergy"
        session['link_back'] = "/allergies"
        session['link_forward'] = "/surgical_history"
        return redirect('/proposition')
    else:
        return render_template("new_patient/allergies.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/allergies_medications", methods=["GET", "POST"])
@login_required
def allergies_medications():
    if request.method == "POST":
        if not request.form.get("allergy_medication_name"):
            return apology("must provide name of the medication", 400)
        if not request.form.get("allergy_medication_description"):
            return apology("must provide description of the medication", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT name FROM medications WHERE name = ?", (request.form["allergy_medication_name"].lower(),))
        medication = cur.fetchall()

        if len(medication) > 0:
            return jsonify({"message": "medication already exists"})
        # insert medication into database
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("INSERT INTO medications(name, description) VALUES(?,?)", (request.form["allergy_medication_name"],  request.form["allergy_medication_description"],))
        con.commit()
        con.close()
        # refresh the list of available medications
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT * FROM medications")
        medications = cur.fetchall()
        return jsonify(medications)
    else:
        medications = [{"name": "No matches"}]
        if len(request.args.get("allergy_medication_input_name")) > 0:
            con = sqlite3.connect('./medical_history.db')
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM medications WHERE name LIKE ?", ("%" + request.args.get("allergy_medication_input_name") + "%",))
            medications = cur.fetchall()
            if len(medications) == 0:
                medications = [{"name": "No matches"}]
        return jsonify(medications)


@app.route("/surgical_history", methods=["GET", "POST"])
@login_required
def surgical_history():
    if request.method == "POST":
        if not request.form.get("surgery_name"):
            return apology("must provide surgery name", 400)
        if not request.form.get("surgery_description"):
            return apology("must provide description of the surgery", 400)
        if not request.form.get("surgery_date"):
            return apology("must provide date of the surgery", 400)
        if not request.form.get("surgery_preoperative_diagnosis"):
            return apology("must provide surgery preoperative diagnosis", 400)
        if not request.form.get("surgery_postoperative_diagnosis"):
            return apology("must provide surgery_postoperative_diagnosis", 400)
        if not request.form.get("condition_after_surgery"):
            return apology("must provide condition after surgery", 400)

        # check date format
        regex_date_format_surgery_date = re.search("\d{4}-\d{2}-\d{2}", request.form.get("surgery_date"))

        if regex_date_format_surgery_date == None:
            return apology("the date must be in format yyyy-mm-dd", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO surgical_history(operation_name, description, date, preoperative_diagnosis, postoperative_diagnosis, condition_after_surgery, patient_id, doctor_id) VALUES(?,?,?,?,?,?,?,?)", (request.form.get("surgery_name"),  request.form.get("surgery_description"), request.form.get("surgery_date"), request.form.get("surgery_preoperative_diagnosis"), request.form.get("surgery_postoperative_diagnosis"), request.form.get("condition_after_surgery"), session['patient_id'], session["user_id"],))
        con.commit()
        con.close()

        session['section'] = "surgery"
        session['link_back'] = "/surgical_history"
        session['link_forward'] = "/immunization_history"
        return redirect('/proposition')
    else:
        return render_template("new_patient/surgical_history.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/immunization_history", methods=["GET", "POST"])
@login_required
def immunization_history():
    if request.method == "POST":
        if not request.form.get("immunization_name"):
            return apology("must provide immunization name", 400)
        if not request.form.get("immunization_date"):
            return apology("must provide immunization date", 400)

        # check date format
        regex_date_format_immunization_date = re.search("\d{4}-\d{2}-\d{2}", request.form.get("immunization_date"))

        if regex_date_format_immunization_date == None:
            return apology("the date must be in format yyyy-mm-dd", 400)

        # check medication id format
        regex_integers_medication_id = None

        if request.form.get("immunization_medications_options") != None:
            regex_integers_medication_id = re.search("^\d+$", request.form.get("immunization_medications_options"))
        if request.form.get("immunization_medications_options") != None and regex_integers_medication_id == None:
            return apology("medication id must be a positive integer", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO immunization_history(name, date, medication_id, patient_id) VALUES(?,?,?,?)", (request.form.get("immunization_name"),  request.form.get("immunization_date"), request.form.get("immunization_medications_options"), session['patient_id'],))
        con.commit()
        con.close()

        session['section'] = "immunization"
        session['link_back'] = "/immunization_history"
        session['link_forward'] = "/tests_results"
        return redirect('/proposition')
    else:
        return render_template("new_patient/immunization_history.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/immunization_medications", methods=["GET", "POST"])
@login_required
def immunization_medications():
    if request.method == "POST":
        if not request.form.get("immunization_medication_name"):
            return apology("must provide name of the medication", 400)
        if not request.form.get("immunization_medication_description"):
            return apology("must provide description of the medication", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT name FROM medications WHERE name = ?", (request.form["immunization_medication_name"].lower(),))
        medication = cur.fetchall()

        if len(medication) > 0:
            return jsonify({"message": "medication already exists"})
        # insert medication into database
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("INSERT INTO medications(name, description) VALUES(?,?)", (request.form["immunization_medication_name"],  request.form["immunization_medication_description"],))
        con.commit()
        con.close()
        # refresh the list of available medications
        con = sqlite3.connect('./medical_history.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT * FROM medications")
        medications = cur.fetchall()
        return jsonify(medications)
    else:
        medications = [{"name": "No matches"}]
        if len(request.args.get("immunization_medication_input_name")) > 0:
            con = sqlite3.connect('./medical_history.db')
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM medications WHERE name LIKE ?", ("%" + request.args.get("immunization_medication_input_name") + "%",))
            medications = cur.fetchall()
            if len(medications) == 0:
                medications = [{"name": "No matches"}]
        return jsonify(medications)


@app.route("/tests_results", methods=["GET", "POST"])
@login_required
def tests_results():
    if request.method == "POST":
        if not request.form.get("test_name"):
            return apology("must provide test name", 400)
        if not request.form.get("test_date"):
            return apology("must provide test date", 400)
        if not request.form.get("test_result_description"):
            return apology("must provide test result description", 400)

        # check date format
        regex_date_format_test_date = re.search("\d{4}-\d{2}-\d{2}", request.form.get("test_date"))

        if regex_date_format_test_date == None:
            return apology("the date must be in format yyyy-mm-dd", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO tests_results(name, date, result_description, patient_id) VALUES(?,?,?,?)", (request.form.get("test_name"),  request.form.get("test_date"), request.form.get("test_result_description"), session['patient_id'],))
        con.commit()
        con.close()

        session['section'] = "test"
        session['link_back'] = "/tests_results"
        session['link_forward'] = f"/patient/{session['patient_id']}"
        return redirect('/proposition')
    else:
        return render_template("new_patient/tests_results.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/encounters", methods=["GET", "POST"])
@login_required
def encounters():
    if request.method == "POST":
        if not request.form.get("chief_complaint"):
            return apology("must provide chief complaint", 400)
        if not request.form.get("history_of_illness"):
            return apology("must provide history of illness", 400)
        if not request.form.get("examination"):
            return apology("must provide examination", 400)
        if not request.form.get("assessment_and_plan"):
            return apology("must provide assessment and plan", 400)

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("INSERT INTO medical_encounters(chief_complaint, history_of_illness, examination, assessment_and_plan, patient_id, doctor_id) VALUES(?,?,?,?,?,?)", (request.form.get("chief_complaint"),  request.form.get("history_of_illness"), request.form.get("examination"), request.form.get("assessment_and_plan"), session['patient_id'], session["user_id"],))
        con.commit()
        con.close()

        return redirect(f"/patient/{session['patient_id']}")
    else:
        return render_template("/encounters.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'])


@app.route("/proposition")
@login_required
def proposition():
    return render_template("new_patient/proposition.html", patient_fullname = session['patient_fullname'], patient_id = session['patient_id'], current_section = session['section'], link_back=session['link_back'], link_forward=session['link_forward'])


@app.route("/find_patient", methods=["GET", "POST"])
@login_required
def find_patient():
    if request.method == "POST":
        data = None
        # no parameters provided
        if not request.form.get("find_patient_fullname") and not request.form.get("find_patient_address") and not request.form.get("find_patient_passport_number") and not request.form.get("find_patient_id"):
             return apology("must provide at least one search parameter", 400)

        search_string = "SELECT * FROM social_history WHERE "
        search_parameters = []
        first_parameter = True

        if request.form.get("find_patient_id"):
            if first_parameter == True:
                search_string += "id = ?"
            else:
                search_string += " AND id = ?"
            first_parameter = False
            search_parameters.append(request.form.get("find_patient_id"))
        if request.form.get("find_patient_passport_number"):
            if first_parameter == True:
                search_string += "passport_number = ?"
            else:
                search_string += " AND passport_number = ?"
            first_parameter = False
            search_parameters.append(request.form.get("find_patient_passport_number"))
        if request.form.get("find_patient_fullname"):
            if first_parameter == True:
                search_string += "full_name LIKE ?"
            else:
                search_string += " AND full_name LIKE ?"
            first_parameter = False
            search_parameters.append("%" + request.form.get("find_patient_fullname").lower() + "%")
        if request.form.get("find_patient_address"):
            if first_parameter == True:
                search_string += "address LIKE ?"
            else:
                search_string += " AND address LIKE ?"
            first_parameter = False
            search_parameters.append("%" + request.form.get("find_patient_address").lower() + "%")
        if request.form.get("my_patients") == "on":
            if first_parameter == True:
                search_string += "doctor_id = ?"
            else:
                search_string += " AND doctor_id = ?"
            first_parameter = False
            search_parameters.append(session['user_id'])

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(search_string, (*search_parameters,))
        data = cur.fetchall()
        return render_template("/found_patients.html", data = data)
    else:
        return render_template("/find_patient.html")


@app.route("/find_doctor", methods=["GET", "POST"])
@login_required
def find_doctor():
    if request.method == "POST":
        data = None
        # no parameters provided
        if not request.form.get("find_doctor_id") and not request.form.get("find_doctor_fullname") and not request.form.get("find_doctor_specialty"):
             return apology("must provide at least one search parameter", 400)

        search_string = "SELECT * FROM doctors WHERE "
        search_parameters = []
        first_parameter = True

        if request.form.get("find_doctor_id"):
            if first_parameter == True:
                search_string += "id = ?"
            else:
                search_string += " AND id = ?"
            first_parameter = False
            search_parameters.append(request.form.get("find_doctor_id"))
        if request.form.get("find_doctor_fullname"):
            if first_parameter == True:
                search_string += "full_name LIKE ?"
            else:
                search_string += " AND full_name LIKE ?"
            first_parameter = False
            search_parameters.append("%" + request.form.get("find_doctor_fullname").lower() + "%")
        if request.form.get("find_doctor_specialty"):
            if first_parameter == True:
                search_string += "specialty LIKE ?"
            else:
                search_string += " AND specialty LIKE ?"
            first_parameter = False
            search_parameters.append("%" + request.form.get("find_doctor_specialty").lower() + "%")

        con = sqlite3.connect('./medical_history.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(search_string, (*search_parameters,))
        data = cur.fetchall()

        encounters = []
        if len(data) > 0:
            for i in range(len(data)):
                con = sqlite3.connect('./medical_history.db')
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM medical_encounters WHERE doctor_id = ?", (data[i]['id'],))
                encounter = cur.fetchall()
                encounters.append(encounter)
        return render_template("/found_doctors.html", data = data, encounters = encounters)
    else:
        return render_template("/find_doctor.html", doctor_id = session['user_id'])
