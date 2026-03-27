"""
Консольный интерфейс для управления пайплайном обработки данных.
"""

import click
import sys
from pathlib import Path
from datetime import datetime

# Добавляем src в path для импортов
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import DataPipeline


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """📚 Dog Wisdom Datasets - Система подготовки датасетов
    
    Инструмент для загрузки, очистки, разметки и векторизации
    текстовых данных проекта "Собачья мудрость".
    """
    pass


@cli.command()
@click.option('--input', '-i', 'input_path', 
              default='./raw',
              help='Папка с сырыми данными')
@click.option('--output', '-o', 'output_path',
              default='./processed',
              help='Папка для обработанных JSON файлов')
@click.option('--vectors', '-v', 'vector_path',
              default='./vectors',
              help='Папка для ChromaDB')
@click.option('--no-vectors', is_flag=True,
              help='Не создавать векторные представления')
@click.option('--stats-only', is_flag=True,
              help='Только показать статистику без обработки')
def process(input_path, output_path, vector_path, no_vectors, stats_only):
    """🔄 Запустить обработку данных
    
    Пример:
        python cli.py process --input ./raw --output ./processed --vectors
    """
    if stats_only:
        # Показать статистику без обработки
        click.echo("\n📊 Статистика папок:")
        click.echo(f"   Сырые данные: {input_path}")
        click.echo(f"   Обработанные: {output_path}")
        click.echo(f"   Векторы: {vector_path}")
        
        # Посчитать файлы
        raw_path = Path(input_path)
        if raw_path.exists():
            files = list(raw_path.rglob('*.txt')) + \
                    list(raw_path.rglob('*.md')) + \
                    list(raw_path.rglob('*.docx'))
            click.echo(f"\n📁 Найдено файлов: {len(files)}")
        else:
            click.echo(f"\n⚠️  Папка не найдена: {input_path}")
        
        return
    
    # Запуск пайплайна
    use_vectors = not no_vectors
    
    if use_vectors:
        click.echo("\n⚠️  Векторизация включена. Это займёт время.")
        click.echo("   Для отключения используйте --no-vectors\n")
    
    pipeline = DataPipeline(
        raw_path=input_path,
        processed_path=output_path,
        vector_path=vector_path,
        use_vectors=use_vectors
    )
    
    stats = pipeline.run()
    
    # Сохранить лог
    log_file = Path(output_path) / f"process_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Дата: {datetime.now().isoformat()}\n")
        f.write(f"Входная папка: {input_path}\n")
        f.write(f"Выходная папка: {output_path}\n")
        f.write(f"Векторизация: {'включена' if use_vectors else 'отключена'}\n\n")
        f.write(f"Успешно: {stats['processed_files']}\n")
        f.write(f"Ошибок: {stats['failed_files']}\n")
        f.write(f"Всего символов: {stats['total_characters']:,}\n")
    
    click.echo(f"\n💾 Лог сохранён: {log_file}")


@cli.command()
@click.argument('file_path')
def test(file_path):
    """🧪 Протестировать обработку одного файла
    
    Пример:
        python cli.py test ./raw/books/test.txt
    """
    from src.loader import TextLoader
    from src.cleaner import TextCleaner
    from src.tagger import TextTagger
    
    click.echo(f"\n🔍 Тестирование файла: {file_path}\n")
    
    # Загрузка
    loader = TextLoader()
    try:
        data = loader.load_file(file_path)
        click.echo(f"✅ Загружено: {data['source_file']}")
        click.echo(f"   Расширение: {data['extension']}")
        click.echo(f"   Длина: {len(data['text'])} символов\n")
    except Exception as e:
        click.echo(f"❌ Ошибка загрузки: {e}\n")
        return
    
    # Очистка
    cleaner = TextCleaner()
    cleaned = cleaner.clean(data['text'])
    click.echo(f"✅ После очистки: {len(cleaned)} символов")
    click.echo(f"   Удалено: {len(data['text']) - len(cleaned)} символов\n")
    
    # Разметка
    tagger = TextTagger()
    tags = tagger.tag(cleaned, file_path)
    
    click.echo("🏷️  Теги:")
    click.echo(f"   Язык: {tags['language']}")
    click.echo(f"   Тип: {tags['content_type']}")
    click.echo(f"   Персонажи: {', '.join(tags['characters']) if tags['characters'] else 'не найдены'}")
    click.echo(f"   Темы: {', '.join(tags['themes']) if tags['themes'] else 'не найдены'}")
    click.echo(f"   Эмоции: {', '.join(tags['emotions']) if tags['emotions'] else 'не найдены'}")
    click.echo(f"   Агент: {tags['agent_profile']}\n")
    
    # Предпросмотр текста
    click.echo("📝 Предпросмотр (первые 200 символов):")
    click.echo(f"   {cleaned[:200]}...\n")


@cli.command()
@click.option('--path', '-p', 'db_path',
              default='./vectors',
              help='Путь к базе ChromaDB')
def db_stats(db_path):
    """📊 Показать статистику векторной базы"""
    from src.vectorizer import ChromaDBManager
    
    try:
        db = ChromaDBManager(db_path)
        stats = db.get_stats()
        
        click.echo("\n📊 Статистика ChromaDB:")
        click.echo(f"   Путь: {stats['path']}")
        click.echo(f"   Коллекция: {stats['name']}")
        click.echo(f"   Документов: {stats['count']}\n")
        
    except Exception as e:
        click.echo(f"❌ Ошибка: {e}\n")


@cli.command()
@click.option('--path', '-p', 'db_path',
              default='./vectors',
              help='Путь к базе ChromaDB')
@click.confirmation_option(prompt='Вы уверены? Это удалит все данные!')
def db_reset(db_path):
    """🗑️  Очистить векторную базу"""
    from src.vectorizer import ChromaDBManager
    
    try:
        db = ChromaDBManager(db_path)
        db.reset()
        click.echo("✅ База данных очищена\n")
        
    except Exception as e:
        click.echo(f"❌ Ошибка: {e}\n")


@cli.command()
def info():
    """ℹ️  Показать информацию о системе"""
    import sys
    import platform
    
    click.echo("\nℹ️  Информация о системе")
    click.echo("="*40)
    click.echo(f"Python: {sys.version}")
    click.echo(f"OS: {platform.platform()}")
    click.echo(f"Платформа: {platform.machine()}\n")
    
    # Проверка зависимостей
    click.echo("📦 Зависимости:")
    
    deps = {
        'chromadb': 'ChromaDB',
        'sentence_transformers': 'Sentence Transformers',
        'nltk': 'NLTK',
        'pymorphy3': 'PyMorphy3',
        'docx': 'python-docx',
        'tqdm': 'tqdm',
        'rich': 'Rich',
        'click': 'Click',
    }
    
    for module, name in deps.items():
        try:
            __import__(module)
            click.echo(f"   ✅ {name}")
        except ImportError:
            click.echo(f"   ❌ {name} (не установлен)")
    
    click.echo()


if __name__ == '__main__':
    cli()
