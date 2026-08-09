from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_name = Column(String, nullable=False)
    dataset_name = Column(String, nullable=False)
    dataset_rows = Column(Integer, default=0)
    dataset_size = Column(Float, default=0.0) # in MB
    total_flows = Column(Integer, default=0)
    attacks = Column(Integer, default=0)
    attack_rate = Column(Float, default=0.0)
    benign = Column(Integer, default=0)
    confidence = Column(Float, default=0.0)
    risk_level = Column(String, default="Unknown")
    summary = Column(Text, nullable=True)
    pdf_path = Column(String, nullable=True)
    csv_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")
    attack_breakdown = relationship("ReportAttack", back_populates="report", cascade="all, delete-orphan")
    investigations = relationship("Investigation", back_populates="report", cascade="all, delete-orphan")


class ReportAttack(Base):
    __tablename__ = "report_attacks"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    attack_name = Column(String, nullable=False)
    count = Column(Integer, default=0)

    report = relationship("Report", back_populates="attack_breakdown")


class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    prediction = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    confidence = Column(Float, default=0.0)
    anomaly_score = Column(Float, default=0.0)

    report = relationship("Report", back_populates="investigations")


class IOC(Base):
    __tablename__ = "iocs"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"))
    indicator = Column(String, index=True)  # e.g., IP, domain, hash, URL
    ioc_type = Column(String)               # IP Address, SHA256, MD5, URL, Domain
    confidence = Column(Float, default=0.0)
    severity = Column(String, default="High")
    created_at = Column(DateTime, default=datetime.utcnow)

class MaliciousIP(Base):
    __tablename__ = "malicious_ips"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"))
    ip_address = Column(String, index=True)
    country = Column(String)
    country_code = Column(String)           # e.g., "ru", "nl", "sg", "us", "de"
    latitude = Column(Float)
    longitude = Column(Float)
    risk_level = Column(String)             # Critical, High, Medium, Low
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)