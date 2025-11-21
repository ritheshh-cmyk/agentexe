import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool, NullPool

# Get database URL from environment
# Vercel Postgres automatically sets POSTGRES_URL
DATABASE_URL = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL", "sqlite:///:memory:")

if "sqlite" in DATABASE_URL:
    # Local development with SQLite
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    # PostgreSQL configuration (Vercel Postgres or Supabase)
    # SQLAlchemy requires 'postgresql://', but some providers give 'postgres://'
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Serverless-optimized connection pooling
    # NullPool prevents connection pooling issues in serverless environments
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,  # No connection pooling for serverless
        connect_args={
            "sslmode": "require",
            "connect_timeout": 10,
        }
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
