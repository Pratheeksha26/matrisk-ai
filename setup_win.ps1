# MatRisk AI Windows Setup Script
Write-Host "Starting MatRisk AI Environment Setup..." -ForegroundColor Cyan

# 1. Install Torch first (Required for building extensions)
Write-Host "Step 1: Installing PyTorch..." -ForegroundColor Yellow
pip install torch --index-url https://download.pytorch.org/whl/cpu

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing Torch. Please check your internet connection." -ForegroundColor Red
    exit
}

# 2. Install the rest of the requirements
Write-Host "Step 2: Installing remaining dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing dependencies. Some components like torch-geometric extensions might require C++ Build Tools." -ForegroundColor Red
    Write-Host "Try: pip install torch-geometric (skipping extensions if build fails)" -ForegroundColor Gray
} else {
    Write-Host "✅ Setup Complete! You can now run 'make data' or start the pipeline." -ForegroundColor Green
}
