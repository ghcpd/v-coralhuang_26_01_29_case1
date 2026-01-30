#!/usr/bin/env python3
"""
Test Runner for Snowflake Comment Parsing Fix

This script runs all tests for the Snowflake comment parsing bug fix.
It executes both the minimal reproduction case and the comprehensive test suite.

Usage:
    python run_tests.py
    
Or on Windows:
    python run_tests.py

Exit codes:
    0 - All tests passed
    1 - One or more tests failed
"""

import sys
import subprocess
from pathlib import Path


def run_test_file(filepath, description):
    """Run a single test file and return success status"""
    print()
    print("=" * 80)
    print(f"Running: {description}")
    print(f"File: {filepath}")
    print("=" * 80)
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=False,
            text=True,
            cwd=Path(__file__).parent
        )
        
        success = result.returncode == 0
        
        print()
        if success:
            print(f"✓ {description} - ALL TESTS PASSED")
        else:
            print(f"✗ {description} - SOME TESTS FAILED")
        
        return success
        
    except Exception as e:
        print(f"✗ ERROR running {description}: {e}")
        return False


def main():
    """Run all test files"""
    print()
    print("=" * 80)
    print("SNOWFLAKE COMMENT PARSING - TEST RUNNER")
    print("Issue #1763: Support for // comments in Snowflake")
    print("=" * 80)
    
    test_files = [
        ("minimal_repro.py", "Minimal Reproduction (Issue #1763)"),
        ("issue_test.py", "Comprehensive Test Suite"),
    ]
    
    results = []
    for filepath, description in test_files:
        success = run_test_file(filepath, description)
        results.append((description, success))
    
    # Final summary
    print()
    print("=" * 80)
    print("OVERALL TEST SUMMARY")
    print("=" * 80)
    
    all_passed = True
    for description, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {description}")
        if not success:
            all_passed = False
    
    print()
    passed_count = sum(1 for _, success in results if success)
    total_count = len(results)
    print(f"Test Files: {passed_count}/{total_count} passed")
    
    if all_passed:
        print()
        print("🎉 ALL TESTS PASSED! The bug fix is working correctly.")
    else:
        print()
        print("❌ SOME TESTS FAILED. Please review the output above.")
    
    print("=" * 80)
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
