#!/usr/bin/env python3
"""
download_data.py - Download the Lex Fridman podcast embeddings dataset.

This script downloads the pre-computed embeddings and batch request files
from GitHub Releases. The dataset is approximately 615MB total.

Expected download time: 1-3 minutes depending on your connection.

Usage:
    python download_data.py
"""

import os
import sys
import zipfile
import requests
from pathlib import Path

# GitHub Release URLs
RELEASE_BASE = "https://github.com/byu-cs-452/byu-cs-452-class-content/releases/download/v1.0-lex-fridman-dataset"
FILES = [
    ("raw_data.zip", f"{RELEASE_BASE}/raw_data.zip", 30),       # ~30 MB
    ("embeddings.zip", f"{RELEASE_BASE}/embeddings.zip", 585),  # ~585 MB
]


def download_file(url: str, dest_path: Path, expected_mb: int) -> bool:
    """Download a file with progress indicator."""
    try:
        response = requests.get(url, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    pct = (downloaded / total_size) * 100
                    mb = downloaded / (1024 * 1024)
                    print(f"\r   {mb:.1f} / {expected_mb} MB ({pct:.0f}%)", end="", flush=True)
        
        print()  # Newline after progress
        return True
        
    except requests.RequestException as e:
        print(f"\n   ❌ Download failed: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extract a zip file and clean up."""
    print(f"   Extracting...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        zip_path.unlink()  # Remove zip after extraction
        return True
    except zipfile.BadZipFile:
        print(f"   ❌ Invalid zip file")
        return False


def main():
    print()
    print("📥 Downloading Lex Fridman Podcast Embeddings")
    print("   ~615 MB total, expect 1-3 minutes")
    print("=" * 50)
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    
    # Check if already downloaded
    if data_dir.exists() and list(data_dir.glob("**/*.jsonl")):
        print("✅ Data already exists!")
        print(f"   Location: {data_dir}")
        print()
        print("   To re-download, delete the data folder:")
        print(f"   rm -rf {data_dir}")
        return 0
    
    # Create data directory
    data_dir.mkdir(exist_ok=True)
    
    # Download each file
    for filename, url, expected_mb in FILES:
        print(f"📦 {filename} ({expected_mb} MB)")
        dest_path = data_dir / filename
        
        if not download_file(url, dest_path, expected_mb):
            return 1
        
        if not extract_zip(dest_path, data_dir):
            return 1
        
        print(f"   ✅ Done")
        print()
    
    # Verify
    jsonl_count = len(list(data_dir.glob("**/*.jsonl")))
    print("=" * 50)
    print(f"✅ Download complete!")
    print(f"   {jsonl_count} data files ready")
    print()
    print("Next steps:")
    print("   python db_build.py    # Create tables")
    print("   python db_insert.py   # Load data")
    print("   python db_query.py    # Run queries")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
