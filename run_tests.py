#!/usr/bin/env python3
"""
Test runner script for the Notched Music project.
This script runs the test suite and generates coverage reports.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    """Main test runner function."""
    print("Notched Music Test Runner")
    print("=" * 60)
    
    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if pytest is available
    try:
        import pytest
        print(f"Using pytest version: {pytest.__version__}")
    except ImportError:
        print("ERROR: pytest is not installed. Please install it with:")
        print("pip install pytest pytest-cov")
        sys.exit(1)
    
    # Run tests with different configurations
    test_commands = [
        ("pytest tests/ -v", "Basic test run"),
        ("pytest tests/ --cov=src --cov-report=term-missing", "Test run with coverage"),
        ("pytest tests/ --cov=src --cov-report=html", "Generate HTML coverage report"),
    ]
    
    success_count = 0
    total_commands = len(test_commands)
    
    for command, description in test_commands:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"FAILED: {description}")
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Commands executed: {success_count}/{total_commands}")
    
    if success_count == total_commands:
        print("✅ All tests completed successfully!")
        print("\nCoverage report generated in htmlcov/index.html")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

