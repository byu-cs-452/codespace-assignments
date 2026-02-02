#!/usr/bin/env python3
"""
download_data.py - Download the Lex Fridman podcast embeddings dataset.

This script downloads the pre-computed embeddings and batch request files.
The dataset is approximately 550MB total.

Usage:
    python download_data.py

The script will check for existing data and skip if already downloaded.
"""

import os
import sys
import zipfile
import requests
from pathlib import Path

# =============================================================================
# DATA SOURCE CONFIGURATION
# =============================================================================
# Change these URLs if data hosting changes in the future.
# 
# Current sources (choose one):
#   - GitHub Releases: Most reliable for class use
#   - Google Drive: Original source, may have rate limits
#   - Kaggle: Requires API key setup
#
# To switch sources, update the URLs below.

DATA_SOURCES = {
    # GitHub Releases (recommended for class use)
    # Upload files to: https://github.com/byu-cs-452/codespace-assignments/releases
    "github": {
        "raw_data": "https://github.com/byu-cs-452/codespace-assignments/releases/download/v1.0/raw_data.zip",
        "embeddings": "https://github.com/byu-cs-452/codespace-assignments/releases/download/v1.0/embeddings.zip",
    },
    
    # Google Drive (original source - may have rate limits)
    "gdrive": {
        "raw_data": "1RXxlcUBHhE4_fQHU3qlX7Ghz5pBSvNrV",  # File ID
        "embeddings": "1uCx21PhPtpnmy3ZpTc8MoR0vvokTYzrB",  # File ID
    },
}

# Which source to use (change this if needed)
ACTIVE_SOURCE = "gdrive"  # Options: "github", "gdrive"


# =============================================================================
# DOWNLOAD FUNCTIONS
# =============================================================================

def download_from_github(url: str, dest_path: Path) -> bool:
    """Download a file from GitHub Releases."""
    print(f"   Downloading from GitHub...")
    
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
                    print(f"\r   Progress: {pct:.1f}%", end="", flush=True)
        
        print()  # Newline after progress
        return True
        
    except requests.RequestException as e:
        print(f"\n   ❌ Download failed: {e}")
        return False


def download_from_gdrive(file_id: str, dest_path: Path) -> bool:
    """Download a file from Google Drive using gdown."""
    print(f"   Downloading from Google Drive...")
    
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(dest_path), quiet=False)
        return dest_path.exists()
        
    except ImportError:
        print("   ❌ gdown not installed. Run: pip install gdown")
        return False
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extract a zip file."""
    print(f"   Extracting {zip_path.name}...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # Clean up zip file
        zip_path.unlink()
        return True
        
    except zipfile.BadZipFile:
        print(f"   ❌ Invalid zip file: {zip_path}")
        return False


def check_existing_data(data_dir: Path) -> bool:
    """Check if data already exists."""
    # Look for any .jsonl files
    jsonl_files = list(data_dir.glob("**/*.jsonl"))
    return len(jsonl_files) > 0


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("📥 Lex Fridman Podcast Embeddings Dataset")
    print("=" * 50)
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    
    # Check if already downloaded
    if check_existing_data(data_dir):
        print("✅ Data already exists!")
        print(f"   Location: {data_dir}")
        print()
        print("   To re-download, delete the data folder first:")
        print(f"   rm -rf {data_dir}")
        return 0
    
    # Create data directory
    data_dir.mkdir(exist_ok=True)
    
    # Get source configuration
    source = DATA_SOURCES.get(ACTIVE_SOURCE)
    if not source:
        print(f"❌ Unknown data source: {ACTIVE_SOURCE}")
        return 1
    
    print(f"📡 Source: {ACTIVE_SOURCE}")
    print()
    
    # Download files
    files_to_download = [
        ("raw_data", "raw_data.zip"),
        ("embeddings", "embeddings.zip"),
    ]
    
    for key, filename in files_to_download:
        print(f"📦 Downloading {filename}...")
        dest_path = data_dir / filename
        
        if ACTIVE_SOURCE == "github":
            success = download_from_github(source[key], dest_path)
        elif ACTIVE_SOURCE == "gdrive":
            success = download_from_gdrive(source[key], dest_path)
        else:
            print(f"   ❌ Unknown source type: {ACTIVE_SOURCE}")
            success = False
        
        if not success:
            print(f"   ❌ Failed to download {filename}")
            return 1
        
        # Extract
        if not extract_zip(dest_path, data_dir):
            return 1
        
        print(f"   ✅ {filename} complete!")
        print()
    
    # Verify
    jsonl_count = len(list(data_dir.glob("**/*.jsonl")))
    print("=" * 50)
    print(f"✅ Download complete!")
    print(f"   Location: {data_dir}")
    print(f"   Files: {jsonl_count} .jsonl files found")
    print()
    print("Next steps:")
    print("   python db_build.py    # Create tables")
    print("   python db_insert.py   # Load data")
    print("   python db_query.py    # Run queries")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
