import sqlite3
import datetime
from werkzeug.security import generate_password_hash
import random
import secrets
import uuid
import string

connection = sqlite3.connect('app/database.sqlite')
cur = connection.cursor()

roles = ["Programmer","Analyst","Director","Accountant","Recepcionist"]
genders = ["Male","Female"]

# Insert a new corporation user to the user table
is_corp= True
is_doctor = False
is_employee = False
email = "corp3@example.com"
username = "corp3"
role= "Corporation"
gender= (secrets.choice(genders))
cur.execute("INSERT OR IGNORE INTO 'user' (username,email,password,is_active,is_corp,is_doctor,is_employee,role,gender,doctor_access) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (f"{username}",f"{email}",generate_password_hash('123456'), True ,is_corp, is_doctor, is_employee,role,gender, False)
            )



connection.commit()


connection.commit()
connection.close()