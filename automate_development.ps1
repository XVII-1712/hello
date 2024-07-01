# Define the project path and virtual environment path
$projectPath = "C:\Users\mike\qlf_project\backend\backend"
$venvPath = "$projectPath\qlf_env"

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

# Activate the virtual environment (PowerShell syntax)
& "$venvPath\Scripts\Activate.ps1"

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
python $scriptPath

# Add, commit, and push any changes back to version control
git add .
git commit -m "Automated update: $(Get-Date)"
git push origin main

# Optionally run repository maintenance commands
git prune
git gc
