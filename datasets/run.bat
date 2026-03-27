@echo off
chcp 65001 >nul
echo ============================================================
echo   📚 Dog Wisdom Datasets - Обработка данных
echo ============================================================
echo.

call venv\Scripts\activate.bat

if "%~1"=="" (
    echo Использование:
    echo   run.bat              - полная обработка с векторами
    echo   run.bat --no-vectors - без векторизации
    echo   run.bat --help       - справка
    echo.
    echo Запуск обработки...
    echo.
)

python cli.py process %*

echo.
pause
