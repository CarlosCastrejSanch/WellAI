from app import app, db
from flask import render_template, request,redirect,url_for,flash
from ..models.user import User,EmployeeList
from werkzeug.security import generate_password_hash
import uuid

@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("El usuario ya se encuentra registrado", category="error")
            
        else:
            user_from_email_list  = EmployeeList.query.filter_by(email=email).first()
            if not user_from_email_list:
                flash("Por favor, contacta con tu administrador para que te de acceso a la plataforma", category="error")
                return redirect(url_for("register"))
            is_doctor = False
            if user_from_email_list:
                if user_from_email_list.is_doctor:
                    is_doctor = True
                role = user_from_email_list.role
                gender = user_from_email_list.gender
                new_user = User(username=username, email=email, password=generate_password_hash(password), is_doctor=is_doctor,is_employee=not is_doctor,role=role,gender=gender, is_active=True)
                db.session.add(new_user)
                db.session.commit()
                flash("Cuenta creada", category="success")
                return redirect(url_for("login"))
    return render_template('register.html')