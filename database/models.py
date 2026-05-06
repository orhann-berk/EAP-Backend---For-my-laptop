from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from database.database import Base


class DbEmployee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String)
    email = Column(String)
    password = Column(String)
    creationTimestamp = Column(DateTime)
    updatedTimestamp = Column(DateTime)
    isActive = Column(Boolean)

    employees = relationship("DbEmpRole", back_populates="employee")


class DbRole(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    roles = relationship("DbEmpRole", back_populates="role")


class DbEmpRole(Base):
    __tablename__ = "emp_role"

    id = Column(Integer, primary_key=True, index=True)
    roleId = Column(Integer, ForeignKey("role.id"))
    empId = Column(Integer, ForeignKey("employee.id"))

    role = relationship("DbRole", back_populates="roles")
    employee = relationship("DbEmployee", back_populates="employees")
