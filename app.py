from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# ================= DATABASE =================
def db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ================= INIT DATABASE =================
def init_db():
    conn = db()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    );

    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        gender TEXT,
        phone TEXT
    );

    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT,
        schedule TEXT
    );

    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        doctor_id TEXT,
        date TEXT,
        time TEXT
    );

    CREATE TABLE IF NOT EXISTS billing(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        amount TEXT,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS medicines(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        stock TEXT,
        price TEXT
    );

    CREATE TABLE IF NOT EXISTS lab_reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        report TEXT
    );
    """)

    # ✅ AUTO CREATE ADMIN (NO DUPLICATE)
    user = cur.execute("SELECT * FROM users WHERE username='admin'").fetchone()
    if not user:
        cur.execute("INSERT INTO users (username,password,role) VALUES ('admin','admin123','Admin')")

    conn.commit()
    conn.close()

# ================= LOGIN =================
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        user = db().execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()

        if user:
            session['user'] = u
            return redirect('/dashboard')
        else:
            flash("Invalid Username or Password")

    return render_template('login.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    conn = db()
    p = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    d = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    a = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]

    return render_template('dashboard.html', p=p, d=d, a=a)

# ================= PATIENT =================
@app.route('/patients')
def patients():
    data = db().execute("SELECT * FROM patients").fetchall()
    return render_template('patients.html', data=data)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    f = request.form
    conn = db()
    conn.execute(
        "INSERT INTO patients(name, age, gender, phone) VALUES(?,?,?,?)",
        (f['name'], f['age'], f['gender'], f['phone'])
    )
    conn.commit()
    return redirect('/patients')

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    conn = db()
    conn.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    return redirect('/patients')

# ================= DOCTOR =================
@app.route('/doctors')
def doctors():
    data = db().execute("SELECT * FROM doctors").fetchall()
    return render_template('doctors.html', data=data)

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    f = request.form
    conn = db()
    conn.execute(
        "INSERT INTO doctors(name, specialization, schedule) VALUES(?,?,?)",
        (f['name'], f['specialization'], f['schedule'])
    )
    conn.commit()
    return redirect('/doctors')

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    conn = db()
    conn.execute("DELETE FROM doctors WHERE id=?", (id,))
    conn.commit()
    return redirect('/doctors')

# ================= APPOINTMENT =================
@app.route('/appointments')
def appointments():
    data = db().execute("SELECT * FROM appointments").fetchall()
    return render_template('appointments.html', data=data)

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    f = request.form
    conn = db()
    conn.execute(
        "INSERT INTO appointments(patient_id, doctor_id, date, time) VALUES(?,?,?,?)",
        (f['patient_id'], f['doctor_id'], f['date'], f['time'])
    )
    conn.commit()
    return redirect('/appointments')

@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    conn = db()
    conn.execute("DELETE FROM appointments WHERE id=?", (id,))
    conn.commit()
    return redirect('/appointments')

# ================= BILLING =================
@app.route('/billing')
def billing():
    data = db().execute("SELECT * FROM billing").fetchall()
    return render_template('billing.html', data=data)

@app.route('/add_bill', methods=['POST'])
def add_bill():
    f = request.form
    conn = db()
    conn.execute(
        "INSERT INTO billing(patient_id, amount, status) VALUES(?,?,?)",
        (f['patient_id'], f['amount'], f['status'])
    )
    conn.commit()
    return redirect('/billing')

@app.route('/delete_bill/<int:id>')
def delete_bill(id):
    conn = db()
    conn.execute("DELETE FROM billing WHERE id=?", (id,))
    conn.commit()
    return redirect('/billing')

# ================= PHARMACY =================
@app.route('/pharmacy')
def pharmacy():
    data = db().execute("SELECT * FROM medicines").fetchall()
    return render_template('pharmacy.html', data=data)

@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    f = request.form
    conn = db()
    conn.execute(
        "INSERT INTO medicines(name, stock, price) VALUES(?,?,?)",
        (f['name'], f['stock'], f['price'])
    )
    conn.commit()
    return redirect('/pharmacy')

@app.route('/delete_medicine/<int:id>')
def delete_medicine(id):
    conn = db()
    conn.execute("DELETE FROM medicines WHERE id=?", (id,))
    conn.commit()
    return redirect('/pharmacy')

# ================= LAB =================
@app.route('/lab')
def lab():
    data = db().execute("SELECT * FROM lab_reports").fetchall()
    return render_template('lab.html', data=data)

@app.route('/add_report', methods=['POST'])
def add_report():
    f = request.form
    conn = db()
    conn.execute(
        "INSERT INTO lab_reports(patient_id, report) VALUES(?,?)",
        (f['patient_id'], f['report'])
    )
    conn.commit()
    return redirect('/lab')

@app.route('/delete_report/<int:id>')
def delete_report(id):
    conn = db()
    conn.execute("DELETE FROM lab_reports WHERE id=?", (id,))
    conn.commit()
    return redirect('/lab')

# ================= RUN =================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)