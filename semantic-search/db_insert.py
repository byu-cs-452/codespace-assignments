"""
db_insert.py - Load podcast data into the database.

This script reads the podcast data and embeddings from the data files
and inserts them into the PostgreSQL database.

Data sources:
- batch_request_XX.jsonl: Contains raw text and metadata
- embedding.jsonl: Contains the 128-dimensional embeddings

Run this script AFTER db_build.py has created the tables.

Usage:
    python db_insert.py
"""

import os
import json
import glob
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset

from utils import get_connection_string, fast_pg_insert, vector_to_pg_format

# Get database connection
CONNECTION = get_connection_string()

# Path to the data directory (download using download_data.sh first)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


# =============================================================================
# REFERENCE: Sample data structures
# =============================================================================
# These are complete examples of what you'll find in the data files.
# Use these to understand how to extract the fields you need.

# Sample document from batch_request_XX.jsonl:
SAMPLE_DOCUMENT = """
{
  "custom_id": "89:115",
  "url": "/v1/embeddings",
  "method": "POST",
  "body": {
    "input": " have been possible without these approaches?",
    "model": "text-embedding-3-large",
    "dimensions": 128,
    "metadata": {
      "title": "Podcast: Boris Sofman: Waymo, Cozmo, Self-Driving Cars, and the Future of Robotics | Lex Fridman Podcast #241",
      "podcast_id": "U_AREIyd0Fc",
      "start_time": 484.52,
      "stop_time": 487.08
    }
  }
}
"""

# Sample embedding from embedding.jsonl:
SAMPLE_EMBEDDING = """
{
  "id": "batch_req_QZBmHS7FBiVABxcsGiDx2THJ",
  "custom_id": "89:115",
  "response": {
    "status_code": 200,
    "request_id": "7a55eba082c70aca9e7872d2b694f095",
    "body": {
      "object": "list",
      "data": [
        {
          "object": "embedding",
          "index": 0,
          "embedding": [
            0.0035960325,
            -0.012345678,
            ... (126 more values) ...
            -0.093248844
          ]
        }
      ],
      "model": "text-embedding-3-large",
      "usage": {
        "prompt_tokens": 7,
        "total_tokens": 7
      }
    }
  },
  "error": null
}
"""


# =============================================================================
# STEP 1: Read the embedding files
# =============================================================================
# TODO: Read all embedding.jsonl files from the data directory
#
# Each line in embedding.jsonl looks like:
# {
#   "id": "batch_req_...",
#   "custom_id": "89:115",
#   "response": {
#     "status_code": 200,
#     "body": {
#       "data": [{"embedding": [0.003, -0.012, ..., 0.045]}]
#     }
#   }
# }
#
# You need to extract:
#   - custom_id → segment ID (e.g., "89:115")
#   - embedding → 128-dimensional vector

def load_embeddings():
    """Load embeddings from embedding.jsonl files."""
    embeddings = {}  # Dict mapping segment_id -> embedding vector
    
    # TODO: Find and read all embedding.jsonl files
    # Hint: Use glob to find files matching pattern 'data/**/embedding*.jsonl'
    
    print(f"📊 Loaded {len(embeddings)} embeddings")
    return embeddings


# =============================================================================
# STEP 2: Read the document/request files
# =============================================================================
# TODO: Read all batch_request_XX.jsonl files from the data directory
#
# Each line looks like:
# {
#   "custom_id": "89:115",
#   "body": {
#     "input": "have been possible without these approaches?",
#     "metadata": {
#       "title": "Podcast: Boris Sofman: ...",
#       "podcast_id": "U_AREIyd0Fc",
#       "start_time": 484.52,
#       "stop_time": 487.08
#     }
#   }
# }
#
# You need to extract:
#   - custom_id → segment ID
#   - input → content (raw text)
#   - metadata.podcast_id → podcast foreign key
#   - metadata.title → podcast title (for podcast table)
#   - metadata.start_time, stop_time → timestamps

def load_documents():
    """Load documents from batch_request_XX.jsonl files."""
    documents = []  # List of document dictionaries
    
    # TODO: Find and read all batch_request_*.jsonl files
    # Hint: Use glob to find files matching pattern 'data/**/batch_request*.jsonl'
    
    print(f"📄 Loaded {len(documents)} documents")
    return documents


# =============================================================================
# STEP 3: (Optional) Load raw data from HuggingFace
# =============================================================================
# If you need additional data, you can load the raw podcast dataset:
#
# from datasets import load_dataset
# ds = load_dataset("Whispering-GPT/lex-fridman-podcast")
#
# This contains the full transcripts if needed.


# =============================================================================
# STEP 4: Create DataFrames for insertion
# =============================================================================
# TODO: Combine the embeddings and documents into DataFrames for each table
#
# podcast_df should have columns: ['id', 'title']
# segment_df should have columns: ['id', 'start_time', 'end_time', 'content', 'embedding', 'podcast_id']

def prepare_dataframes(documents, embeddings):
    """Prepare DataFrames for podcast and segment tables."""
    
    # TODO: Create podcast_df with unique podcasts
    podcast_df = None
    
    # TODO: Create segment_df by joining documents with embeddings
    segment_df = None
    
    return podcast_df, segment_df


# =============================================================================
# STEP 5: Insert into PostgreSQL
# =============================================================================
# TODO: Use fast_pg_insert to load data into the database
#
# Remember:
# - Insert podcasts FIRST (because segments have a foreign key to podcast)
# - For large datasets, you may want to insert in chunks to avoid memory issues

def insert_data(podcast_df, segment_df):
    """Insert data into the database."""
    
    # TODO: Insert podcast data
    # fast_pg_insert(podcast_df, CONNECTION, 'podcast', ['id', 'title'])
    
    # TODO: Insert segment data
    # Hint: You may need to convert embeddings to PostgreSQL format
    # Use vector_to_pg_format() from utils.py
    # 
    # For large datasets, consider chunking:
    # for i in tqdm(range(0, len(segment_df), 10000)):
    #     chunk = segment_df.iloc[i:i+10000]
    #     fast_pg_insert(chunk, CONNECTION, 'segment', [...])
    
    pass


# =============================================================================
# Main execution
# =============================================================================
def main():
    print("📥 Loading data into database...")
    print()
    
    # Check if data exists
    if not os.path.exists(DATA_DIR):
        print("❌ Data directory not found!")
        print("   Run './download_data.sh' first to download the dataset.")
        return
    
    # Load data
    embeddings = load_embeddings()
    documents = load_documents()
    
    # Prepare DataFrames
    podcast_df, segment_df = prepare_dataframes(documents, embeddings)
    
    # Insert into database
    insert_data(podcast_df, segment_df)
    
    print()
    print("✅ Data loading complete!")


if __name__ == "__main__":
    main()
