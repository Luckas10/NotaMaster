from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import Session
from models.Grade import Grade
from models.Complaint import Complaint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    session = Session()

    if current_user.role == 'discente':
        grades = session.query(Grade).filter_by(student_id=current_user.id).all()
        complaints = session.query(Complaint).filter_by(student_id=current_user.id).all()
        return render_template('dashboard.html', grades=grades, complaints=complaints)
    
    elif current_user.role == 'docente':
        complaints = session.query(Complaint).all()
        return render_template('dashboard.html', complaints=complaints)
