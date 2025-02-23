from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.id'), nullable=False)

    student = relationship("User", back_populates="enrollments")
    subject = relationship("Subject", back_populates="enrollments")
