#!/usr/bin/env python3
"""
Database sanity check script for CS-452 Assignment 1
This script verifies that the Postgres database with pgvector is ready.
"""

import psycopg2
from psycopg2 import sql
import sys

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'vectordb',
    'user': 'student',
    'password': 'vector_lab_2024'
}

def main():
    print("🔍 Running database sanity check...")
    
    try:
        # Connect to the database
        print(f"📡 Connecting to {DB_CONFIG['database']}@{DB_CONFIG['host']}...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Enable pgvector extension
        print("🔧 Enabling pgvector extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
        
        # Drop table if exists (for clean testing)
        cursor.execute("DROP TABLE IF EXISTS lab_check;")
        
        # Create sample table
        print("📝 Creating test table 'lab_check'...")
        cursor.execute("""
            CREATE TABLE lab_check (
                id SERIAL PRIMARY KEY,
                test_val TEXT NOT NULL
            );
        """)
        conn.commit()
        
        # Insert test row
        print("➕ Inserting test data...")
        cursor.execute(
            "INSERT INTO lab_check (test_val) VALUES (%s) RETURNING id, test_val;",
            ("Database is ready! 🎉",)
        )
        result = cursor.fetchone()
        conn.commit()
        
        # Verify the insert
        print("✅ Data inserted successfully!")
        print(f"   ID: {result[0]}")
        print(f"   Value: {result[1]}")
        
        # Test pgvector functionality
        print("\n🧪 Testing pgvector functionality...")
        cursor.execute("SELECT vector_dims('[1,2,3]'::vector);")
        dims = cursor.fetchone()[0]
        print(f"✅ pgvector is working! Test vector has {dims} dimensions.")
        
        # Clean up
        cursor.execute("DROP TABLE lab_check;")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("\n✨ All checks passed! Your environment is ready for Assignment 1.")
        return 0
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure the database container is running")
        print("   2. Check that you're in the Codespace (not running locally)")
        print("   3. Try rebuilding the container")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
