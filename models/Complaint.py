from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Complaint(Base):
    __tablename__ = 'complaints'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)  # Corrigido 'user.id' para 'users.id'
    grade_id: Mapped[int] = mapped_column(Integer, ForeignKey('grades.id'), nullable=False)  # Corrigido 'grade.id' para 'grades.id'
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Pendente")  # Pode ser "Aprovado" ou "Rejeitado"

    student = relationship("User", back_populates="complaints")
    grade = relationship("Grade", back_populates="complaints")  # Relação com Grade
