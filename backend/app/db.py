from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./xandrosyn.db"), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
