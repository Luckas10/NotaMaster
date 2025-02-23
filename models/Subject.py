from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    grades = relationship("Grade", back_populates="subject")

    # Novo relacionamento para matrículas
    enrollments = relationship("Enrollment", back_populates="subject")
    