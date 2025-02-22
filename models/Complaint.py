from database import db

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)
    justification = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Pendente")  # Pode ser "Aprovado" ou "Rejeitado"
