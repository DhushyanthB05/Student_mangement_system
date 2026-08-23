from app.routes.auth import admin_required
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.models import Student, Attendance, Course
from datetime import datetime

bp = Blueprint('attendance', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    courses = Course.query.all()
    selected_course = None
    date = datetime.today().date()
    students = []
    
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        date_str = request.form.get('date')
        
        if course_id:
            selected_course = Course.query.get(course_id)
            if selected_course:
                students = Student.query.filter_by(course_id=course_id).all()
        
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
        # Handle marking attendance
        if 'mark_attendance' in request.form:
            for student in students:
                status = request.form.get(f'status_{student.id}')
                if status:
                    # check if already marked
                    existing = Attendance.query.filter_by(student_id=student.id, date=date).first()
                    if existing:
                        existing.status = status
                    else:
                        att = Attendance(student_id=student.id, date=date, status=status)
                        db.session.add(att)
            db.session.commit()
            flash('Attendance marked successfully!', 'success')
            
    return render_template('attendance/index.html', courses=courses, selected_course=selected_course, date=date, students=students)

