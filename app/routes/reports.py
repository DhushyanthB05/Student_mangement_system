from flask import Blueprint, make_response
from flask_login import login_required
from app.models.models import Student
import csv
from io import StringIO

bp = Blueprint('reports', __name__)

@bp.route('/students.csv')
@login_required
def export_students():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Roll No', 'Name', 'Age', 'Course', 'Marks', 'Grade'])
    
    students = Student.query.all()
    for s in students:
        course_name = s.enrolled_course.name if s.enrolled_course else 'N/A'
        marks = s.academic_record.marks if s.academic_record else ''
        grade = s.academic_record.grade if s.academic_record else ''
        cw.writerow([s.roll_no, s.name, s.age, course_name, marks, grade])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=students_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output
