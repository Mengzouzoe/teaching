from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length

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