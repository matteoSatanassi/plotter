@echo off

cd ..\

    ::Attivazione ambiente virtuale
call .venv\Scripts\activate

.venv\Scripts\python.exe IdVd_plotter\main.py

    ::Mantiene il terminale aperto dopo l'esecuzione
pause