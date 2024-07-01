# Define paths
$projectPath = "C:\Users\mike\qlf_project\backend\backend"
$venvPath = "$projectPath\qutip_env"

# Navigate to project directory
cd $projectPath

# Activate the virtual environment
& "$venvPath\Scripts\Activate.ps1"

# Check if qutip is installed, install if not
pip show qutip
if ($LASTEXITCODE -ne 0) {
    pip install qutip
}

# Check if matplotlib is installed, install if not
pip show matplotlib
if ($LASTEXITCODE -ne 0) {
    pip install matplotlib
}

# Pull latest code from git repository
git pull origin main

# Additional script logic (e.g., running tests, building, etc.)

# Add, commit, and push any changes to the repository
git add .
git commit -m "Automated update: $(Get-Date -Format 'MM/dd/yyyy HH:mm:ss')"
git push origin main
