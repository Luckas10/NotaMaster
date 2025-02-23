from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import Session
from models.User import User
from models.Subject import Subject
from models.Grade import Grade
from flask_login import login_required, current_user

add_grades_bp = Blueprint('add_grades', __name__)

@add_grades_bp.route('/add_grade', methods=['GET', 'POST'])
@login_required
def add_grade():
    if current_user.role != 'docente':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    session = Session()

    # Carregar todos os discentes
    students = session.query(User).filter_by(role='discente').all()
    # Carregar todas as disciplinas
    subjects = session.query(Subject).all()

    if request.method == 'POST':
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        grade_value = request.form['grade']

        if not student_id or not subject_id or not grade_value:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('add_grades.add_grade'))

        new_grade = Grade(student_id=student_id, subject_id=subject_id, grade=float(grade_value))
        session.add(new_grade)
        session.commit()

        flash('Nota adicionada com sucesso!', 'success')
        return redirect(url_for('add_grades.add_grade'))

    return render_template('add_grade.html', students=students, subjects=subjects)
