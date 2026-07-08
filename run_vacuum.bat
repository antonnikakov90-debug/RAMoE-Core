@echo off
title RAMoE Adaptive Echo Chamber Terminal
color 0B

echo ============================================================
echo   ЗАПУСК АППАРАТА СЕМАНТИЧЕСКОГО ЭХА RAMoE
echo ============================================================
echo.

:: 1. Инициализация путей Anaconda (стандартный путь установки для Windows)
set "CONDAPATH=C:\Users\%USERNAME%\anaconda3"
if not exist "%CONDAPATH%\Scripts\activate.bat" (
    set "CONDAPATH=C:\ProgramData\anaconda3"
)

:: 2. Активация среды Conda base
echo [CONDA] Активация базового CUDA-окружения...
call "%CONDAPATH%\Scripts\activate.bat" base

:: 3. Переход в рабочую директорию полигона RAMoE
echo [SYSTEM] Переход на физический уровень диска E:...
E:
cd "E:\RAMoE"

:: 4. Запуск квантового интерактивного ядра
echo [CUDA] Запуск Ложного Вакуума диалога...
echo ------------------------------------------------------------
python interface_vacuum.py

echo.
echo ============================================================
echo   Поле сколлапсировало. Сессия закрыта.
echo ============================================================
pause
