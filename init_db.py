"""
Database initialization script for Supabase.
Run this locally to create the required tables in your Supabase database.
"""
import os
from sqlalchemy import create_engine
from server.models import Base

# Use the same DATABASE_URL that Vercel uses
DATABASE_URL = "postgresql://postgres:Rithesh%40555@db.bnxtjlzlxgcdxlelfmom.supabase.co:5432/postgres"

# Fix the scheme if needed
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")
print("\nTables created:")
print("- devices (device_id, identifier, approved, created_at)")
print("- otps (id, identifier, otp_hash, device_id, is_used, created_at, expires_at)")
