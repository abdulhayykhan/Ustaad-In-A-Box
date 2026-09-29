@echo off
title Ustaad-in-a-Box

echo.
echo  ==========================================
echo   Ustaad-in-a-Box v0.1 -- Rocketathon 2026
echo  ==========================================
echo.

:: Step 1: Check dependencies (offline safe)
echo [1/3] Checking dependencies...
python -c "import fastapi, uvicorn, yaml, pydantic" 2>nul
if errorlevel 1 (
    echo Installing missing packages...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ERROR: pip install failed and dependencies are missing.
        pause
        exit /b 1
    )
) else (
    echo Dependencies verified. Running offline.
)

:: Step 2: Run tests
echo.
echo [2/3] Running rule engine tests...
python -X utf8 test_engine.py
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed. Check test output above.
    echo Press any key to start the server anyway, or Ctrl+C to abort.
    pause
)

:: Step 3: Start server
echo.
echo [3/3] Starting server...
echo.
echo  Open your browser at:  http://localhost:8000
echo  (Also accessible from phone on same Wi-Fi: http://YOUR-IP:8000)
echo.
echo  Press Ctrl+C to stop.
echo.

python main.py

pause
