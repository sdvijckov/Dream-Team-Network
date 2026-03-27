# 📚 Dog Wisdom Datasets

Система подготовки, разметки и векторизации текстовых данных для проекта **"Собачья мудрость. Секрет счастья"**.

## 🎯 Назначение

Автоматическая обработка текстовых произведений:
- Загрузка из различных форматов (.txt, .md, .docx)
- Очистка от шума и артефактов
- Автоматическая разметка (персонажи, темы, эмоции)
- Создание векторных представлений для семантического поиска
- Подготовка датасетов для обучения нейросетей и LoRA адаптеров

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Перейти в папку проекта
cd "D:\Projects python\Dream Team Network\datasets"

# Создать виртуальное окружение
python -m venv venv

# Активировать (PowerShell)
.\venv\Scripts\Activate.ps1

# Или cmd
venv\Scripts\activate.bat

# Обновить pip
python -m pip install --upgrade pip

# Установить зависимости
pip install -r requirements.txt

# Скачать NLTK данные
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

### 2. Подготовка данных

Скопируй тексты в папку `raw/` в соответствующие подпапки:

```
raw/
├── books/          # Книги, повести
├── stories/        # Рассказы, притчи
├── quotes/         # Цитаты, афоризмы
├── essays/         # Философские эссе
├── dialogs/        # Диалоги
└── drafts/         # Черновики
```

**Форматы файлов:** .txt, .md, .docx

### 3. Запуск обработки

**Базовая обработка (без векторов):**

```bash
python cli.py process --input ./raw --output ./processed --no-vectors
```

**Полная обработка (с векторизацией):**

```bash
python cli.py process --input ./raw --output ./processed --vectors ./vectors
```

---

## 📖 Команды CLI

### process - Обработка данных

```bash
# Базовая обработка
python cli.py process

# С указанием путей
python cli.py process -i ./raw -o ./processed -v ./vectors

# Без векторизации (быстрее)
python cli.py process --no-vectors

# Только статистика
python cli.py process --stats-only
```

**Опции:**
- `-i, --input` - Папка с сырыми данными (по умолчанию: ./raw)
- `-o, --output` - Папка для JSON (по умолчанию: ./processed)
- `-v, --vectors` - Папка для ChromaDB (по умолчанию: ./vectors)
- `--no-vectors` - Не создавать векторы
- `--stats-only` - Только показать статистику

---

### test - Тестирование одного файла

```bash
python cli.py test ./raw/books/глава1.txt
```

Покажет:
- Информацию о файле
- Результат очистки
- Автоматические теги
- Предпросмотр текста

---

### db_stats - Статистика векторной базы

```bash
python cli.py db_stats --path ./vectors
```

---

### db_reset - Очистка векторной базы

```bash
python cli.py db_reset --path ./vectors
```

⚠️ **Внимание:** Удаляет все данные из ChromaDB!

---

### info - Информация о системе

```bash
python cli.py info
```

Покажет версию Python, ОС и статус установленных зависимостей.

---

## 📊 Формат выходных данных

### JSON файл (в папке processed/)

```json
{
  "id": "uuid-идентификатор",
  "text": "полный очищенный текст",
  "metadata": {
    "source_file": "имя_файла.txt",
    "source_path": "полный/путь/к/файлу",
    "extension": ".txt",
    "content_type": "book|story|quote|essay|dialog|draft",
    "language": "ru|en",
    "word_count": 1500,
    "character_count": 8000,
    "processed_date": "2026-03-21T10:30:00"
  },
  "tags": {
    "characters": ["Смельчак", "Генрих"],
    "themes": ["дружба", "верность"],
    "emotions": ["радость", "надежда"]
  },
  "agent_profile": "oleg|sheldon|genrikh|smelchak"
}
```

### ChromaDB (в папке vectors/)

Векторное хранилище для семантического поиска.

**Использование в коде:**

```python
from src.vectorizer import Vectorizer, ChromaDBManager

# Инициализация
vectorizer = Vectorizer()
db = ChromaDBManager('./vectors')

# Поиск по тексту
results = db.search_by_text("дружба и верность", vectorizer, n_results=5)

# Результаты
for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    print(f"Текст: {doc[:100]}...")
    print(f"Метаданные: {meta}")
```

---

## 🏷️ Автоматическая разметка

Система автоматически определяет:

### Тип контента
- `book` - книги, повести (5000+ символов)
- `story` - рассказы, притчи (500-5000 символов)
- `quote` - цитаты, афоризмы (<500 символов)
- `essay` - философские эссе
- `dialog` - диалоги
- `draft` - черновики

### Персонажи
Смельчак, Генрих, Эльза, Григорий, Максим, Петр, Нелли, Катя, Грета, Багги, Родион

### Темы
дружба, верность, предназначение, любовь, счастье, страх, смерть, жизнь, обучение, семья, потеря, надежда, память, доверие

### Эмоции
радость, грусть, страх, гнев, надежда, любовь, тревога, спокойствие, удивление, благодарность

### Профиль агента
- `oleg` - авторский контент (по умолчанию)
- `sheldon` - англоязычный контент
- `genrikh` - с участием Генриха
- `smelchak` - с участием Смельчака

---

## 🛠️ Структура проекта

```
datasets/
├── raw/                    # Сырые данные (копировать с Яндекс.Диска)
│   ├── books/
│   ├── stories/
│   ├── quotes/
│   ├── essays/
│   ├── dialogs/
│   └── drafts/
├── processed/              # Обработанные JSON файлы
├── vectors/                # ChromaDB векторное хранилище
├── src/                    # Исходный код
│   ├── loader.py           # Загрузчик файлов
│   ├── cleaner.py          # Очистка текста
│   ├── tagger.py           # Автоматическая разметка
│   ├── vectorizer.py       # Векторизация и ChromaDB
│   └── pipeline.py         # Основной пайплайн
├── cli.py                  # Консольный интерфейс
├── requirements.txt        # Зависимости
├── .env.example            # Пример переменных окружения
└── README.md               # Эта документация
```

---

## 🔧 Настройка

### Переменные окружения (.env файл)

Создайте файл `.env` на основе `.env.example`:

```env
# Путь к хранилищу ChromaDB
CHROMA_DB_PATH=./vectors

# Папка с сырыми данными
RAW_DATA_PATH=./raw

# Папка для обработанных данных
PROCESSED_DATA_PATH=./processed

# API ключи (когда понадобятся)
# GEMINI_API_KEY=...
# OPENAI_API_KEY=...
```

---

## 📝 Примеры использования

### 1. Первичная обработка большой коллекции

```bash
# Без векторизации для скорости
python cli.py process -i ./raw -o ./processed --no-vectors

# Просмотр статистики
python cli.py process --stats-only
```

### 2. Полная обработка с векторизацией

```bash
# С созданием векторов для поиска
python cli.py process -i ./raw -o ./processed -v ./vectors
```

### 3. Тестирование перед обработкой

```bash
# Протестировать на одном файле
python cli.py test ./raw/quotes/цитаты.txt

# Проверить систему
python cli.py info
```

---

## ⚠️ Возможные проблемы

### Ошибка при установке зависимостей

```bash
# Обновить pip
python -m pip install --upgrade pip

# Установить по отдельности
pip install chromadb
pip install sentence-transformers
```

### NLTK требует данные

```bash
python -c "import nltk; nltk.download('all')"
```

### ChromaDB не создаётся

Удалите папку `vectors/` и запустите заново.

---

## 🎯 Следующие шаги

После обработки данных:

1. **Проверьте результат** в папке `processed/`
2. **Протестируйте поиск** через ChromaDB
3. **Используйте датасеты** для:
   - Обучения LoRA адаптеров
   - RAG системы
   - Анализа контента
   - Интеграции с Dream Team

---

## 📞 Поддержка

Вопросы и предложения: [контакты]

---

**Версия:** 0.1.0  
**Дата:** Март 2026  
**Проект:** "Собачья мудрость. Секрет счастья"
