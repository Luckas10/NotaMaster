from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Grade(Base):
    __tablename__ = 'grade'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    grade: Mapped[float] = mapped_column(Float, nullable=False)

    student = relationship("User", back_populates="grades")
    complaints = relationship("Complaint", back_populates="grade")  # Relação com Complaint
