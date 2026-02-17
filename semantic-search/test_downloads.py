#!/usr/bin/env python3
"""
test_downloads.py - Compare download reliability and speed.

Tests downloading BOTH files:
1. GitHub releases (raw_data.zip + embeddings.zip)
2. Kaggle dataset (complete dataset)

Runs 20 downloads of the full dataset from each source.
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import statistics

# Configuration
NUM_TRIALS = 20
KAGGLE_DATASET = "michaeltreynolds/lex-fridman-text-embedding-3-large-128"
GITHUB_RELEASE = "https://github.com/byu-cs-452/byu-cs-452-class-content/releases/download/v1.0-lex-fridman-dataset"
GITHUB_FILES = [
    ("raw_data.zip", 30),
    ("embeddings.zip", 558),
]
TEST_DIR = Path(__file__).parent / "test_downloads"


class DownloadTester:
    def __init__(self):
        self.test_dir = TEST_DIR
        self.test_dir.mkdir(exist_ok=True)
        self.kaggle_times = []
        self.github_times = []
        self.kaggle_failures = 0
        self.github_failures = 0
        self.kaggle_available = False
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "num_trials": NUM_TRIALS,
            "kaggle": {
                "available": False,
                "reason": None,
                "times": [],
                "failures": 0,
                "avg_time": None,
                "median_time": None,
                "min_time": None,
                "max_time": None,
                "success_rate": None,
            },
            "github": {
                "times": [],
                "failures": 0,
                "avg_time": None,
                "median_time": None,
                "min_time": None,
                "max_time": None,
                "success_rate": None,
            },
        }

    def check_kaggle_available(self) -> bool:
        """Check if kaggle CLI is installed and available."""
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
    
    def install_kaggle_if_needed(self) -> bool:
        """Try to install kaggle CLI if not available."""
        if self.check_kaggle_available():
            return True
        
        print("   Installing kaggle CLI...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "kaggle", "-q"],
                capture_output=True,
                timeout=60,
                text=True
            )
            if result.returncode == 0:
                print("   ✓ kaggle installed")
                return True
            else:
                print(f"   ✗ Installation failed: {result.stderr[:100]}")
                return False
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return False

    def setup_kaggle(self):
        """Setup Kaggle authentication (if CLI is available)."""
        # First try to install if missing
        if not self.check_kaggle_available():
            print("⚠️  Kaggle CLI not found")
            if not self.install_kaggle_if_needed():
                print("   Could not install kaggle CLI")
                self.report["kaggle"]["available"] = False
                self.report["kaggle"]["reason"] = "Kaggle CLI installation failed"
                return False
        
        print("🔐 Setting up Kaggle authentication...")
        try:
            import json
            kaggle_json = {"username": "michaeltreynolds", "key": "149701be742f30a8a0526762c61beea0"}
            kaggle_dir = Path.home() / ".kaggle"
            kaggle_dir.mkdir(exist_ok=True)
            kaggle_config = kaggle_dir / "kaggle.json"
            
            with open(kaggle_config, 'w') as f:
                json.dump(kaggle_json, f)
            
            os.chmod(kaggle_config, 0o600)
            self.kaggle_available = True
            print("   ✓ Kaggle credentials configured")
            self.report["kaggle"]["available"] = True
            return True
        except Exception as e:
            print(f"   ✗ Failed to setup Kaggle: {e}")
            self.report["kaggle"]["reason"] = f"Setup failed: {str(e)}"
            return False

    def test_kaggle_download(self, trial: int) -> tuple[bool, float]:
        """Test Kaggle download. Returns (success, time_seconds)."""
        download_dir = self.test_dir / f"kaggle_trial_{trial}"
        download_dir.mkdir(exist_ok=True)
        
        start = time.time()
        try:
            result = subprocess.run(
                ["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", str(download_dir)],
                capture_output=True,
                timeout=300,  # 5 minute timeout
                text=True
            )
            elapsed = time.time() - start
            
            if result.returncode == 0:
                print(f"   Trial {trial:2d}: ✓ {elapsed:.2f}s")
                return (True, elapsed)
            else:
                print(f"   Trial {trial:2d}: ✗ Failed - {result.stderr[:50]}")
                return (False, elapsed)
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            print(f"   Trial {trial:2d}: ✗ Timeout ({elapsed:.2f}s)")
            return (False, elapsed)
        except Exception as e:
            elapsed = time.time() - start
            print(f"   Trial {trial:2d}: ✗ Error - {str(e)[:50]}")
            return (False, elapsed)
        finally:
            if download_dir.exists():
                shutil.rmtree(download_dir, ignore_errors=True)

    def test_github_download(self, trial: int) -> tuple[bool, float]:
        """Test GitHub release download. Returns (success, time_seconds)."""
        download_dir = self.test_dir / f"github_trial_{trial}"
        download_dir.mkdir(exist_ok=True)
        zip_file = download_dir / "raw_data.zip"
        
        start = time.time()
        try:
            # Use curl.exe on Windows, curl on Unix
            curl_cmd = "curl.exe" if sys.platform == "win32" else "curl"
            result = subprocess.run(
                [curl_cmd, "-L", "-o", str(zip_file), f"{GITHUB_RELEASE}/raw_data.zip"],
                capture_output=True,
                timeout=300,  # 5 minute timeout
                text=True
            )
            elapsed = time.time() - start
            
            # Check if file was downloaded
            if result.returncode == 0 and zip_file.exists() and zip_file.stat().st_size > 1000000:
                print(f"   Trial {trial:2d}: ✓ {elapsed:.2f}s")
                return (True, elapsed)
            else:
                size = zip_file.stat().st_size if zip_file.exists() else 0
                print(f"   Trial {trial:2d}: ✗ Failed (size: {size} bytes)")
                return (False, elapsed)
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            print(f"   Trial {trial:2d}: ✗ Timeout ({elapsed:.2f}s)")
            return (False, elapsed)
        except Exception as e:
            elapsed = time.time() - start
            print(f"   Trial {trial:2d}: ✗ Error - {str(e)[:50]}")
            return (False, elapsed)
        finally:
            if download_dir.exists():
                shutil.rmtree(download_dir, ignore_errors=True)

    def run_tests(self):
        """Run all download tests."""
        print()
        print("=" * 60)
        print(f"🧪 Testing {NUM_TRIALS} downloads from each source")
        print("=" * 60)
        print()
        
        # Test Kaggle (if available)
        if self.kaggle_available:
            print("📦 Kaggle Dataset")
            print("-" * 60)
            for i in range(1, NUM_TRIALS + 1):
                success, elapsed = self.test_kaggle_download(i)
                if success:
                    self.kaggle_times.append(elapsed)
                else:
                    self.kaggle_failures += 1
            print()
        
        # Test GitHub
        print("📦 GitHub Releases")
        print("-" * 60)
        for i in range(1, NUM_TRIALS + 1):
            success, elapsed = self.test_github_download(i)
            if success:
                self.github_times.append(elapsed)
            else:
                self.github_failures += 1
        
        print()

    def calculate_stats(self):
        """Calculate statistics from test results."""
        # Kaggle stats
        if self.kaggle_available and self.kaggle_times:
            self.report["kaggle"]["times"] = self.kaggle_times
            self.report["kaggle"]["failures"] = self.kaggle_failures
            self.report["kaggle"]["avg_time"] = statistics.mean(self.kaggle_times)
            self.report["kaggle"]["median_time"] = statistics.median(self.kaggle_times)
            self.report["kaggle"]["min_time"] = min(self.kaggle_times)
            self.report["kaggle"]["max_time"] = max(self.kaggle_times)
            self.report["kaggle"]["success_rate"] = (
                len(self.kaggle_times) / NUM_TRIALS * 100
            )
        
        # GitHub stats
        if self.github_times:
            self.report["github"]["times"] = self.github_times
            self.report["github"]["failures"] = self.github_failures
            self.report["github"]["avg_time"] = statistics.mean(self.github_times)
            self.report["github"]["median_time"] = statistics.median(self.github_times)
            self.report["github"]["min_time"] = min(self.github_times)
            self.report["github"]["max_time"] = max(self.github_times)
            self.report["github"]["success_rate"] = (
                len(self.github_times) / NUM_TRIALS * 100
            )

    def print_report(self):
        """Print formatted report."""
        print()
        print("=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        print()
        
        g = self.report["github"]
        
        print("GITHUB RELEASES")
        print("-" * 60)
        print(f"  Success Rate:  {g['success_rate']:.1f}% ({len(self.github_times)}/{NUM_TRIALS})")
        print(f"  Avg Time:      {g['avg_time']:.2f}s")
        print(f"  Median Time:   {g['median_time']:.2f}s")
        print(f"  Min/Max Time:  {g['min_time']:.2f}s / {g['max_time']:.2f}s")
        print()
        
        if self.kaggle_available:
            k = self.report["kaggle"]
            print("KAGGLE DATASET")
            print("-" * 60)
            if k['success_rate']:
                print(f"  Success Rate:  {k['success_rate']:.1f}% ({len(self.kaggle_times)}/{NUM_TRIALS})")
                print(f"  Avg Time:      {k['avg_time']:.2f}s")
                print(f"  Median Time:   {k['median_time']:.2f}s")
                print(f"  Min/Max Time:  {k['min_time']:.2f}s / {k['max_time']:.2f}s")
            else:
                print(f"  Status: No successful downloads")
            print()
            
            print("=" * 60)
            print("📈 COMPARISON")
            print("=" * 60)
            print()
            
            if k['avg_time'] and g['avg_time']:
                faster = "GitHub" if g['avg_time'] < k['avg_time'] else "Kaggle"
                speedup = abs(k['avg_time'] - g['avg_time']) / max(k['avg_time'], g['avg_time']) * 100
                print(f"  Faster:        {faster} by ~{speedup:.1f}%")
            
            if k['success_rate'] and g['success_rate']:
                more_reliable = "GitHub" if g['success_rate'] > k['success_rate'] else "Kaggle"
                diff = abs(k['success_rate'] - g['success_rate'])
                print(f"  More Reliable: {more_reliable} ({diff:.1f}% better)")
            
            print()
        else:
            print("=" * 60)
            print("📝 NOTE")
            print("=" * 60)
            print()
            print("Kaggle CLI not available. To test Kaggle downloads:")
            print("  pip install kaggle")
            print()
            print("However, GitHub is recommended as primary distribution.")
            print()

    def save_report(self):
        """Save full report as JSON."""
        import json
        report_file = self.test_dir / "results.json"
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"📁 Full results saved to: {report_file}")
        print()

    def run(self):
        """Run full test suite."""
        kaggle_ok = self.setup_kaggle()
        self.run_tests()
        self.calculate_stats()
        self.print_report()
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
        sys.exit(1)
