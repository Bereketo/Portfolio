from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import bcrypt
import mariadb
from mysql.connector import Error
from mariadb import Error


app = Flask(__name__, static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'ride_sharing_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('register.html')

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
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (name, email, phone_number, password) VALUES (%s, %s, %s, %s)',
                       (name, email, phone_number, password_hash))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
    return render_template('login.html')

    # if True:
    #    return jsonify({'success': True, 'user': user})
    # else:
    #    return jsonify({'success': False, 'message': 'Invalid email or password.'})
    """     if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return redirect(url_for('profile'))
        else:
            error = 'Invalid login credentials'
            return render_template('login.html', error=error)
    return render_template('login.html')
    """

@app.route('/profile')
def profile():
    user = request.args.get('user')
    if user:
        # Parse the user's data from the URL query string
        # and render the profile page with the data
        return render_template('profile.html', user=user)
    else:
        # Redirect to the login page if the user's data is not provided
        return redirect('/')

@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    user_id = session.get('id')
    cursor = mysql.connection.cursor()
    email = request.form['email']
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    print(user)
    if user:
        user_data = {
            'name': user['name'],
            'email': user['email'],
            'phone_number': user['phone_number'],
            'profile_pic': user['profile_pic']
        }
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'})


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        profile_pic = request.form['profile_pic']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE users SET name = %s, email = %s, phone_number = %s, profile_pic = %s WHERE id = %s',
                       (name, email, phone_number, profile_pic, 1))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('profile'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT name, email, phone_number, profile_pic FROM users WHERE id = %s', (1,))
        user = cursor.fetchone()
        return render_template('edit_profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)

