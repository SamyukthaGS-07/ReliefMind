import uuid
from typing import Optional, List
from sqlalchemy import String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), index=True)
    source_type: Mapped[str] = mapped_column(String(50)) # e.g. "citizen", "official", "news"
    reliability_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    reports: Mapped[List["Report"]] = relationship("Report", back_populates="source")

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sources.id"))
    content: Mapped[str] = mapped_column(Text)
    
    # Store AI extracted JSON
    extracted_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    source: Mapped["Source"] = relationship("Source", back_populates="reports")
    incident_links: Mapped[List["IncidentReport"]] = relationship("IncidentReport", back_populates="report")

class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String(100), index=True) # e.g. "flood", "earthquake"
    location_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Keeping it simple before PostGIS geometry is added
    people_affected: Mapped[Optional[int]] = mapped_column(nullable=True)
    reliability: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    reports: Mapped[List["IncidentReport"]] = relationship("IncidentReport", back_populates="incident")
    needs: Mapped[List["Need"]] = relationship("Need", back_populates="incident")

class IncidentReport(Base):
    __tablename__ = "incident_reports"

    incident_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("incidents.id"), primary_key=True)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reports.id"), primary_key=True)
    
    # Confidence that this report is about this incident
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True) 

    incident: Mapped["Incident"] = relationship("Incident", back_populates="reports")
    report: Mapped["Report"] = relationship("Report", back_populates="incident_links")

class Need(Base):
    __tablename__ = "needs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("incidents.id"))
    
    need_type: Mapped[str] = mapped_column(String(100), index=True) # e.g. "medical", "food"
    urgency: Mapped[str] = mapped_column(String(50)) # e.g. "high", "critical"
    
    # Calculated priority
    priority_score: Mapped[Optional[int]] = mapped_column(nullable=True)
    priority_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    incident: Mapped["Incident"] = relationship("Incident", back_populates="needs")
