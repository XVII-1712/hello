# Define the project path and virtual environment path
$projectPath = "C:\Users\mike\qlf_project\backend\backend"
$venvPath = "$projectPath\qutip_env"

# Navigate to the project directory
cd $projectPath

# Initialize Git repository if not already a Git repository
if (-Not (Test-Path -Path ".git")) {
    git init
    git remote add origin https://github.com/XVII-1712/hello.git
}

# Create the virtual environment if it does not exist
if (-Not (Test-Path -Path $venvPath)) {
    python -m venv $venvPath
}

# Activate the virtual environment
$activateScript = "$venvPath\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "Error: Activate.ps1 script not found in $venvPath\Scripts"
    exit 1
}

# Install necessary packages if not already installed
pip show qutip
if ($LASTEXITCODE -ne 0) {
    pip install qutip
}

pip show matplotlib
if ($LASTEXITCODE -ne 0) {
    pip install matplotlib
}

# Pull the latest code from version control
try {
    git fetch origin
    $branchExists = git branch -r | Select-String -Pattern "origin/main"
    if ($branchExists) {
        git pull origin main
    } else {
        Write-Host "Remote branch 'main' not found."
    }
} catch {
    Write-Host "Error pulling from remote repository: $_"
}

# Run the QuTiP script
$scriptPath = "$projectPath\complex_simulation.py"
if (Test-Path $scriptPath) {
    python $scriptPath
} else {
    Write-Host "Error: QuTiP script not found at $scriptPath"
    exit 1
}

# Add, commit, and push any changes back to version control
git add .
git commit -m "Automated update: $(Get-Date)"
git push origin main

# Optionally run repository maintenance commands
git prune
git gc
