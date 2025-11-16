from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, uuid, subprocess, re

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB = "users.db"
WORKDIR = os.path.join(os.getcwd(), "temp")
os.makedirs(WORKDIR, exist_ok=True)

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT UNIQUE,
                       password TEXT)''')
    conn.commit()
    conn.close()
init_db()

# Cleanup function
def cleanup(files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)

# Default route redirect to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Registration route
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "danger")
    return render_template("register.html")

# Login route
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row and check_password_hash(row[0], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template("login.html")

# Dashboard (Compiler)
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    output = ''
    code = ''
    if request.method == "POST":
        code = request.form['code']
        lang = request.form['lang']
        uid = str(uuid.uuid4())[:8]

        if lang == 'java':
            match = re.search(r'class\s+(\w+)', code)
            classname = match.group(1) if match else 'Main'
            src = os.path.join(WORKDIR, f'{uid}_{classname}.java')
            with open(src, 'w') as f:
                f.write(code)
            try:
                compile_proc = subprocess.run(['javac', src], capture_output=True, text=True, timeout=10)
                if compile_proc.returncode != 0:
                    output = compile_proc.stderr
                else:
                    run_proc = subprocess.run(['java', '-cp', WORKDIR, f'{uid}_{classname}'], capture_output=True, text=True, timeout=5)
                    output = run_proc.stdout + run_proc.stderr
            except subprocess.TimeoutExpired:
                output = "Timeout (compilation/run)"
            finally:
                cleanup([src, os.path.join(WORKDIR, f'{uid}_{classname}.class')])

        elif lang == 'python':
            src = os.path.join(WORKDIR, f'{uid}_script.py')
            with open(src, 'w') as f:
                f.write(code)
            try:
                run_proc = subprocess.run(['python', src], capture_output=True, text=True, timeout=5)
                output = run_proc.stdout + run_proc.stderr
            except subprocess.TimeoutExpired:
                output = "Timeout (run)"
            finally:
                cleanup([src])

    return render_template("dashboard.html", username=session['username'], code=code, output=output)

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

