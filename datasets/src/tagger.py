"""
Автоматическая разметка текста.
Определение типа контента, персонажей, тем, эмоций.
"""

import re
from typing import List, Dict, Optional
from pathlib import Path


class TextTagger:
    """Автоматическая разметка текстов"""
    
    # Персонажи проекта
    CHARACTERS = {
        'Смельчак': ['смельчак', 'смельчаку', 'смельчаком', 'смельчака'],
        'Генрих': ['генрих', 'генриха', 'генрихом', 'генриху'],
        'Эльза': ['эльза', 'эльзы', 'эльзе', 'эльзу', 'мама', 'мать'],
        'Григорий': ['григорий', 'григория', 'григорию', 'хозяин', 'первый хозяин'],
        'Максим': ['максим', 'максима', 'максиму'],
        'Петр': ['петр', 'петра', 'петру', 'пожарный'],
        'Нелли': ['нелли', 'нелли'],
        'Катя': ['катя', 'кати', 'кате', 'катю'],
        'Грета': ['грета', 'греты', 'грете', 'грету', 'сестра'],
        'Багги': ['багги', 'багги'],
        'Родион': ['родион', 'родиона', 'родиону', 'трудный подросток'],
    }
    
    # Темы проекта
    THEMES = {
        'дружба': ['дружб', 'друг', 'друзья', 'приятель', 'товарищ'],
        'верность': ['верност', 'предан', 'преданност'],
        'предназначение': ['предназначен', 'цель', 'миссия', 'служен'],
        'любовь': ['люб', 'любит', 'ласка', 'нежность'],
        'счастье': ['счаст', 'радост', 'блажен'],
        'страх': ['страх', 'бо', 'испуг', 'тревог'],
        'смерть': ['смерт', 'уход', 'погиб', 'умер'],
        'жизнь': ['жизн', 'жить', 'жив', 'существован'],
        'обучение': ['уч', 'наук', 'знан', 'школ', 'трениров'],
        'семья': ['сем', 'дом', 'родн', 'близк'],
        'потеря': ['потер', 'разлук', 'расставан'],
        'надежда': ['надежд', 'вера', 'ожидан'],
        'память': ['помн', 'воспоминан', 'памят'],
        'доверие': ['довер', 'доверя', 'вер'],
    }
    
    # Эмоции
    EMOTIONS = {
        'радость': ['рад', 'весел', 'счастлив', 'лик', 'восторг'],
        'грусть': ['груст', 'печал', 'тоск', 'уны'],
        'страх': ['страш', 'бо', 'испуг', 'паник'],
        'гнев': ['зл', 'гнев', 'ярост', 'сердит'],
        'надежда': ['надежд', 'вера', 'ожидан', 'мечт'],
        'любовь': ['люб', 'нежн', 'ласк', 'тепл'],
        'тревога': ['тревог', 'беспокой', 'нерв', 'волнен'],
        'спокойствие': ['спокой', 'умиротвор', 'тишин', 'покой'],
        'удивление': ['удив', 'изум', 'неожидан'],
        'благодарность': ['благодар', 'спасиб', 'признател'],
    }
    
    # Типы контента по ключевым признакам
    CONTENT_TYPES = {
        'quote': {
            'max_length': 500,  # символов
            'patterns': [r'^["«].*["»]$'],  # В кавычках
        },
        'dialog': {
            'patterns': [r'^[-–—]\s', r'^\w+ сказал:', r'^\w+ спросил:'],
        },
        'essay': {
            'min_length': 1000,
            'keywords': ['размышление', 'эссе', 'философия', 'мудрость'],
        },
        'story': {
            'min_length': 500,
            'keywords': ['история', 'рассказ', 'случай'],
        },
        'book': {
            'min_length': 5000,
        },
        'draft': {
            'keywords': ['черновик', 'набросок', 'заметка'],
        },
    }
    
    def __init__(self):
        pass
    
    def detect_language(self, text: str) -> str:
        """Определяет язык текста (упрощённо)"""
        cyrillic = len(re.findall(r'[а-яА-ЯёЁ]', text))
        latin = len(re.findall(r'[a-zA-Z]', text))
        
        if cyrillic > latin * 2:
            return 'ru'
        elif latin > 0:
            return 'en'
        return 'unknown'
    
    def detect_characters(self, text: str) -> List[str]:
        """Определяет персонажей в тексте"""
        text_lower = text.lower()
        found = []
        
        for character, variants in self.CHARACTERS.items():
            for variant in variants:
                if variant in text_lower:
                    found.append(character)
                    break
        
        return list(set(found))
    
    def detect_themes(self, text: str, threshold: int = 2) -> List[str]:
        """
        Определяет темы в тексте.
        
        Args:
            text: Исходный текст
            threshold: Минимальное количество совпадений для темы
        """
        text_lower = text.lower()
        found = []
        
        for theme, keywords in self.THEMES.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches >= threshold:
                found.append(theme)
        
        return found
    
    def detect_emotions(self, text: str, threshold: int = 1) -> List[str]:
        """
        Определяет эмоции в тексте.
        
        Args:
            text: Исходный текст
            threshold: Минимальное количество совпадений для эмоции
        """
        text_lower = text.lower()
        found = []
        
        for emotion, keywords in self.EMOTIONS.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches >= threshold:
                found.append(emotion)
        
        return found
    
    def detect_content_type(self, text: str, source_path: str = '') -> str:
        """
        Определяет тип контента.
        
        Args:
            text: Исходный текст
            source_path: Путь к файлу (для эвристики по имени файла)
        """
        text_len = len(text)
        path_lower = source_path.lower()
        
        # Проверка по пути
        if '/quotes/' in path_lower or '/цитаты/' in path_lower:
            return 'quote'
        if '/dialogs/' in path_lower or '/диалоги/' in path_lower:
            return 'dialog'
        if '/essays/' in path_lower or '/эссе/' in path_lower:
            return 'essay'
        if '/books/' in path_lower or '/книги/' in path_lower:
            return 'book'
        if '/drafts/' in path_lower or '/черновики/' in path_lower:
            return 'draft'
        
        # Проверка по содержимому
        for ctype, rules in self.CONTENT_TYPES.items():
            # Проверка длины
            if 'min_length' in rules and text_len < rules['min_length']:
                continue
            if 'max_length' in rules and text_len > rules['max_length']:
                continue
            
            # Проверка паттернов
            if 'patterns' in rules:
                for pattern in rules['patterns']:
                    if re.search(pattern, text, re.MULTILINE):
                        return ctype
            
            # Проверка ключевых слов
            if 'keywords' in rules:
                text_lower = text.lower()
                if any(kw in text_lower for kw in rules['keywords']):
                    return ctype
        
        # По умолчанию
        if text_len < 500:
            return 'quote'
        elif text_len < 2000:
            return 'story'
        else:
            return 'book'
    
    def detect_agent_profile(self, text: str, characters: List[str]) -> str:
        """
        Определяет, какому агенту принадлежит контент.
        
        Args:
            text: Исходный текст
            characters: Список обнаруженных персонажей
        """
        # Если есть Генрих - это его профиль
        if 'Генрих' in characters:
            return 'genrikh'
        
        # Если есть Смельчак - это его профиль
        if 'Смельчак' in characters:
            return 'smelchak'
        
        # Проверка на английский (Шелдон)
        lang = self.detect_language(text)
        if lang == 'en':
            return 'sheldon'
        
        # По умолчанию - Олег (автор)
        return 'oleg'
    
    def tag(self, text: str, source_path: str = '') -> Dict:
        """
        Полная разметка текста.
        
        Args:
            text: Исходный текст
            source_path: Путь к файлу
            
        Returns:
            Dict с тегами и метаданными
        """
        characters = self.detect_characters(text)
        
        return {
            'language': self.detect_language(text),
            'content_type': self.detect_content_type(text, source_path),
            'characters': characters,
            'themes': self.detect_themes(text),
            'emotions': self.detect_emotions(text),
            'agent_profile': self.detect_agent_profile(text, characters),
        }


# Пример использования
if __name__ == '__main__':
    tagger = TextTagger()
    
    test_text = """
    Смельчак смотрел на Генриха с надеждой.
    - Ты думаешь, мы справимся? - спросил он.
    Генрих молчал. Его зелёные глаза смотрели вдаль.
    - Жизнь научила меня одному: нельзя терять веру.
    """
    
    tags = tagger.tag(test_text, '/raw/stories/test.txt')
    
    print("Теги:")
    for key, value in tags.items():
        print(f"  {key}: {value}")
