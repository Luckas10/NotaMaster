from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.Grade import Grade
from models.Complaint import Complaint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'discente':
        grades = Grade.query.filter_by(student_id=current_user.id).all()
        complaints = Complaint.query.filter_by(student_id=current_user.id).all()
        return render_template('dashboard.html', grades=grades, complaints=complaints)
    
    elif current_user.role == 'docente':
        complaints = Complaint.query.all()
        return render_template('dashboard.html', complaints=complaints)
