from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from pymysql import MySQLError
from config import info_tab, generate_id, fetch_latest_lab_test_request, send_acceptance_email
from flask_bcrypt import Bcrypt
import pymysql
import logging
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dbconfig import get_db_connection, queries


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


CORS(app)  # Enable CORS for all routes

# Set up Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Secret key for session management
app.secret_key = 'your_secret_key'  # Replace with a strong secret key in production

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
db = client['equipment_information']  # Replace with your database name
collection = db['equipment_info']  # Replace with your collection name

# Set the folder to store uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size for upload

# Allowed file extensions for uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/register_user', methods=['POST'])
def signin():
    try:
        username = request.form['username']
        email = request.form['email']
        phone_no = request.form['phone_no']
        password = request.form['password']
        role_id = request.form['role_id']
        user_id = generate_id()

        # Check if the email ends with @gsfcunivercity.ac.in
        if email.endswith('@gsfcuniversity.ac.in'):
            is_member = 1  # True
        else:
            is_member = 0  # False

        # Connect to MySQL database and insert user data
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Update the SQL query to include the 'member' column
            sql = queries['signin']
            cursor.execute(sql, (user_id, username, email, phone_no, password, role_id, is_member))  # Store plain password and membership status

        connection.commit()
        connection.close()

        flash('Registration successful!', 'success')
        return redirect(url_for('home'))

    except MySQLError as e:
        # Check if the error is a duplicate entry error
        if e.args[0] == 1062:
            flash('This email is already registered. Please use a different email.', 'danger')
        else:
            flash('An unexpected error occurred. Please try again later.', 'danger')
        return redirect(url_for('user_login'))  # Redirect to the login page

    except Exception as e:
        print(f"Error: {str(e)}")
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return redirect(url_for('user_login'))

@app.route('/user_login', methods=['POST'])
def login():
    login_input = request.form['login_input']  # This will hold email, username, or phone number
    password = request.form['login_password']

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # SQL query to fetch password, email, role_id, and username
            sql = queries['login']
            cursor.execute(sql, (login_input, login_input, login_input))
            result = cursor.fetchone()
            print(f"Query result: {result}")

        if result:
            stored_password = result['password']  # Accessing dictionary correctly
            email = result['email']  # Fetch the email
            role_id = result['role_id']
            username = result['username']  # Fetch the username

            print(f"Stored password: '{stored_password}', Input password: '{password}'")

            if stored_password == password:
                # Store the user details in session
                session['login_input'] = login_input  # Store the login input for later use
                session['email'] = email  # Store the email in session
                session['role_id'] = role_id  # Store the role ID
                session['username'] = username  # Store the username in session

                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                print("Passwords do not match.")
                flash('Invalid password.', 'danger')
                return redirect(url_for('user_login'))

        else:
            flash('No user found with this email, username, or phone number.', 'danger')
            return redirect(url_for('user_login'))

    except Exception as e:
        print(f"Error during login: {type(e).__name__}: {str(e)}")
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return redirect(url_for('user_login'))

@app.route("/")
def user_login():
    return render_template('login.html')

@app.route("/home")
def home():
    try:
        # Ensure the user is logged in by checking if the email exists in the session
        if 'email' not in session:
            flash('You need to log in to view this page.', 'danger')
            return redirect(url_for('user_login'))

        user_email = session['email']
        role_id = session.get('role_id')

        # Use the helper function to get the latest lab test request
        latest_request = fetch_latest_lab_test_request(user_email)
        print(latest_request)

        # Pass the latest_request to the home template
        return render_template('index.html', latest_request=latest_request, role_id = role_id)

    except Exception as e:
        print(f"Error: {str(e)}")
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return redirect(url_for('home'))

@app.route("/user_input_form")
def user_input_form():
    email = session.get('email')
    role_id = session.get('role_id')
    print(f"email {email}")
    return render_template('user_input_form.html', email=email, role_id = role_id)

@app.route('/add_lab_test_request', methods=['POST'])
def add_lab_test_request():
    # Capture form data
    test_name = request.form['test-name']
    equipment = request.form['equipment']
    sample_name = request.form['sample']
    sample_day = request.form['sample-day']  # Ensure date is captured correctly
    test_method = request.form['test-method']
    request_id = generate_id()
    amount = 100
    
    # Retrieve user info from the session
    user_name = session.get('username')
    user_email =session.get('email')
    role_id = session.get('role_id')

    # Check if user info is missing in the session
    if not user_name or not user_email:
        flash('You must be logged in to submit a lab test request.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if session data is missing

    # Validate if the sample day is provided
    if not sample_day:
        flash('Sample day is required.', 'danger')
        return redirect(url_for('home'))

    try:
        # Connect to the database and insert the request
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = queries['lab_test_request']
            cursor.execute(sql, (request_id, user_name, user_email, test_name, equipment, sample_name, sample_day, test_method, amount))
            connection.commit()
            flash('Lab test request submitted successfully!', 'success')
            return redirect(url_for('home'))

    except Exception as e:
        # Handle any errors that occur during the insertion process
        print(f"Error during request insertion: {type(e).__name__}: {str(e)}")
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return redirect(url_for('home'))

    finally:
        if connection:
            connection.close()


@app.route('/accept_request', methods=['POST'])
def accept_request():
    data = request.get_json()
    request_id = data.get('request_id')
    equipment = data.get('equipment')
    sample = data.get('sample')
    sample_day = data.get('sample_day')

    # Get the current user's email from session
    manager_email = session.get('email')  # Analyst email from the session

    if not manager_email:
        return jsonify({'status': 'error', 'message': 'You must be logged in to accept a request!'}), 403

    try:
        # Check if the request ID is provided
        if not request_id:
            return jsonify({'status': 'error', 'message': 'Request ID is required!'}), 400

        # Log the equipment ID being searched
        logging.info(f"Searching for equipment with name: {equipment}")

        # Fetch equipment details using the equipment ID from MongoDB
        equipment_data = db.equipments.find_one({"equipment_name": equipment})

        # Log the result of the query
        if equipment_data:
            logging.info(f"Equipment found: {equipment_data}")
        else:
            logging.warning(f"No equipment found for name: {equipment}")

        if not equipment_data:
            return jsonify({'status': 'error', 'message': 'Equipment not found!'}), 404

        # Extract manager details from the equipment data
        manager = equipment_data.get('manager')
        if not manager:
            return jsonify({'status': 'error', 'message': 'Manager not found for this equipment!'}), 404

        # Get the manager details
        manager_id = manager.get('id')  # Assuming you want the 'id' field from the manager
        manager_name = manager.get('name')
        manager_dp = manager.get('dp')

        # Update the request status to 'accepted' and store manager details
        connection = get_db_connection()  # Use the proper DB connection function
        with connection.cursor() as cursor:
            sql = queries["update_accept_request"]
            cursor.execute(sql, (manager_id, request_id))
            connection.commit()

        # Fetch user email for sending notification
        user_email = data.get('user_email')  # Pass this from the frontend when accepting the request
        if user_email:
            send_acceptance_email(user_email, equipment, sample, sample_day, manager_email)

        return jsonify({'status': 'success', 'message': 'Request accepted and email sent!'})

    except Exception as e:
        logging.error(f"Error accepting request: {str(e)}")
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500

    finally:
        # Ensure the connection is closed if it was opened
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/reject_request', methods=['POST'])
def reject_request():
    data = request.get_json()
    request_id = data.get('request_id')

    if not request_id:
        return jsonify({'status': 'error', 'message': 'Request ID is required!'}), 400

    try:
        # Update the request status to 'rejected'
        connection = get_db_connection()  # Use the proper DB connection function
        with connection.cursor() as cursor:
            sql = queries["update_reject_request"]
            cursor.execute(sql, (request_id,))
            connection.commit()

        return jsonify({'status': 'success', 'message': 'Request rejected successfully!'})

    except Exception as e:
        logging.error(f"Error rejecting request: {str(e)}")
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500

    finally:
        connection.close()

@app.route("/equipment_information")
def equipment_information():
    role_id = session.get('role_id')
    # Fetch all equipment information from MongoDB
    equipment_data = list(collection.find())  # Retrieve all documents in the collection
    return render_template('equipment_information.html', equipment_data=equipment_data, role_id=role_id)

@app.route("/inputform")
def inputform():
    role_id = session.get('role_id')
    return render_template('input_form.html', role_id = role_id)


# Route for rendering requests
@app.route('/requests')
def requests_view():

    role_id = session.get('role_id')
    # Fetch request data from the database
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql_query = queries['request_display']
            cursor.execute(sql_query)
            requests_data = cursor.fetchall()  # Fetch all the request records
    finally:
        connection.close()

    # Pass the requests_data to the template
    return render_template('requests_page.html', requests_data=requests_data, role_id = role_id)

@app.route('/submit_equipment_information', methods=['POST'])
def submit_equipment_information():
    try:
        # Retrieve form data
        equipment_name = request.form.get('equipment-name')
        equipment_id = request.form.get('equipment-id')
        manager_name = request.form.get('manager-name')
        manager_email = request.form.get('manager-email')
        manager_id = request.form.get('manager-id')
        description = request.form.get('description')

        # Get the selected equipment image and manager DP filenames
        equipment_filename = request.form.get('equipment-image')
        manager_dp_filename = request.form.get('manager-dp')

        # Get the features as a string separated by //
        features_string = request.form.get('features', '')
        features = [feature.strip() for feature in features_string.split('//') if feature.strip()]

        # Prepare document for MongoDB
        equipment_data = {
            'equipment_name': equipment_name,
            'equipment_image': equipment_filename,
            'manager': {
                'name': manager_name,
                'email': manager_email,
                'id': manager_id,
                'dp': manager_dp_filename,
            },
            'description': description,
            'features': features,
        }

        # Insert into MongoDB
        result = collection.insert_one(equipment_data)
        print("Data inserted into MongoDB successfully. ID:", result.inserted_id)
        return jsonify({"message": "Equipment data stored successfully!"}), 200

    except Exception as e:
        print("Exception occurred:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)