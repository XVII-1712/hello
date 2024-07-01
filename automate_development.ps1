# Define paths
$projectPath = "C:\Users\mike\qlf_project\backend\backend"
$venvPath = "$projectPath\qutip_env"

# Navigate to project directory
cd $projectPath

# Activate the virtual environment
try {
    & "$venvPath\Scripts\Activate.ps1"
} catch {
    Write-Error "Failed to activate virtual environment: $_"
    exit 1
}

# Check if qutip is installed, install if not
try {
    pip show qutip
    if ($LASTEXITCODE -ne 0) {
        pip install qutip
    }
} catch {
    Write-Error "Failed to check/install qutip: $_"
    exit 1
}

# Check if matplotlib is installed, install if not
try {
    pip show matplotlib
    if ($LASTEXITCODE -ne 0) {
        pip install matplotlib
    }
} catch {
    Write-Error "Failed to check/install matplotlib: $_"
    exit 1
}

# Pull latest code from git repository
try {
    git pull origin main
} catch {
    Write-Error "Failed to pull latest code from repository: $_"
    exit 1
}

# Run unit tests
try {
    pytest
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Unit tests failed"
        exit 1
    }
} catch {
    Write-Error "Failed to run unit tests: $_"
    exit 1
}

# Run code quality checks
try {
    flake8 .
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Code quality checks failed"
        exit 1
    }
} catch {
    Write-Error "Failed to run code quality checks: $_"
    exit 1
}

# Add, commit, and push any changes to the repository
try {
    git add .
    git commit -m "Automated update: $(Get-Date -Format 'MM/dd/yyyy HH:mm:ss')"
    git push origin main
} catch {
    Write-Error "Failed to commit and push changes: $_"
    exit 1
}

Write-Output "Script executed successfully"
