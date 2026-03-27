# 🚀 Быстрый старт Dream Team Network

## 📋 Что у нас есть

```
Dream Team Network/
├── datasets/           ✅ Готово - Система подготовки данных
│   ├── src/           - Исходный код (loader, cleaner, tagger, vectorizer)
│   ├── raw/           - Сюда копировать тексты
│   ├── processed/     - Обработанные JSON
│   ├── vectors/       - ChromaDB
│   ├── cli.py         - Консольный интерфейс
│   ├── install.bat    - Автоматическая установка
│   └── README.md      - Документация
├── models/            🔲 В разработке - LoRA адаптеры
├── api/               🔲 В разработке - Сервер
├── install_all.bat    - Установка всех подпроектов
└── README.md          - Общая документация
```

---

## ⚡ Установка и запуск (3 шага)

### Шаг 1: Установка зависимостей

**Вариант A: Автоматически (рекомендуется)**

Запустить `install.bat` в папке `datasets/`:
```bash
cd "D:\Projects python\Dream Team Network\datasets"
install.bat
```

**Вариант B: Вручную**
```bash
cd "D:\Projects python\Dream Team Network\datasets"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

---

### Шаг 2: Копирование текстов

Скопируй тексты из Яндекс.Диска в папку `raw/`:

```
raw/
├── books/      - Книги, повести ("Собачье счастье")
├── stories/    - Рассказы, притчи
├── quotes/     - Цитаты (уже есть тестовые)
├── essays/     - Философские эссе
├── dialogs/    - Диалоги Генриха и Смельчака
└── drafts/     - Черновики
```

**Форматы:** .txt, .md, .docx

---

### Шаг 3: Запуск обработки

**Вариант A: Через скрипт**
```bash
run.bat              # Полная обработка с векторами
run.bat --no-vectors # Без векторов (быстрее)
```

**Вариант B: Через CLI**
```bash
python cli.py process              # Полная обработка
python cli.py process --no-vectors # Без векторов
python cli.py test ./raw/quotes/цитаты.md  # Тест файла
```

---

## 📊 Результат

После обработки в папке `processed/` появятся JSON файлы:

```json
{
  "id": "uuid-...",
  "text": "очищенный текст",
  "metadata": {
    "content_type": "book|story|quote|essay",
    "language": "ru|en",
    "word_count": 1500
  },
  "tags": {
    "characters": ["Смельчак", "Генрих"],
    "themes": ["дружба", "верность"],
    "emotions": ["радость", "надежда"]
  },
  "agent_profile": "oleg|sheldon|genrikh|smelchak"
}
```

Если использовалась векторизация — в `vectors/` будет ChromaDB для семантического поиска.

---

## 🛠️ Полезные команды

```bash
# Проверка системы
python cli.py info

# Тест одного файла
python cli.py test ./raw/books/глава1.txt

# Статистика обработки
python cli.py process --stats-only

# Статистика ChromaDB
python cli.py db_stats

# Очистка ChromaDB
python cli.py db_reset
```

---

## 📖 Документация

- **Полная документация:** [datasets/README.md](datasets/README.md)
- **Быстрый старт:** [datasets/START.md](datasets/START.md)

---

## ⚠️ Возможные проблемы

### Ошибка при установке
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### NLTK требует данные
```bash
python -c "import nltk; nltk.download('all')"
```

### ChromaDB не работает
```bash
rmdir /s /q vectors
python cli.py process
```

---

## 🎯 Что дальше?

1. ✅ Обработать все тексты
2. ✅ Проверить результат в `processed/`
3. ✅ Протестировать поиск через ChromaDB
4. 🔄 Перейти к обучению LoRA адаптеров (следующий этап)

---

**Проект:** "Собачья мудрость. Секрет счастья"  
**Версия:** 0.1.0  
**Дата:** Март 2026
