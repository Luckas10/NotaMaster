from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from database import Session
from models.Grade import Grade
from models.Complaint import Complaint
from models.Enrollment import Enrollment
from models.User import User
from sqlalchemy.orm import joinedload

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    session = Session()
    if current_user.role == 'discente':
        grades = (session.query(Grade)
                .options(joinedload(Grade.subject))
                .filter_by(student_id=current_user.id)
                .all())
        complaints = session.query(Complaint).filter_by(student_id=current_user.id).all()
        session.close()
        return render_template('dashboard.html', grades=grades, complaints=complaints)

    elif current_user.role == 'docente':
        complaints = (session.query(Complaint)
                    .options(
                        joinedload(Complaint.student),
                        joinedload(Complaint.grade)
                    )
                    .all())
        session.close()
        return render_template('dashboard.html', complaints=complaints)


@dashboard_bp.route('/student/bulletin')
@login_required
def student_bulletin():
    if current_user.role != 'discente':
        flash('Apenas discentes podem ver esta página.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    session = Session()

    # Carrega matriculas + student + subject + grades
    enrollments = (session.query(Enrollment)
                   .options(
                       joinedload(Enrollment.student).joinedload(User.grades),
                       joinedload(Enrollment.subject)
                   )
                   .filter_by(student_id=current_user.id)
                   .all())
    session.close()

    return render_template('complete_bulletin.html', enrollments=enrollments)

