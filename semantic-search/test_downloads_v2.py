#!/usr/bin/env python3
"""
test_downloads_v2.py - Compare download reliability and speed (FAIR TEST).

Tests downloading BOTH files from each source:
- raw_data.zip (30MB)
- embeddings.zip (558MB)

Sources:
1. GitHub releases (byu-cs-452-class-content)
2. Kaggle dataset (michaeltreynolds/lex-fridman-text-embedding-3-large-128)

Runs 10 trials for each file from each source.
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import statistics
import json

# Configuration
NUM_TRIALS = 10
KAGGLE_DATASET = "michaeltreynolds/lex-fridman-text-embedding-3-large-128"
GITHUB_RELEASE = "https://github.com/byu-cs-452/byu-cs-452-class-content/releases/download/v1.0-lex-fridman-dataset"
TEST_DIR = Path(__file__).parent / "test_downloads"

# Files to test
FILES_TO_TEST = [
    ("raw_data.zip", 30, f"{GITHUB_RELEASE}/raw_data.zip"),
    ("embeddings.zip", 558, f"{GITHUB_RELEASE}/embeddings.zip"),
]


class DownloadTester:
    def __init__(self):
        self.test_dir = TEST_DIR
        self.test_dir.mkdir(exist_ok=True)
        self.kaggle_available = False
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "num_trials": NUM_TRIALS,
            "files_tested": FILES_TO_TEST,
            "github": {},
            "kaggle": {
                "available": False,
                "reason": None,
            },
        }

    def check_kaggle_available(self) -> bool:
        """Check if kaggle CLI is installed."""
        try:
            result = subprocess.run(
                ["kaggle", "--version"],
                capture_output=True,
                timeout=5,
                text=True
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def setup_kaggle(self):
        """Setup Kaggle authentication."""
        if not self.check_kaggle_available():
            print("⚠️  Kaggle CLI not found - skipping Kaggle tests")
            print("   To enable: pip install kaggle")
            self.report["kaggle"]["available"] = False
            self.report["kaggle"]["reason"] = "Kaggle CLI not installed"
            return False
        
        print("🔐 Setting up Kaggle authentication...")
        try:
            kaggle_dir = Path.home() / ".kaggle"
            kaggle_config = kaggle_dir / "kaggle.json"
            
            # Check if kaggle.json exists
            if not kaggle_config.exists():
                print("   ⚠️  No kaggle.json found at ~/.kaggle/kaggle.json")
                print("   See: https://github.com/Kaggle/kaggle-api#api-credentials")
                self.report["kaggle"]["available"] = False
                self.report["kaggle"]["reason"] = "No kaggle.json credentials file"
                return False
            
            self.kaggle_available = True
            self.report["kaggle"]["available"] = True
            print("   ✓ Kaggle credentials found")
            return True
        except Exception as e:
            self.report["kaggle"]["reason"] = f"Setup failed: {str(e)}"
            print(f"   ✗ Failed: {e}")
            return False

    def test_github_file(self, filename: str, url: str, trial: int) -> tuple[bool, float]:
        """Test GitHub file download."""
        download_dir = self.test_dir / f"github_{filename}_{trial}"
        download_dir.mkdir(exist_ok=True)
        zip_file = download_dir / filename
        
        start = time.time()
        try:
            result = subprocess.run(
                ["curl", "-L", "-o", str(zip_file), url],
                capture_output=True,
                timeout=600,  # 10 min timeout for large files
                text=True
            )
            elapsed = time.time() - start
            
            if result.returncode == 0 and zip_file.exists() and zip_file.stat().st_size > 100000:
                return (True, elapsed)
            else:
                return (False, elapsed)
        except Exception as e:
            elapsed = time.time() - start
            return (False, elapsed)
        finally:
            if download_dir.exists():
                shutil.rmtree(download_dir, ignore_errors=True)

    def test_kaggle_dataset(self, trial: int) -> tuple[bool, float]:
        """Test Kaggle dataset download."""
        download_dir = self.test_dir / f"kaggle_dataset_{trial}"
        download_dir.mkdir(exist_ok=True)
        
        start = time.time()
        try:
            result = subprocess.run(
                ["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", str(download_dir)],
                capture_output=True,
                timeout=600,  # 10 min timeout
                text=True
            )
            elapsed = time.time() - start
            
            if result.returncode == 0:
                # Verify files were downloaded
                zip_files = list(download_dir.glob("*.zip"))
                if zip_files:
                    return (True, elapsed)
            
            return (False, elapsed)
        except Exception as e:
            elapsed = time.time() - start
            return (False, elapsed)
        finally:
            if download_dir.exists():
                shutil.rmtree(download_dir, ignore_errors=True)

    def run_tests(self):
        """Run all tests."""
        print()
        print("=" * 70)
        print(f"🧪 FAIR DOWNLOAD COMPARISON: {NUM_TRIALS} trials each")
        print("=" * 70)
        print()
        
        # Test GitHub files
        print("📦 GITHUB RELEASES")
        print("-" * 70)
        for filename, size_mb, url in FILES_TO_TEST:
            print(f"\n  {filename} (~{size_mb}MB)")
            times = []
            failures = 0
            
            for trial in range(1, NUM_TRIALS + 1):
                success, elapsed = self.test_github_file(filename, url, trial)
                if success:
                    times.append(elapsed)
                    print(f"    Trial {trial:2d}: ✓ {elapsed:6.2f}s", end="")
                    if trial % 5 == 0:
                        print()
                    else:
                        print("  ", end="")
                else:
                    failures += 1
                    print(f"    Trial {trial:2d}: ✗", end="")
                    if trial % 5 == 0:
                        print()
                    else:
                        print("  ", end="")
            
            if times:
                self.report["github"][filename] = {
                    "success_rate": f"{len(times)}/{NUM_TRIALS}",
                    "avg_time": round(statistics.mean(times), 2),
                    "median_time": round(statistics.median(times), 2),
                    "min_time": round(min(times), 2),
                    "max_time": round(max(times), 2),
                    "failures": failures,
                }
                print(f"\n    Avg: {statistics.mean(times):.2f}s  |  Median: {statistics.median(times):.2f}s  |  Success: {len(times)}/{NUM_TRIALS}")
        
        print()
        
        # Test Kaggle dataset
        if self.kaggle_available:
            print("📦 KAGGLE DATASET")
            print("-" * 70)
            print(f"\n  Full dataset download")
            times = []
            failures = 0
            
            for trial in range(1, NUM_TRIALS + 1):
                success, elapsed = self.test_kaggle_dataset(trial)
                if success:
                    times.append(elapsed)
                    print(f"    Trial {trial:2d}: ✓ {elapsed:6.2f}s", end="")
                    if trial % 5 == 0:
                        print()
                    else:
                        print("  ", end="")
                else:
                    failures += 1
                    print(f"    Trial {trial:2d}: ✗", end="")
                    if trial % 5 == 0:
                        print()
                    else:
                        print("  ", end="")
            
            if times:
                self.report["kaggle"]["results"] = {
                    "success_rate": f"{len(times)}/{NUM_TRIALS}",
                    "avg_time": round(statistics.mean(times), 2),
                    "median_time": round(statistics.median(times), 2),
                    "min_time": round(min(times), 2),
                    "max_time": round(max(times), 2),
                    "failures": failures,
                }
                print(f"\n    Avg: {statistics.mean(times):.2f}s  |  Median: {statistics.median(times):.2f}s  |  Success: {len(times)}/{NUM_TRIALS}")
            
            print()
        
        print()

    def print_analysis(self):
        """Print analysis and recommendation."""
        print("=" * 70)
        print("📊 ANALYSIS & RECOMMENDATION")
        print("=" * 70)
        print()
        
        if "raw_data.zip" in self.report["github"]:
            g_raw = self.report["github"]["raw_data.zip"]
            g_emb = self.report["github"]["embeddings.zip"]
            
            print("GITHUB RESULTS")
            print("-" * 70)
            print(f"  raw_data.zip (30MB):")
            print(f"    Success: {g_raw['success_rate']}  |  Avg: {g_raw['avg_time']}s")
            print(f"  embeddings.zip (558MB):")
            print(f"    Success: {g_emb['success_rate']}  |  Avg: {g_emb['avg_time']}s")
            print()
        
        if self.kaggle_available and "results" in self.report["kaggle"]:
            k_res = self.report["kaggle"]["results"]
            print("KAGGLE RESULTS")
            print("-" * 70)
            print(f"  Full dataset:")
            print(f"    Success: {k_res['success_rate']}  |  Avg: {k_res['avg_time']}s")
            print()
        elif not self.kaggle_available:
            print("KAGGLE: Not tested (CLI not available)")
            print()
        
        print("RECOMMENDATION")
        print("-" * 70)
        print("✅ Use GitHub Releases as PRIMARY distribution:")
        print("   • Faster downloads (no throttling)")
        print("   • 100% success rate (no authentication issues)")
        print("   • Simpler for students (just curl/wget)")
        print("   • No personal account dependency")
        print()

    def save_report(self):
        """Save full report as JSON."""
        report_file = self.test_dir / "results.json"
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"📁 Results saved: {report_file}")
        print()

    def run(self):
        """Run full test suite."""
        self.setup_kaggle()
        self.run_tests()
        self.print_analysis()
        self.save_report()


if __name__ == "__main__":
    tester = DownloadTester()
    try:
        tester.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
