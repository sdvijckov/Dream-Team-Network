@echo off
chcp 65001 >nul
echo ============================================================
echo   🐾 Dream Team Network - Установка всех подпроектов
echo ============================================================
echo.

echo Проверка Python...
python --version
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.10+
    pause
    exit /b 1
)
echo.

echo ============================================================
echo   📊 Установка datasets
echo ============================================================
echo.

if exist "datasets" (
    cd datasets
    
    if exist "install.bat" (
        echo Запуск install.bat для datasets...
        call install.bat
    ) else (
        echo ⚠️  install.bat не найден в datasets
    )
    
    cd ..
) else (
    echo ⚠️  Папка datasets не найдена!
)

echo.
echo ============================================================
echo   ✨ Установка завершена!
echo ============================================================
echo.
echo 📝 Следующие шаги:
echo 1. Перейти в datasets: cd datasets
echo 2. Скопировать тексты в raw/
echo 3. Запустить обработку: python cli.py process
echo.
echo 📖 Документация: datasets\README.md
echo.
pause
