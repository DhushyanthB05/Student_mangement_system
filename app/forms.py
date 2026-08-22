from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Department Code', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Save Department')

class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Course Code', validators=[DataRequired(), Length(max=20)])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Course')

class StudentForm(FlaskForm):
    roll_no = StringField('Roll Number', validators=[DataRequired(), Length(max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=10, max=100)])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    marks = IntegerField('Marks (0-100)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Save Student')
