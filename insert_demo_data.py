import sqlite3
import datetime
from werkzeug.security import generate_password_hash
import random
import secrets
import uuid
import string

connection = sqlite3.connect('app/database.sqlite')
cur = connection.cursor()

def generate_email(name):
    return f"{name}@example.com"

roles = ["Programmer","Analyst","Director","Accountant","Recepcionist"]
genders = ["Male","Female"]

# Insert 2 corporation users to the user table
for i in range(1,3):
    is_corp= True
    is_doctor = False
    is_employee = False
    email = generate_email(f"corp{i}")
    username = f"corp{i}"
    role= "Corporation"
    gender= (secrets.choice(genders))
    cur.execute("INSERT OR IGNORE INTO 'user' (username,email,password,is_active,is_corp,is_doctor,is_employee,role,gender,doctor_access) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f"{username}",f"{email}",generate_password_hash('123456'), True ,is_corp, is_doctor, is_employee,role,gender, False)
                )

    # Insert 1 doctor user to the user table and employee_list for each corporation
    is_corp= False
    is_doctor = True
    is_employee = False
    email = generate_email(f"doctor_for_corp{i}")
    username = f"doctor_for_corp{i}"
    role= "Doctor"
    gender= (secrets.choice(genders))
    cur.execute("INSERT OR IGNORE INTO 'user' (username,email,password,is_active,is_corp,is_doctor,is_employee,role,gender,doctor_access) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f"{username}",f"{email}",generate_password_hash('123456'), True ,is_corp, is_doctor, is_employee,role,gender, False)
                )
    cur.execute("INSERT OR IGNORE INTO 'employee_list' (email,name,role,gender,is_doctor,corp_id) VALUES ( ?, ?, ?, ?, ?, ?)",
            (f"{email}",f"{username}", role ,gender, is_doctor,i)
            )    

    # Insert 4 employee users to the user table and employee_list for each corporation
    for j in range(1,5):
        is_corp= False
        is_doctor = False
        is_employee = True
        email = generate_email(f"employee{j}_for_corp{i}")
        username = f"employee{j}_for_corp{i}"
        role= (secrets.choice(roles))
        gender= (secrets.choice(genders))
        cur.execute("INSERT OR IGNORE INTO 'user' (username,email,password,is_active,is_corp,is_doctor,is_employee,role,gender,doctor_access) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (f"{username}",f"{email}",generate_password_hash('123456'), True ,is_corp, is_doctor, is_employee,role,gender, False)
                    )
        cur.execute("INSERT OR IGNORE INTO 'employee_list' (email,name,role,gender,is_doctor,corp_id) VALUES ( ?, ?, ?, ?, ?, ?)",
                (f"{email}",f"{username}", role ,gender, is_doctor,i)
                )     

# insert 1  questionnaire,
cur.execute("INSERT OR IGNORE INTO questionnaire (title) VALUES (?)",
        ("Questionnaire 1",)
        )

# list of questions categorized by their respective categories
questions = {
    'Agotamiento': [
        'En mi trabajo, me siento agotado mentalmente',
        'Al final del día de trabajo, me resultado dificil recuperar mi energía',
        'Me siento fisicamente agotado en mi trabaho'
    ],
    'Distancia mental': [
        'Me esfuerzo por encontrar entusiasmo en mi trabajo',
        'Siento una fuerte aversion hacia mi trabajo',
        'Soy cinico sobre lo que mi trabajo significa para los demas'
    ],
    'Deterioro cognitivo': [
        'Tengo problemas para mantenerme enfocado en mi trabajo',
        'Cuando estoy trabajando, tengo dificultades para concentrarme',
        'Cometo errores en mi trabajo, porque tengo mi mente en otras cosas'
    ],
    'Deterioro emocional': [
        'En mi trabajo, me siento incapaz de controlar mis emociones',
        'No me reconozco en la forma que reacciono en el trabajo',
        'Puedo reaccionar exageradamente sin querer'
    ]
}

# Insert each question with its respective category into the database
for category, question_list in questions.items():
    for question in question_list:
        cur.execute(
            "INSERT OR IGNORE INTO question (text, category, questionnaire_id) VALUES (?, ?, ?)",
            (question, category, 1)
        )


connection.commit()
connection.close()
