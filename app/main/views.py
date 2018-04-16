from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import RegisterForm, SearchForm
from .. import db
from ..models import Student, Class

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_student = Student(student_id=form.student_id.data, studentname=form.studentname.data, class_id=form.class_id.data)
        db.session.add(new_student)
        db.session.commit()

        return 'New Student has been registered'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    
    return render_template('register.html', form=form)

@main.route('/delete', methods=['GET', 'POST'])
def Delete():
    form = SearchForm()

    if form.validate_on_submit():

        students = db.session.query(Student, Class).filter(Student.class_id == Class.id)
        if form.student_id.data:
            students = students.filter(Student.student_id == form.student_id.data)
        if form.studentname.data:
            students = students.filter(Student.studentname == form.studentname.data)
        if form.class_id.data:
            students = students.filter(Student.class_id == form.class_id.data)
        students = students.all()

        #For delete a list of Objects in sqlalchemy
        for o in students:
            db.session.delete(o[0])
        db.session.commit()

        return "<h2> Student has been deleted </h2>" 

    return render_template('delete.html', form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
def Dashboard():
    form = SearchForm()

    #for test
    #return '<h1>Hello World!</h1>' 
    if form.validate_on_submit():

        # For Allow not fill every signle form value blank.
        '''if form.student_id.data:
            students_id = db.session.filter(Student.class_id)
        elif form.studentname:
            students_name = '''
        #Don't konw to Specified the attribute in ORM
        ''' 
        students= db.session.query(Student, Class).filter(Student.class_id == Class.id)\
        .filter(Student.student_id == form.student_id.data)\
        .filter(Student.studentname == form.studentname.data)\
        .filter(Student.class_id == form.class_id.data).all()'''

        students = db.session.query(Student, Class).filter(Student.class_id == Class.id)
        if form.student_id.data:
            students = students.filter(Student.student_id == form.student_id.data)
        if form.studentname.data:
            students = students.filter(Student.studentname == form.studentname.data)
        if form.class_id.data:
            students = students.filter(Student.class_id == form.class_id.data)
        students = students.all()
        
        return render_template('display.html', students=students)
        #return '<h1>' + form.student_id.data + ' ' + form.studentname.data + ' ' + form.class_id.data + ' ' + form.classname.data + '</h1>'

    return render_template('dashboard.html', form=form)