from . import db

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