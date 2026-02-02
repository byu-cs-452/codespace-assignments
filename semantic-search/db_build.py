"""
db_build.py - Create the database tables for the podcast recommender system.

This script creates the necessary tables in PostgreSQL with pgvector support:
- podcast: Stores podcast metadata
- segment: Stores podcast segments with their embeddings

Run this script FIRST before loading data.

Usage:
    python db_build.py
"""

import psycopg2
from utils import get_connection_string

# Get database connection
CONNECTION = get_connection_string()


# =============================================================================
# STEP 1: Enable the pgvector extension
# =============================================================================
# This allows us to use the 'vector' data type for storing embeddings
CREATE_EXTENSION = "CREATE EXTENSION IF NOT EXISTS vector"


# =============================================================================
# STEP 2: Create the podcast table
# =============================================================================
# TODO: Write the CREATE TABLE statement for the podcast table
# 
# Schema:
#   - id: TEXT, PRIMARY KEY (the YouTube video ID, e.g., 'TRdL6ZzWBS0')
#   - title: TEXT (the full podcast title)
#
# Example row:
#   id: 'TRdL6ZzWBS0'
#   title: 'Jed Buchwald: Isaac Newton and the Philosophy of Science | Lex Fridman Podcast #214'

CREATE_PODCAST_TABLE = """

"""


# =============================================================================
# STEP 3: Create the segment table  
# =============================================================================
# TODO: Write the CREATE TABLE statement for the segment table
#
# Schema:
#   - id: TEXT, PRIMARY KEY (format: "podcast_idx:segment_idx", e.g., "0:1")
#   - start_time: FLOAT (start timestamp in seconds)
#   - end_time: FLOAT (end timestamp in seconds)  
#   - content: TEXT (the raw text transcription)
#   - embedding: VECTOR(128) (the 128-dimensional embedding vector)
#   - podcast_id: TEXT, FOREIGN KEY references podcast(id)
#
# Hint: Use VECTOR(128) for the embedding column - this is a pgvector type!
#
# Example row:
#   id: '89:115'
#   start_time: 484.52
#   end_time: 487.08
#   content: 'have been possible without these approaches?'
#   embedding: [0.003, -0.012, ..., 0.045]  (128 numbers)
#   podcast_id: 'U_AREIyd0Fc'

CREATE_SEGMENT_TABLE = """

"""


# =============================================================================
# STEP 4: Execute the SQL statements
# =============================================================================
def main():
    print("🔧 Setting up database...")
    
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    # Enable pgvector extension
    print("  → Enabling pgvector extension...")
    cursor.execute(CREATE_EXTENSION)
    
    # TODO: Create the podcast table
    # print("  → Creating podcast table...")
    # cursor.execute(CREATE_PODCAST_TABLE)
    
    # TODO: Create the segment table
    # print("  → Creating segment table...")
    # cursor.execute(CREATE_SEGMENT_TABLE)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Database setup complete!")


if __name__ == "__main__":
    main()
