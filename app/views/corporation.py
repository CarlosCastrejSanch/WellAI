from app import app,db
from flask import render_template, request
from flask_login import current_user, login_required
from ..models import EmployeeList

@app.route("/corporation", methods = ['GET','POST'])
@login_required
def corporation():
    employee_list = EmployeeList.query.filter_by(corp_id=current_user.id).all()
    return render_template("corporation.html", user=current_user,employee_list=employee_list)


@app.route("/add_email_to_list", methods = ['GET','POST'])
def add_email_to_list():
    email = request.args.get("email")
    name = request.args.get("name")
    role = request.args.get("role")
    gender = request.args.get("gender")
    is_doctor = request.args.get("is_doctor")
    if is_doctor == "Doctor" or is_doctor == "doctor":
        is_doctor = True
    else:
        is_doctor = False
    new_employee = EmployeeList(email=email, name=name, role=role, gender=gender, is_doctor=is_doctor,corp_id=current_user.id)
    db.session.add(new_employee)
    db.session.commit()
    employee_list = EmployeeList.query.filter_by(corp_id=current_user.id).all()
    return render_template("update_employee_email_list.html", user=current_user,employee_list=employee_list)




@app.route("/delete_email", methods = ['GET','POST'])
def delete_email():
    id = request.args.get("id")
    EmployeeList.query.filter_by(id=id).delete()
    db.session.commit()
    employee_list = EmployeeList.query.filter_by(corp_id=current_user.id).all()
    return render_template("update_employee_email_list.html", user=current_user,employee_list=employee_list)