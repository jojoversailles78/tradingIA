@echo off
title TradingIA - Lancement
color 0A
echo.
echo  ================================
echo   TradingIA - Demarrage en cours
echo  ================================
echo.
echo [1/2] Lancement du Backend...
start "TradingIA Backend" cmd /k "cd C:\tradingIA\backend && venv\Scripts\activate.bat && python -W ignore -m uvicorn app.main:app --port 8000 --host 0.0.0.0"
echo Attente demarrage backend...
timeout /t 5 /nobreak >nul
echo [2/2] Ouverture du navigateur...
start http://localhost:8000
echo.
echo  ================================
echo   TradingIA est lance !
echo   Dashboard : http://localhost:8000
echo   Agent IA  : http://localhost:8000/agent
echo  ================================
echo.
pause