param(
    [string]$Py = $null
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not $Py) {
    $venvPy = Join-Path $root ".venv\Scripts\python.exe"
    if (Test-Path $venvPy) {
        $Py = $venvPy
    } else {
        $Py = "python"
    }
}

Write-Host "Using Python: $Py"

try {
    & $Py -m pytest --version | Out-Null
} catch {
    Write-Host "pytest not found; installing..." -ForegroundColor Yellow
    & $Py -m pip install pytest
}

& $Py -m pytest -q
