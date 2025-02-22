from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)  # Corrigido 'user.id' para 'users.id'
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.id'), nullable=False)  # Relacionamento com Subject
    grade: Mapped[float] = mapped_column(Float, nullable=False)

    # Relacionamento com o modelo User
    student = relationship("User", back_populates="grades")
    
    # Relacionamento com o modelo Subject
    subject = relationship("Subject", back_populates="grades")

    complaints = relationship("Complaint", back_populates="grade")  # Relacionamento com Complaint
