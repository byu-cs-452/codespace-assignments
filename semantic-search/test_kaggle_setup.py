#!/usr/bin/env python3
"""
test_kaggle_setup.py - Test if Kaggle downloads work before running full test.

This script:
1. Installs kaggle CLI if needed
2. Sets up credentials
3. Runs ONE test download to verify it works
4. Reports success/failure
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import shutil

KAGGLE_DATASET = "michaeltreynolds/lex-fridman-text-embedding-3-large-128"
TEST_DIR = Path(__file__).parent / "test_downloads"
TEST_DIR.mkdir(exist_ok=True)

print("🔍 Testing Kaggle setup...")
print()

# Step 1: Install kaggle CLI if needed
print("📦 Checking for kaggle CLI...")
try:
    result = subprocess.run(["kaggle", "--version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("   ✓ kaggle CLI is installed")
        kaggle_available = True
    else:
        print("   ✗ kaggle CLI not working, attempting to install...")
        kaggle_available = False
except FileNotFoundError:
    print("   ✗ kaggle CLI not found, attempting to install...")
    kaggle_available = False

# If not available, try to install
if not kaggle_available:
    print()
    print("   Installing kaggle...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "kaggle", "-q"],
            capture_output=True,
            timeout=60,
            text=True
        )
        if result.returncode == 0:
            print("   ✓ kaggle installed successfully")
            kaggle_available = True
        else:
            print(f"   ✗ Failed to install: {result.stderr[:100]}")
            kaggle_available = False
    except Exception as e:
        print(f"   ✗ Installation error: {e}")
        kaggle_available = False

if not kaggle_available:
    print()
    print("❌ Kaggle CLI could not be set up")
    print("   Manual fix: pip install kaggle")
    sys.exit(1)

# Step 2: Set up credentials
print()
print("🔐 Setting up Kaggle credentials...")
try:
    kaggle_json = {
        "username": "michaeltreynolds",
        "key": "149701be742f30a8a0526762c61beea0"
    }
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(exist_ok=True)
    kaggle_config = kaggle_dir / "kaggle.json"
    
    with open(kaggle_config, 'w') as f:
        json.dump(kaggle_json, f)
    
    os.chmod(kaggle_config, 0o600)
    print("   ✓ Credentials configured")
except Exception as e:
    print(f"   ✗ Failed to set up credentials: {e}")
    sys.exit(1)

# Step 3: Test ONE download
print()
print("🧪 Testing single Kaggle download...")
download_dir = TEST_DIR / "kaggle_test"
download_dir.mkdir(exist_ok=True)

try:
    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", str(download_dir)],
        capture_output=True,
        timeout=300,  # 5 minutes
        text=True
    )
    
    if result.returncode == 0:
        # Check if file was actually downloaded
        files = list(download_dir.glob("*.zip"))
        if files:
            file_size = files[0].stat().st_size
            print(f"   ✓ Download successful! ({file_size / (1024*1024):.1f} MB)")
            print()
            print("✅ Kaggle setup is working!")
            print()
            print("You can now run: python test_downloads.py")
            # Clean up
            shutil.rmtree(download_dir)
            sys.exit(0)
        else:
            print("   ✗ No files found after download")
            print(f"   Response: {result.stdout[:200]}")
    else:
        print(f"   ✗ Download failed")
        print(f"   Error: {result.stderr[:200]}")
        print()
        print("Common issues:")
        print("  1. Invalid credentials")
        print("  2. Dataset not publicly available")
        print("  3. Network/firewall blocking Kaggle")

except subprocess.TimeoutExpired:
    print("   ✗ Download timed out (5 minutes)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Clean up
shutil.rmtree(download_dir, ignore_errors=True)

print()
print("❌ Kaggle setup failed")
print("   GitHub releases will be used as fallback")
sys.exit(1)
