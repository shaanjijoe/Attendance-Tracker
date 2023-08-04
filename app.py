from checkup import check_database
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from createtable import setuptable
import period

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route for the login page
@app.route('/')
def login():
    return render_template('login.html')

# Route for the register page
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# Route to handle registration form submission
@app.route('/register', methods=['POST'])
def register_submit():
    username = request.form['username']
    password = request.form['password']

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Username already exists, show an alert and reset the page
        return "<script>alert('Username already exists. Please choose a different username.'); location.href='/register';</script>"

    # Insert the new user into the database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect to the login page after successful registration
    return redirect(url_for('login'))


# Route to handle login form submission and authenticate the user
@app.route('/login', methods=['POST'])
def login_submit():
    check_database()
    username = request.form['username']
    password = request.form['password']

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the username and password match
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    # Close the database connection
    cursor.close()
    conn.close()

    if user is not None:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        # Authentication failed, show an error message
        return 'Invalid username or password'



# Route for the home page (requires authentication)
@app.route('/home')
@login_required
def home():
    username = session['username']

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch the user's data field from the users table
    cursor.execute("SELECT data FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    if user_data is None or user_data[0] is None:
        user_data = []
    else:
        user_data = eval(user_data[0])

    # Close the database connection
    cursor.close()
    conn.close()

    return render_template('home.html', username=username, user_data=user_data)



# Route to handle the creation of a new table (requires authentication)
@app.route('/create_table', methods=['POST'])
@login_required
def create_table():
    activity_name = request.form['activity_name']
    username = request.form['username']
    # Code to create a new table (activity) in the database
    # ...
    res=setuptable(username+"$"+activity_name)
    if res:
        # Table creation was successful

        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Fetch the user's current data field
        cursor.execute("SELECT data FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()[0]
        
        # Update the user's data field with the new table name
        if user_data is None:
            user_data = [activity_name]
        else:
            user_data = eval(user_data)
            user_data.append(activity_name)
        
        # Convert the table names list to a string
        # updated_data = ' '.join(user_data)
        updated_data=str(user_data)
        
        # Update the data field in the users table
        cursor.execute("UPDATE users SET data = ? WHERE username = ?", (updated_data, username))
        conn.commit()
        
        # Close the database connection
        cursor.close()
        conn.close()




        response = {'success': True, 'message': 'New table (activity) created: {}'.format(activity_name)}
    else:
        # Table creation failed
        response = {'success': False, 'message': 'Table creation failed.'}

    return jsonify(response)




# Route to display table contents
@app.route('/table/<username>/<table_name>')
@login_required
def display_table(username, table_name):
    # Code to fetch and display the contents of the selected table
    # ...
    dictionary_data=period.getallperiod(username+'$'+table_name)
    print(dictionary_data)
    
    return render_template('table.html', table_name=table_name, dictionary_data=dictionary_data,user_name=username)



# Route to handle adding a period (requires authentication)
@app.route('/add_period', methods=['POST'])
@login_required
def add_period():
    day = request.form['day']
    period_name = request.form['period_name']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    username = request.form['user_name']
    table_name = request.form['table_name']
    print(day,period_name,start_time,end_time,username,table_name)
    # Code to add the period for the selected day to the database
    # ...
    username=username.strip()
    table_name=table_name.strip()
    dat=username+'$'+table_name
    print(dat)
    outp=period.insertperiod(username+'$'+table_name, day,[start_time,end_time,period_name])

    # After adding the period, you can redirect to the table page or return a response
    # For example:
    if(outp==True):
        return jsonify({'success': True, 'message': 'Period added successfully'})
    else:
        return jsonify({'success': False, 'message': 'Error'})



if __name__ == '__main__':
    # app.run(debug=True, port=8001)
    app.run()
