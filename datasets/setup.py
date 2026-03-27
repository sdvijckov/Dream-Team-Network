"""
Dog Wisdom Datasets - инициализация проекта.
Автоматическая установка зависимостей и настройка.
"""

import subprocess
import sys
from pathlib import Path


def print_header(text: str):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def run_command(command: list, description: str):
    print(f"⚙️  {description}...")
    try:
        subprocess.run(command, check=True)
        print(f"✅ {description} - готово")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ошибка: {e}")
        return False
    except Exception as e:
        print(f"❌ {description} - ошибка: {e}")
        return False


def main():
    print_header("🚀 Установка Dog Wisdom Datasets")
    
    # Проверка Python
    print(f"Python версия: {sys.version}")
    print(f"Python путь: {sys.executable}\n")
    
    # Обновление pip
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        "Обновление pip"
    )
    
    # Установка зависимостей
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    if requirements_path.exists():
        run_command(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
            "Установка зависимостей из requirements.txt"
        )
    else:
        print("❌ requirements.txt не найден!")
        return
    
    # Скачивание NLTK данных
    print("\n⚙️  Скачивание NLTK данных...")
    try:
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        print("✅ NLTK данные загружены")
    except Exception as e:
        print(f"⚠️  NLTK: {e}")
    
    # Создание папок
    print("\n⚙️  Создание структуры папок...")
    
    folders = [
        'raw/books', 'raw/stories', 'raw/quotes',
        'raw/essays', 'raw/dialogs', 'raw/drafts',
        'processed', 'vectors'
    ]
    
    base_path = Path(__file__).parent
    
    for folder in folders:
        path = base_path / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Создана папка: {folder}")
    
    # Создание .env файла
    env_example = base_path / ".env.example"
    env_file = base_path / ".env"
    
    if env_example.exists() and not env_file.exists():
        with open(env_example, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n✅ Создан файл .env")
    
    # Проверка установки
    print_header("🧪 Проверка установки")
    
    from cli import info as cli_info
    # Запускаем команду info
    from click.testing import CliRunner
    from cli import cli
    
    runner = CliRunner()
    result = runner.invoke(cli, ['info'])
    print(result.output)
    
    print_header("✨ Установка завершена!")
    
    print("\n📝 Следующие шаги:")
    print("1. Скопируйте тексты в папку raw/")
    print("2. Запустите обработку: python cli.py process")
    print("3. Проверьте результат в папке processed/")
    print("\n📖 Подробная документация в README.md\n")


if __name__ == '__main__':
    main()
