from app import app
from flask import render_template,jsonify, request, abort,make_response,redirect,url_for
from werkzeug.security import  check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.user import User
from flask import flash

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Te has logueado correctamente", category="success")
                return redirect(url_for("home"))
            else:
                flash("Contraseña incorrecta", category="error")
        else:
            flash("El usuario no existe", category="error")
    return render_template('login.html')

@app.route('/logout')
@login_required # cannot access this unless user is already logged in
def logout():
    logout_user()
    return redirect(url_for('home'))