# 🚀 Быстрый старт

## 1. Установка (Windows)

**Автоматическая установка:**

Запустите файл `install.bat` двойным кликом или через консоль:

```bash
install.bat
```

Скрипт автоматически:
- ✅ Создаст виртуальное окружение
- ✅ Установит все зависимости
- ✅ Скачает данные NLTK
- ✅ Создаст структуру папок
- ✅ Создаст файл .env

**Ручная установка:**

```bash
# Перейти в папку проекта
cd "D:\Projects python\Dream Team Network\datasets"

# Создать venv
python -m venv venv

# Активировать (PowerShell)
.\venv\Scripts\Activate.ps1

# Или cmd
venv\Scripts\activate.bat

# Установить зависимости
pip install -r requirements.txt

# Скачать NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

---

## 2. Подготовка данных

Скопируйте ваши тексты из Яндекс.Диска в папку `raw/`:

```
raw/
├── books/          # Книги и повести
├── stories/        # Рассказы и притчи
├── quotes/         # Цитаты (уже есть тестовые)
├── essays/         # Эссе
├── dialogs/        # Диалоги
└── drafts/         # Черновики
```

**Поддерживаемые форматы:** .txt, .md, .docx

---

## 3. Запуск обработки

**Вариант 1: Через скрипт (рекомендуется)**

```bash
run.bat
```

Или без векторизации (быстрее):
```bash
run.bat --no-vectors
```

**Вариант 2: Через CLI**

```bash
# Полная обработка (с векторами)
python cli.py process

# Без векторов (быстрее)
python cli.py process --no-vectors

# С указанием путей
python cli.py process -i ./raw -o ./processed -v ./vectors

# Только статистика
python cli.py process --stats-only
```

---

## 4. Проверка результата

**Обработанные JSON файлы:**
```
processed/
├── uuid-1.json
├── uuid-2.json
└── ...
```

**Векторная база (если использовалась векторизация):**
```
vectors/
└── chroma.sqlite3
```

**Лог обработки:**
```
processed/process_log_YYYYMMDD_HHMMSS.txt
```

---

## 5. Тестирование

**Проверка одного файла:**

```bash
python cli.py test ./raw/quotes/цитаты.md
```

**Проверка системы:**

```bash
python cli.py info
```

**Статистика ChromaDB:**

```bash
python cli.py db_stats
```

---

## 📚 Примеры использования

### Пример 1: Первичная обработка

```bash
# 1. Копируем все тексты в raw/
# 2. Запускаем без векторов (быстро)
python cli.py process --no-vectors

# 3. Смотрим результат в processed/
```

### Пример 2: Полная обработка с векторизацией

```bash
# 1. Копируем тексты
# 2. Запускаем с векторами (долго, но полезно для поиска)
python cli.py process

# 3. Проверяем статистику
python cli.py db_stats
```

### Пример 3: Тестирование перед обработкой

```bash
# 1. Тестируем один файл
python cli.py test ./raw/books/глава1.txt

# 2. Если всё ок - запускаем полную обработку
python cli.py process
```

---

## ⚙️ Команды CLI

| Команда | Описание |
|---------|----------|
| `process` | Запуск обработки данных |
| `test` | Тест одного файла |
| `db_stats` | Статистика ChromaDB |
| `db_reset` | Очистка ChromaDB |
| `info` | Информация о системе |

---

## 🔧 Решение проблем

### Ошибка при установке зависимостей

```bash
# Обновить pip
python -m pip install --upgrade pip

# Установить по отдельности
pip install chromadb
pip install sentence-transformers
pip install nltk pymorphy3 pymorphy3-dicts-ru
```

### NLTK требует данные

```bash
python -c "import nltk; nltk.download('all')"
```

### ChromaDB не работает

```bash
# Удалить папку vectors/
rmdir /s /q vectors

# Запустить заново
python cli.py process
```

### Ошибка с .docx файлами

Убедитесь, что установлен python-docx:
```bash
pip install python-docx
```

---

## 📖 Документация

Полная документация в файле `README.md`

---

## 🎯 Что дальше?

После обработки:

1. ✅ Проверьте JSON файлы в `processed/`
2. ✅ Протестируйте поиск через ChromaDB
3. ✅ Используйте датасеты для обучения моделей
4. ✅ Интегрируйте с Dream Team

---

**Проект:** "Собачья мудрость. Секрет счастья"  
**Версия:** 0.1.0  
**Дата:** Март 2026
