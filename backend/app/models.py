from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase): pass
def now(): return datetime.now(timezone.utc)
class Job(Base):
    __tablename__="jobs"
    id: Mapped[int]=mapped_column(primary_key=True)
    source: Mapped[str]=mapped_column(String(120), index=True)
    external_id: Mapped[str]=mapped_column(String(255), index=True)
    title: Mapped[str]=mapped_column(String(255))
    company: Mapped[str]=mapped_column(String(255))
    location: Mapped[str]=mapped_column(String(255), default="")
    url: Mapped[str]=mapped_column(Text)
    description: Mapped[str]=mapped_column(Text, default="")
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class Alert(Base):
    __tablename__="alerts"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[str]=mapped_column(String(120), index=True)
    keyword: Mapped[str]=mapped_column(String(255))
    location: Mapped[str]=mapped_column(String(255), default="")
    enabled: Mapped[bool]=mapped_column(Boolean, default=True)
class DeviceToken(Base):
    __tablename__="device_tokens"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[str]=mapped_column(String(120), index=True)
    token: Mapped[str]=mapped_column(Text, unique=True)
    platform: Mapped[str]=mapped_column(String(30), default="android")
class NotificationEvent(Base):
    __tablename__="notification_events"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[str]=mapped_column(String(120), index=True)
    job_id: Mapped[int]=mapped_column(ForeignKey("jobs.id"))
    status: Mapped[str]=mapped_column(String(30), default="pending")
