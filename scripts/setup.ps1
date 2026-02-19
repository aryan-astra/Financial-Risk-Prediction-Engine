# =====================================================
# setup.ps1  -  Complete Project Setup Script (Windows)
# =====================================================
# Run this script to set up the entire project locally.
# Usage: .\scripts\setup.ps1
# =====================================================

param(
    [switch]$SkipDB,
    [switch]$SkipML,
    [switch]$SkipFrontend
)

$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Pre-Delinquency Intervention Engine Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# --- Step 1: Python virtual environment ---
Write-Host "[1/5] Setting up Python virtual environment..." -ForegroundColor Yellow
if (-Not (Test-Path "$ProjectRoot\.venv")) {
    python -m venv "$ProjectRoot\.venv"
    Write-Host "  -> Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "  -> Virtual environment already exists." -ForegroundColor Green
}

# Activate venv
$activateScript = "$ProjectRoot\.venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "  -> Virtual environment activated." -ForegroundColor Green
}

# --- Step 2: Install Python dependencies ---
Write-Host ""
Write-Host "[2/5] Installing Python dependencies..." -ForegroundColor Yellow
pip install -r "$ProjectRoot\ml\requirements.txt" -q
pip install -r "$ProjectRoot\backend\requirements.txt" -q
Write-Host "  -> Python dependencies installed." -ForegroundColor Green

# --- Step 3: Database setup ---
if (-Not $SkipDB) {
    Write-Host ""
    Write-Host "[3/5] Setting up MySQL database..." -ForegroundColor Yellow
    Write-Host "  -> Please ensure MySQL is running on localhost:3306" -ForegroundColor DarkGray
    
    # Copy .env if not exists
    $envFile = "$ProjectRoot\backend\.env"
    if (-Not (Test-Path $envFile)) {
        Copy-Item "$ProjectRoot\backend\.env.example" $envFile
        Write-Host "  -> Created backend\.env from .env.example" -ForegroundColor Green
        Write-Host "  -> IMPORTANT: Update the DB_PASSWORD in backend\.env!" -ForegroundColor Red
    }

    Write-Host "  -> Run the following to create the database:" -ForegroundColor DarkGray
    Write-Host "     mysql -u root -p < scripts\setup_db.sql" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "[3/5] Skipping database setup." -ForegroundColor DarkGray
}

# --- Step 4: Train ML model ---
if (-Not $SkipML) {
    Write-Host ""
    Write-Host "[4/5] Training ML model..." -ForegroundColor Yellow
    Push-Location "$ProjectRoot\ml"
    python train.py
    Pop-Location
    Write-Host "  -> Model training complete." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[4/5] Skipping ML training." -ForegroundColor DarkGray
}

# --- Step 5: Frontend setup ---
if (-Not $SkipFrontend) {
    Write-Host ""
    Write-Host "[5/5] Setting up Next.js frontend..." -ForegroundColor Yellow
    Push-Location "$ProjectRoot\frontend"
    
    # Copy .env.local if not exists
    $frontendEnv = "$ProjectRoot\frontend\.env.local"
    if (-Not (Test-Path $frontendEnv)) {
        Copy-Item "$ProjectRoot\frontend\.env.local.example" $frontendEnv
        Write-Host "  -> Created frontend\.env.local" -ForegroundColor Green
    }

    npm install
    Pop-Location
    Write-Host "  -> Frontend dependencies installed." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[5/5] Skipping frontend setup." -ForegroundColor DarkGray
}

# --- Done ---
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application:" -ForegroundColor White
Write-Host "  1. Start MySQL and ensure the database exists" -ForegroundColor DarkGray
Write-Host "  2. Backend:  cd backend && uvicorn main:app --reload" -ForegroundColor DarkGray
Write-Host "  3. Frontend: cd frontend && npm run dev" -ForegroundColor DarkGray
Write-Host "  4. Open:     http://localhost:3000" -ForegroundColor DarkGray
Write-Host ""
