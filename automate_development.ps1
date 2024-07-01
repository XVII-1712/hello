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

# Additional script logic (e.g., running tests, building, etc.)
# Add your commands here

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
