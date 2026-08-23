from app.routes.auth import admin_required
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.models import Course, Department
from app.forms import CourseForm, DepartmentForm

bp = Blueprint('courses', __name__)

@bp.route('/')
@login_required
@admin_required
def list_courses():
    courses = Course.query.all()
    departments = Department.query.all()
    return render_template('courses/list.html', courses=courses, departments=departments)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_course():
    form = CourseForm()
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if form.validate_on_submit():
        if Course.query.filter_by(code=form.code.data).first():
            flash('Course with this Code already exists.', 'danger')
            return render_template('courses/add_course.html', form=form)

        course = Course(
            name=form.name.data,
            code=form.code.data,
            department_id=form.department_id.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses.list_courses'))
        
    return render_template('courses/add_course.html', form=form)

@bp.route('/departments/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        if Department.query.filter_by(code=form.code.data).first():
            flash('Department with this Code already exists.', 'danger')
            return render_template('courses/add_department.html', form=form)

        dept = Department(name=form.name.data, code=form.code.data)
        db.session.add(dept)
        db.session.commit()
        flash('Department added successfully!', 'success')
        return redirect(url_for('courses.list_courses'))
        
    return render_template('courses/add_department.html', form=form)

