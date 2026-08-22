from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.models import Student, AcademicRecord, Course
from app.forms import StudentForm
from app.services.grade_service import calculate_grade

bp = Blueprint('students', __name__)

@bp.route('/')
@login_required
def list_students():
    students = Student.query.all()
    return render_template('students/list.html', students=students)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
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

        flash('Student added successfully!', 'success')
        return redirect(url_for('students.list_students'))
        
    return render_template('students/add.html', form=form)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
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
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('students/edit.html', form=form, student=student)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students.list_students'))

@bp.route('/<int:id>/profile')
@login_required
def student_profile(id):
    student = Student.query.get_or_404(id)
    return render_template('students/profile.html', student=student)
