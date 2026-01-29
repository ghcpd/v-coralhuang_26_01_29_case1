#!/usr/bin/env pwsh
# PowerShell Test Runner for Snowflake Comment Parsing Fix

Write-Host ""
Write-Host ("=" * 70)
Write-Host "SNOWFLAKE COMMENT PARSING - FULL TEST SUITE"
Write-Host ("=" * 70)
Write-Host ""

$tests = @(
    @{File = "minimal_repro.py"; Description = "Minimal Reproduction (Issue #1763)"},
    @{File = "issue_test.py"; Description = "Basic Comment Style Tests"},
    @{File = "test_comprehensive.py"; Description = "Comprehensive Test Suite"}
)

$results = @()

foreach ($test in $tests) {
    Write-Host ""
    Write-Host ("=" * 70)
    Write-Host "Running: $($test.Description)"
    Write-Host "File: $($test.File)"
    Write-Host ("=" * 70)
    Write-Host ""
    
    try {
        $result = & python $test.File
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-Host ""
            Write-Host "✓ PASSED: $($test.Description)" -ForegroundColor Green
            $results += @{Description = $test.Description; Success = $true}
        } else {
            Write-Host ""
            Write-Host "✗ FAILED: $($test.Description)" -ForegroundColor Red
            $results += @{Description = $test.Description; Success = $false}
        }
    }
    catch {
        Write-Host ""
        Write-Host "✗ FAILED with exception: $_" -ForegroundColor Red
        $results += @{Description = $test.Description; Success = $false}
    }
}

# Summary
Write-Host ""
Write-Host ("=" * 70)
Write-Host "TEST SUMMARY"
Write-Host ("=" * 70)

$passed = 0
foreach ($result in $results) {
    if ($result.Success) {
        Write-Host "✓ PASSED: $($result.Description)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "✗ FAILED: $($result.Description)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Total: $passed/$($results.Count) test files passed"
Write-Host ("=" * 70)
Write-Host ""

# Exit with appropriate code
if ($passed -eq $results.Count) {
    exit 0
} else {
    exit 1
}
