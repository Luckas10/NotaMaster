from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import Session
from models.Subject import Subject
from models.User import User
from models.Enrollment import Enrollment
from models.Grade import Grade
from sqlalchemy.orm import joinedload

subject_bp = Blueprint('subject', __name__)

@subject_bp.route('/subjects')
@login_required
def list_subjects():
    """Lista todas as disciplinas (para aluno ou professor)."""
    session = Session()
    subjects = session.query(Subject).all()
    session.close()
    return render_template('subjects_list.html', subjects=subjects)

@subject_bp.route('/subject/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    """Adicionar uma nova disciplina (apenas professor)."""
    if current_user.role != 'docente':
        flash('Apenas docentes podem adicionar disciplinas.', 'danger')
        return redirect(url_for('subject.list_subjects'))

    if request.method == 'POST':
        session = Session()
        name = request.form.get('name')
        if not name:
            flash('O nome da disciplina é obrigatório.', 'danger')
            session.close()
            return redirect(url_for('subject.add_subject'))
        
        # Verificar se já existe com esse nome
        existing_subject = session.query(Subject).filter_by(name=name).first()
        if existing_subject:
            flash('Disciplina já cadastrada.', 'danger')
            session.close()
            return redirect(url_for('subject.add_subject'))
        
        new_subject = Subject(name=name)
        session.add(new_subject)
        session.commit()
        session.close()

        flash('Disciplina adicionada com sucesso!', 'success')
        return redirect(url_for('subject.list_subjects'))

    return render_template('add_subject.html')

@subject_bp.route('/subject/<int:subject_id>/add_student', methods=['GET', 'POST'])
@login_required
def add_student_to_subject(subject_id):
    """Matricular aluno em uma disciplina (apenas professor)."""
    if current_user.role != 'docente':
        flash('Apenas docentes podem adicionar alunos a disciplinas.', 'danger')
        return redirect(url_for('subject.list_subjects'))
    
    session = Session()
    subject = session.query(Subject).get(subject_id)
    if not subject:
        flash('Disciplina não encontrada.', 'danger')
        session.close()
        return redirect(url_for('subject.list_subjects'))

    # Carrega todos os alunos (discentes)
    students = session.query(User).filter_by(role='discente').all()

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if not student_id:
            flash('Selecione um aluno.', 'danger')
            session.close()
            return redirect(url_for('subject.add_student_to_subject', subject_id=subject_id))
        
        # Verificar se o aluno já está matriculado
        existing = session.query(Enrollment).filter_by(student_id=student_id, subject_id=subject_id).first()
        if existing:
            flash('O aluno já está matriculado nesta disciplina.', 'danger')
            session.close()
            return redirect(url_for('subject.add_student_to_subject', subject_id=subject_id))
        
        enrollment = Enrollment(student_id=student_id, subject_id=subject_id)
        session.add(enrollment)
        session.commit()
        session.close()

        flash('Aluno matriculado na disciplina com sucesso!', 'success')
        return redirect(url_for('subject.view_subject_details', subject_id=subject_id))

    session.close()
    return render_template('add_student_to_subject.html', subject=subject, students=students)

@subject_bp.route('/subject/<int:subject_id>')
@login_required
def view_subject_details(subject_id):
    """Exibe detalhes da disciplina.
       - Professor vê todos os alunos matriculados e suas notas.
       - Aluno vê se está matriculado, e se tiver nota, qual é."""
    session = Session()
    subject = session.query(Subject).get(subject_id)
    if not subject:
        flash('Disciplina não encontrada.', 'danger')
        session.close()
        return redirect(url_for('subject.list_subjects'))

    if current_user.role == 'docente':
      enrollments = (
          session.query(Enrollment)
          .options(
              joinedload(Enrollment.student).joinedload(User.grades)
          )
          .filter_by(subject_id=subject_id)
          .all()
      )
      session.close()
      return render_template('subject_details.html',
                            subject=subject,
                            enrollments=enrollments,
                            role='docente')
    else:
        # Aluno
        enrollment = session.query(Enrollment)\
                            .filter_by(subject_id=subject_id, student_id=current_user.id)\
                            .first()
        grade = None
        if enrollment:
            # Se estiver matriculado, tenta pegar a nota
            grade = session.query(Grade)\
                           .filter_by(student_id=current_user.id, subject_id=subject_id)\
                           .first()
        
        session.close()
        return render_template('subject_details.html', 
                               subject=subject, 
                               enrollment=enrollment, 
                               grade=grade, 
                               role='discente')

@subject_bp.route('/subject/<int:subject_id>/bulletin')
@login_required
def subject_bulletin(subject_id):
    session = Session()

    subject = session.query(Subject).get(subject_id)
    if not subject:
        session.close()
        flash('Disciplina não encontrada.', 'danger')
        return redirect(url_for('subject.list_subjects'))

    enrollments = (
        session.query(Enrollment)
        .options(
            joinedload(Enrollment.student).joinedload(User.grades)  # <---- carrega tbm as notas
        )
        .filter_by(subject_id=subject_id)
        .all()
    )

    session.close()

    return render_template('list_bulletins_for_subject.html',
                           subject=subject,
                           enrollments=enrollments)

