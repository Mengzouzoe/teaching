from flask import Flask, render_template
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:password@127.0.0.1/teaching'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
manager = Manager(app)
bootsrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    studentname = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.String(50), db.ForeignKey('classes.id'), nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.studentname

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.String(50), primary_key=True)
    classname = db.Column(db.String(6), nullable=False)
    students = db.relationship('Student', backref='Class', lazy="dynamic")

    def __repr__(self):
        return '<Class %r>' % self.classname

class RegisterForm(FlaskForm):
    student_id = StringField('student_id', validators=[InputRequired(), Length(min=11, max=20)])
    studentname = StringField('studentname', validators=[InputRequired(), Length(min=4, max=20)])
    class_id = StringField('class_id', validators=[InputRequired(), Length(min=4, max=12)])

class SearchForm(FlaskForm):    
    student_id = StringField('student_id')
    studentname = StringField('studentname')
    class_id = StringField('class_id')
    classname = StringField('classname')
    #search = SubmitField('Search')

def make_shell_context():
    return dict(app=app, db=db, Student=Student, Class=Class)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_student = Student(student_id=form.student_id.data, studentname=form.studentname.data, class_id=form.class_id.data)
        db.session.add(new_student)
        db.session.commit()

        return 'New Student has been registered'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    
    return render_template('register.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
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

@app.route('/dashboard', methods=['GET', 'POST'])
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
