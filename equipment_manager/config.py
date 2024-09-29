import random
import string
from pymysql.err import MySQLError
from dbconfig import get_db_connection, queries
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_id():
    # Generate 3 random alphabetic characters
    letters = ''.join(random.choices(string.ascii_letters, k=3))
    # Generate 3 random numeric characters
    digits = ''.join(random.choices(string.digits, k=3))
    # Combine letters and digits
    unique_id = letters + digits
    return unique_id

# Example usage
generated_id = generate_id()
print("Generated ID:", generated_id)

info_tab = {
    "Equipment 1":"John Deo",
    "Equipment 2":"Adam Seladin",
    "Equipment 3":"James Chris"
}

def external_charges(amount):
    per_amount = (30 / 100) * amount + amount
    return round(per_amount)


    
def fetch_latest_lab_test_request(email):
    """
    Fetch the latest lab test request for the given email.

    :param email: The email of the user whose latest lab test request is to be fetched.
    :return: The latest lab test request record as a dictionary or None if no request is found.
    """
    try:
        # Connect to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Fetch the latest lab_test_request for the given email
            query = queries['latest_request']
            cursor.execute(query, (email,))
            latest_request = cursor.fetchone()

        connection.close()

        # Return the latest request or None if not found
        return latest_request if latest_request else None

    except MySQLError as e:
        print(f"Database error: {str(e)}")
        return None

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def send_acceptance_email(user_email, equipment, sample, sample_day, analyst_email):
    try:
        # Email content
        subject = "Request Accepted: Equipment and Sample Details"
        body = f"""
        Dear User,

        Your request for the following equipment and sample has been accepted:

        Equipment: {equipment}
        Sample: {sample}
        Expected Report Date: {sample_day}

        If you have any queries, feel free to contact your assigned analyst: {analyst_email}.

        Regards,
        Laboratory Management Team
        """

        # Email setup
        sender_email = "yourlab@example.com"  # Sender's email
        sender_password = "yourpassword"  # Sender's email password (use environment variables in production)

        # MIMEText object for the email body
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Sending the email using SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()

        print(f"Email sent to {user_email}")

    except Exception as e:
        print(f"Error sending email: {str(e)}")