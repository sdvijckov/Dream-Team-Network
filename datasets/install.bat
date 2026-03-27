@echo off
chcp 65001 >nul
echo ============================================================
echo   🚀 Установка Dog Wisdom Datasets
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

echo Создание виртуального окружения...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Ошибка создания venv
        pause
        exit /b 1
    )
    echo ✅ venv создано
) else (
    echo ✅ venv уже существует
)
echo.

echo Активация venv...
call venv\Scripts\activate.bat
echo.

echo Обновление pip...
python -m pip install --upgrade pip
echo.

echo Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)
echo.

echo Загрузка NLTK данных...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
echo.

echo Создание папок...
if not exist "raw\books" mkdir "raw\books"
if not exist "raw\stories" mkdir "raw\stories"
if not exist "raw\quotes" mkdir "raw\quotes"
if not exist "raw\essays" mkdir "raw\essays"
if not exist "raw\dialogs" mkdir "raw\dialogs"
if not exist "raw\drafts" mkdir "raw\drafts"
if not exist "processed" mkdir "processed"
if not exist "vectors" mkdir "vectors"
echo ✅ Папки созданы
echo.

if not exist ".env" (
    copy .env.example .env >nul
    echo ✅ .env создан
)
echo.

echo ============================================================
echo   ✨ Установка завершена!
echo ============================================================
echo.
echo 📝 Следующие шаги:
echo 1. Скопируйте тексты в папку raw\
echo 2. Запустите обработку: python cli.py process
echo 3. Для справки: python cli.py --help
echo.
pause
