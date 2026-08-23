from app.routes.auth import admin_required
from flask import Blueprint, render_template
from flask_login import login_required
from app.extensions import db
from app.models.models import Student, Course, Department, AcademicRecord, Attendance, AuditLog

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
@admin_required
def index():
    student_count = Student.query.count()
    course_count = Course.query.count()
    dept_count = Department.query.count()
    
    # Calculate Average Attendance
    total_att = Attendance.query.count()
    present_att = Attendance.query.filter_by(status='Present').count()
    avg_attendance = round((present_att / total_att * 100)) if total_att > 0 else 0
    
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(7).all()
    
    departments = Department.query.all()
    dept_labels = [d.code for d in departments]
    dept_data = [
        Student.query.join(Course).filter(Course.department_id == d.id).count() 
        for d in departments
    ]
    
    grades = db.session.query(AcademicRecord.grade, db.func.count(AcademicRecord.id)).group_by(AcademicRecord.grade).all()
    grade_labels = [g[0] for g in grades]
    grade_data = [g[1] for g in grades]
    
    return render_template('dashboard/index.html', 
        student_count=student_count, 
        course_count=course_count, 
        dept_count=dept_count,
        avg_attendance=avg_attendance,
        recent_logs=recent_logs,
        dept_labels=dept_labels,
        dept_data=dept_data,
        grade_labels=grade_labels,
        grade_data=grade_data
    )



