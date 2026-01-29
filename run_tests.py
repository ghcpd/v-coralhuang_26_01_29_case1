"""
Test Runner - Executes all test files for Snowflake comment parsing fix
"""

import subprocess
import sys
from pathlib import Path


def run_test(test_file, description):
    """Run a single test file and return success status"""
    print()
    print("=" * 70)
    print(f"Running: {description}")
    print(f"File: {test_file}")
    print("=" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=False,
            text=True,
            cwd=Path(__file__).parent
        )
        
        success = result.returncode == 0
        status = "✓ PASSED" if success else "✗ FAILED"
        print()
        print(f"{status}: {description}")
        return success
        
    except Exception as e:
        print(f"✗ FAILED with exception: {e}")
        return False


def main():
    """Run all test files"""
    print()
    print("=" * 70)
    print("SNOWFLAKE COMMENT PARSING - FULL TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("minimal_repro.py", "Minimal Reproduction (Issue #1763)"),
        ("issue_test.py", "Basic Comment Style Tests"),
        ("test_comprehensive.py", "Comprehensive Test Suite"),
    ]
    
    results = []
    for test_file, description in tests:
        success = run_test(test_file, description)
        results.append((description, success))
    
    # Summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for description, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {description}")
    
    total_passed = sum(1 for _, success in results if success)
    print()
    print(f"Total: {total_passed}/{len(results)} test files passed")
    print("=" * 70)
    
    # Exit with appropriate code
    all_passed = all(success for _, success in results)
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
