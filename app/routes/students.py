from app.routes.auth import admin_required
import csv
from io import StringIO
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.models import Student, AcademicRecord, Course
from app.forms import StudentForm
from app.services.grade_service import calculate_grade
from app.services.audit_service import log_action

bp = Blueprint('students', __name__)

@bp.route('/')
@login_required
@admin_required
def list_students():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    
    query = Student.query
    if q:
        query = query.filter(
            (Student.name.ilike(f'%{q}%')) | 
            (Student.roll_no.ilike(f'%{q}%'))
        )
        
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    return render_template('students/list.html', pagination=pagination, q=q)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    form = StudentForm()
    # Populate course choices
    form.course_id.choices = [(c.id, f"{c.code} - {c.name}") for c in Course.query.all()]
    
    if form.validate_on_submit():
        if Student.query.filter_by(roll_no=form.roll_no.data).first():
            flash('Student with this Roll Number already exists.', 'danger')
            return render_template('students/add.html', form=form)

        student = Student(
            roll_no=form.roll_no.data,
            name=form.name.data,
            age=form.age.data,
            course_id=form.course_id.data
        )
        db.session.add(student)
        db.session.commit()

        marks = form.marks.data
        grade = calculate_grade(marks)
        record = AcademicRecord(student_id=student.id, marks=marks, grade=grade)
        
        db.session.add(record)
        db.session.commit()

        log_action(f'Added student {student.name} ({student.roll_no})')
        flash('Student added successfully!', 'success')
        return redirect(url_for('students.list_students'))
        
    return render_template('students/add.html', form=form)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    form.course_id.choices = [(c.id, f"{c.code} - {c.name}") for c in Course.query.all()]
    
    if request.method == 'GET' and student.academic_record:
        form.marks.data = student.academic_record.marks

    if form.validate_on_submit():
        existing = Student.query.filter_by(roll_no=form.roll_no.data).first()
        if existing and existing.id != student.id:
            flash('Roll Number already assigned to another student.', 'danger')
            return render_template('students/edit.html', form=form, student=student)

        student.roll_no = form.roll_no.data
        student.name = form.name.data
        student.age = form.age.data
        student.course_id = form.course_id.data
        
        if student.academic_record:
            student.academic_record.marks = form.marks.data
            student.academic_record.grade = calculate_grade(form.marks.data)
            
        db.session.commit()
        log_action(f'Updated student {student.name} ({student.roll_no})')
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/edit.html', form=form, student=student)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    log_action(f'Deleted student {student.name} ({student.roll_no})')
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students.list_students'))

@bp.route('/<int:id>/profile')
@login_required
def student_profile(id):
    student = Student.query.get_or_404(id)
    return render_template('students/profile.html', student=student)



@bp.route('/import', methods=['POST'])
@login_required
@admin_required
def import_students():
    if 'csv_file' not in request.files:
        flash('No file uploaded.', 'danger')
        return redirect(url_for('students.list_students'))
        
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('students.list_students'))
        
    if file and file.filename.endswith('.csv'):
        try:
            stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            next(csv_input) # Skip header
            
            count = 0
            for row in csv_input:
                if len(row) >= 5:
                    roll_no, name, age, course_code, marks = row[:5]
                    
                    # Skip if student exists
                    if Student.query.filter_by(roll_no=roll_no).first():
                        continue
                        
                    # Find or create course if needed (simplified: just find)
                    course = Course.query.filter_by(code=course_code).first()
                    course_id = course.id if course else None
                    
                    student = Student(roll_no=roll_no, name=name, age=int(age), course_id=course_id)
                    db.session.add(student)
                    db.session.commit()
                    
                    m = int(marks)
                    g = calculate_grade(m)
                    record = AcademicRecord(student_id=student.id, marks=m, grade=g)
                    db.session.add(record)
                    count += 1
            
            db.session.commit()
            log_action(f'Bulk imported {count} students via CSV')
            flash(f'Successfully imported {count} students!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error importing CSV: {str(e)}', 'danger')
    else:
        flash('Invalid file format. Please upload a CSV.', 'danger')
        
    return redirect(url_for('students.list_students'))


