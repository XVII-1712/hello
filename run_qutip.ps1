# Define the project path and virtual environment path
$projectPath = "C:\Users\mike\qlf_project\backend\backend"
$venvPath = "$projectPath\qutip_env"

# Navigate to the project directory
cd $projectPath

# Create the virtual environment if it does not exist
if (-Not (Test-Path -Path $venvPath)) {
    python -m venv $venvPath
}

# Activate the virtual environment
& "$venvPath\Scripts\Activate"

# Install QuTiP and Matplotlib if not already installed
pip show qutip
if ($LASTEXITCODE -ne 0) {
    pip install qutip
}

pip show matplotlib
if ($LASTEXITCODE -ne 0) {
    pip install matplotlib
}

# Run the QuTiP script
$scriptPath = "$projectPath\your_script.py"
python $scriptPath

# Deactivate the virtual environment (optional)
# & "$venvPath\Scripts\Deactivate"
