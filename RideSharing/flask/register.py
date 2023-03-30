from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
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
app.config['SECRET_KEY'] = 'secret_key'
mysql = MySQL(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('landing.html')

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

        # Get the user from the database based on the entered email
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        # Check if user exists and the entered password matches the hashed password in the database
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['logged_in'] = True
            session['userId'] = user['userId']
            return jsonify({'redirect': url_for('profile')})
        else:
            session['logged_in'] = False
            return jsonify({'redirect': None, 'error': 'Invalid email or password. Please try again.'})


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
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name, email, phone_number FROM users WHERE userId = %s', (session['userId'],))
    user = cursor.fetchone()
    cursor.close()
    return render_template('profile.html', User=user)
    #return jsonify(name=user['name'], email=user['email'], phone_number=user['phone_number'])


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


@app.route('/book')
def bookRide():
    return render_template('book.html')


#@app.route('/editProfile')
#def editProfile():
#    return render_template('editProfile.html')



@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    # Redirect to login if user is not logged in
    if 'userId' not in session:
        return redirect('/login')

    # Connect to MariaDB
    try:
        cur = mysql.connection.cursor()
        # Get user information
        userId = int(session['userId'])
        cur.execute("SELECT * FROM users WHERE userId=%s", (userId,))
        user = cur.fetchone()

        # Handle form submission
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            print(name)
            # Update user information in database
            userId = int(session['userId'])
            cur.execute("UPDATE users SET name=%s, email=%s, phone_number=%s WHERE userId=%s", (name, email, phone_number, userId))
            mysql.connection.commit()

            # Update session information
            session['name'] = name
            session['email'] = email
            session['phone_number'] = phone_number

            # Redirect to profile page
            return redirect('/profile')

        # Close database connection and cursor
        cur.close()

        return render_template('editProfile.html', user=user)

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)



if __name__ == '__main__':
    app.run(debug=True)

