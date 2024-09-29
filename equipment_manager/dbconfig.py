from flask_bcrypt import Bcrypt
import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',  # Your MySQL username
        password='PASSWORD',  # Your MySQL password
        database='DATA_BASE_NAME',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        
)

#queries used in app.py
queries = {"login": """
                SELECT username, password, email, role_id 
                FROM user_login 
                WHERE email = %s OR username = %s OR phone_no = %s
            """,
        "signin": """INSERT INTO user_login (id, username, email, phone_no, password, role_id, member)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)""",

        "lab_test_request":"""
                INSERT INTO lab_test_requests (Request_id, UserID, Request_time, Report_day, EquipmentDI, SampleID)
                VALUES (%s, %s, NOW(), %s, %s, %s)
            """,
        
        "latest_request" :  """
                SELECT * 
                FROM lab_test_requests 
                WHERE user_email = %s
                ORDER BY Request_time DESC 
                LIMIT 1
            """,
        "request_display":  """ 
                SELECT request_id, user_email, equipment, sample, sample_day 
                FROM lab_test_requests 
                ORDER BY Request_time DESC;  
            """,
        "update_accept_request": """
                UPDATE lab_test_requests 
                SET Request_status = 'accepted', manager_id = %s
                WHERE RequestID = %s
            """,
        "update_reject_request":"""
                UPDATE lab_test_requests 
                SET Request_status = 'rejected'
                WHERE RequestID = %s
            """
}

