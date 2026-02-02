#!/usr/bin/env python3
"""
db_check.py - Verify that the Codespace environment is correctly configured.

This script checks:
1. Database connection works
2. pgvector extension is available
3. Vector operations function correctly

Run this after creating your Codespace to verify everything is working.

Usage:
    python db_check.py
"""

import sys
import psycopg2
from utils import get_connection_string


def main():
    print("🔍 Running environment sanity check...")
    print()
    
    try:
        # Connect to the database
        connection_string = get_connection_string()
        print(f"📡 Connecting to database...")
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        print("   ✓ Connection successful!")
        
        # Enable pgvector extension
        print()
        print("🔧 Enabling pgvector extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
        print("   ✓ pgvector extension enabled!")
        
        # Create a test table
        print()
        print("📝 Creating test table...")
        cursor.execute("DROP TABLE IF EXISTS _sanity_check;")
        cursor.execute("""
            CREATE TABLE _sanity_check (
                id SERIAL PRIMARY KEY,
                test_val TEXT NOT NULL,
                test_vector VECTOR(3)
            );
        """)
        conn.commit()
        print("   ✓ Table created with vector column!")
        
        # Insert test data
        print()
        print("➕ Inserting test data...")
        cursor.execute(
            "INSERT INTO _sanity_check (test_val, test_vector) VALUES (%s, %s) RETURNING id, test_val;",
            ("Database is ready! 🎉", "[1,2,3]")
        )
        result = cursor.fetchone()
        conn.commit()
        print(f"   ✓ Inserted row: id={result[0]}, value='{result[1]}'")
        
        # Test vector operations
        print()
        print("🧪 Testing vector operations...")
        cursor.execute("SELECT vector_dims('[1,2,3]'::vector);")
        dims = cursor.fetchone()[0]
        print(f"   ✓ Vector dimensions work! (test vector has {dims} dimensions)")
        
        # Test L2 distance
        cursor.execute("SELECT '[1,2,3]'::vector <-> '[4,5,6]'::vector;")
        distance = cursor.fetchone()[0]
        print(f"   ✓ L2 distance works! (distance = {distance:.4f})")
        
        # Clean up
        cursor.execute("DROP TABLE _sanity_check;")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print()
        print("=" * 50)
        print("✨ All checks passed! Your environment is ready.")
        print("=" * 50)
        print()
        print("Next steps:")
        print("  1. Download data:  ./download_data.sh")
        print("  2. Build tables:   python db_build.py")
        print("  3. Load data:      python db_insert.py")
        print("  4. Run queries:    python db_query.py")
        print()
        return 0
        
    except psycopg2.Error as e:
        print()
        print(f"❌ Database error: {e}")
        print()
        print("💡 Troubleshooting tips:")
        print("   1. Make sure the database container is running (docker ps)")
        print("   2. Check that you're in the Codespace, not running locally")
        print("   3. Try rebuilding the container (Ctrl+Shift+P → Rebuild Container)")
        return 1
        
    except Exception as e:
        print()
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
