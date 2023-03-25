from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors
import bcrypt

app = Flask(__name__ , static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'ride_sharing_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                             user=app.config['MYSQL_USER'],
                             password=app.config['MYSQL_PASSWORD'],
                             db=app.config['MYSQL_DB'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', [email])
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password, user['password']):
            session['name'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('profile'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return render_template('profile.html', user=user)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        confirm_password = request.form['confirm_password']
        confirm_password_hash = bcrypt.hashpw(confirm_password.encode('utf-8'), bcrypt.gensalt())
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO users (name, email, phone_number, password) VALUES (%s, %s, %s, %s)',
                           (name, email, phone_number, password_hash))
            connection.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

