"""
Очистка и нормализация текста.
Удаление мусора, лишних пробелов, служебных символов.
"""

import re
from typing import List


class TextCleaner:
    """Очистка текста от шума и артефактов"""
    
    def __init__(self):
        # Паттерны для удаления
        self._patterns_to_remove = [
            r'\n{3,}',  # 3+ переносов строк подряд
            r' {2,}',   # 2+ пробелов подряд
            r'\t+',     # Табуляции
            r' +\n',    # Пробелы перед переносом строки
            r'\n +',    # Пробелы после переноса строки
        ]
    
    def clean(self, text: str, remove_empty_lines: bool = True) -> str:
        """
        Очищает текст от шума.
        
        Args:
            text: Исходный текст
            remove_empty_lines: Удалять ли пустые строки
            
        Returns:
            Очищенный текст
        """
        if not text:
            return ''
        
        # Нормализация переносов строк (Windows/Mac -> Unix)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Удаление невидимых символов
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        
        # Удаление по паттернам
        for pattern in self._patterns_to_remove:
            text = re.sub(pattern, '\n' if '\n' in pattern else ' ', text)
        
        # Удаление пустых строк
        if remove_empty_lines:
            lines = [line.strip() for line in text.split('\n')]
            lines = [line for line in lines if line]
            text = '\n'.join(lines)
        
        # Финальная обрезка
        text = text.strip()
        
        return text
    
    def remove_page_numbers(self, text: str) -> str:
        """Удаляет номера страниц (одиночные цифры в отдельных строках)"""
        lines = text.split('\n')
        filtered = []
        
        for line in lines:
            stripped = line.strip()
            # Если строка состоит только из 1-3 цифр - пропускаем
            if re.match(r'^\d{1,3}$', stripped):
                continue
            filtered.append(line)
        
        return '\n'.join(filtered)
    
    def remove_headers_footers(self, text: str, markers: List[str] = None) -> str:
        """
        Удаляет колонтитулы по маркерам.
        
        Args:
            text: Исходный текст
            markers: Список маркеров для удаления (например, ['© Олег Сдвижков', 'Собачья мудрость'])
        """
        if not markers:
            return text
        
        lines = text.split('\n')
        filtered = []
        
        for line in lines:
            is_marker = False
            for marker in markers:
                if marker.lower() in line.lower():
                    is_marker = True
                    break
            
            if not is_marker:
                filtered.append(line)
        
        return '\n'.join(filtered)
    
    def normalize_whitespace(self, text: str) -> str:
        """Нормализует пробелы вокруг знаков препинания"""
        # Удаление пробелов перед знаками препинания
        text = re.sub(r' +([,.!?;:)])', r'\1', text)
        # Добавление пробелов после знаков препинания
        text = re.sub(r'([,.!?;:(])([а-яА-Яa-zA-Z])', r'\1 \2', text)
        return text
    
    def get_statistics(self, text: str) -> dict:
        """Возвращает статистику текста"""
        lines = text.split('\n')
        words = text.split()
        
        return {
            'characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '').replace('\n', '')),
            'words': len(words),
            'lines': len([l for l in lines if l.strip()]),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
        }


# Пример использования
if __name__ == '__main__':
    cleaner = TextCleaner()
    
    test_text = """
    Это тестовый   текст.
    
    
    Он содержит    лишние пробелы 
    и пустые строки.
    
    123
    
    Конец.
    """
    
    cleaned = cleaner.clean(test_text)
    print("Очищенный текст:")
    print(cleaned)
    
    stats = cleaner.get_statistics(cleaned)
    print(f"\nСтатистика: {stats}")
