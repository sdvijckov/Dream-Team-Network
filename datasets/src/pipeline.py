"""
Основной пайплайн обработки данных.
Объединяет загрузку, очистку, разметку и векторизацию.
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm

from src.loader import TextLoader
from src.cleaner import TextCleaner
from src.tagger import TextTagger
from src.vectorizer import Vectorizer, ChromaDBManager


class DataPipeline:
    """Пайплайн обработки текстовых данных"""
    
    def __init__(self, 
                 raw_path: str,
                 processed_path: str,
                 vector_path: str,
                 use_vectors: bool = True):
        """
        Инициализация пайплайна.
        
        Args:
            raw_path: Папка с сырыми данными
            processed_path: Папка для обработанных JSON
            vector_path: Папка для ChromaDB
            use_vectors: Создавать ли векторные представления
        """
        self.raw_path = Path(raw_path)
        self.processed_path = Path(processed_path)
        self.vector_path = Path(vector_path)
        self.use_vectors = use_vectors
        
        # Создаём папки если не существуют
        self.processed_path.mkdir(parents=True, exist_ok=True)
        if use_vectors:
            self.vector_path.mkdir(parents=True, exist_ok=True)
        
        # Компоненты
        self.loader = TextLoader()
        self.cleaner = TextCleaner()
        self.tagger = TextTagger()
        self.vectorizer = None
        self.db = None
        
        if use_vectors:
            print("🔄 Инициализация векторизатора...")
            self.vectorizer = Vectorizer()
            self.db = ChromaDBManager(str(vector_path))
        
        # Статистика
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'total_characters': 0,
            'content_types': {},
            'languages': {},
            'errors': []
        }
    
    def process_file(self, file_data: Dict) -> Optional[Dict]:
        """
        Обрабатывает один файл.
        
        Args:
            file_data: Данные из loader.load_file()
            
        Returns:
            Обработанный Dict или None если ошибка
        """
        try:
            # Очистка
            text = self.cleaner.clean(file_data['text'])
            
            if not text.strip():
                return None
            
            # Разметка
            tags = self.tagger.tag(text, file_data['source_path'])
            
            # Статистика текста
            text_stats = self.cleaner.get_statistics(text)
            
            # Создаём результат
            doc_id = str(uuid.uuid4())
            
            result = {
                'id': doc_id,
                'text': text,
                'metadata': {
                    'source_file': file_data['source_file'],
                    'source_path': file_data['source_path'],
                    'extension': file_data['extension'],
                    'content_type': tags['content_type'],
                    'language': tags['language'],
                    'word_count': text_stats['words'],
                    'character_count': text_stats['characters'],
                    'processed_date': datetime.now().isoformat(),
                },
                'tags': {
                    'characters': tags['characters'],
                    'themes': tags['themes'],
                    'emotions': tags['emotions'],
                },
                'agent_profile': tags['agent_profile'],
            }
            
            # Векторизация
            if self.use_vectors and self.vectorizer:
                embedding = self.vectorizer.create_embedding(text)
                
                # Добавляем в ChromaDB
                self.db.add_document(
                    doc_id=doc_id,
                    text=text,
                    embedding=embedding,
                    metadata={
                        **result['metadata'],
                        **result['tags'],
                        'agent_profile': tags['agent_profile']
                    }
                )
            
            # Обновляем статистику
            self.stats['processed_files'] += 1
            self.stats['total_characters'] += text_stats['characters']
            
            ctype = tags['content_type']
            self.stats['content_types'][ctype] = \
                self.stats['content_types'].get(ctype, 0) + 1
            
            lang = tags['language']
            self.stats['languages'][lang] = \
                self.stats['languages'].get(lang, 0) + 1
            
            return result
            
        except Exception as e:
            self.stats['failed_files'] += 1
            error_msg = f"{file_data['source_file']}: {str(e)}"
            self.stats['errors'].append(error_msg)
            print(f"❌ Ошибка обработки {file_data['source_file']}: {e}")
            return None
    
    def save_result(self, result: Dict):
        """Сохраняет результат в JSON файл"""
        output_file = self.processed_path / f"{result['id']}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    def run(self) -> Dict:
        """
        Запускает пайплайн обработки.
        
        Returns:
            Статистика обработки
        """
        print("\n" + "="*60)
        print("🚀 Запуск пайплайна обработки данных")
        print("="*60)
        
        # Загрузка всех файлов
        print(f"\n📂 Загрузка файлов из: {self.raw_path}")
        files = self.loader.load_directory(str(self.raw_path), recursive=True)
        self.stats['total_files'] = len(files)
        
        if not files:
            print("⚠️  Файлы не найдены!")
            return self.stats
        
        print(f"✅ Найдено файлов: {len(files)}")
        
        # Обработка
        print("\n⚙️  Обработка файлов...")
        
        for file_data in tqdm(files, desc="Обработка"):
            result = self.process_file(file_data)
            
            if result:
                self.save_result(result)
        
        # Вывод статистики
        self._print_stats()
        
        return self.stats
    
    def _print_stats(self):
        """Выводит статистику обработки"""
        print("\n" + "="*60)
        print("📊 Статистика обработки")
        print("="*60)
        
        print(f"\n✅ Успешно обработано: {self.stats['processed_files']}")
        print(f"❌ Ошибок: {self.stats['failed_files']}")
        print(f"📝 Всего символов: {self.stats['total_characters']:,}")
        
        print("\n📁 Типы контента:")
        for ctype, count in sorted(self.stats['content_types'].items()):
            print(f"   {ctype}: {count}")
        
        print("\n🌐 Языки:")
        for lang, count in sorted(self.stats['languages'].items()):
            lang_name = {'ru': 'Русский', 'en': 'Английский'}.get(lang, lang)
            print(f"   {lang_name}: {count}")
        
        if self.stats['errors']:
            print("\n⚠️  Ошибки:")
            for error in self.stats['errors'][:5]:  # Показываем первые 5
                print(f"   {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... и ещё {len(self.stats['errors']) - 5}")
        
        if self.use_vectors and self.db:
            db_stats = self.db.get_stats()
            print(f"\n📊 ChromaDB: {db_stats['count']} документов")
        
        print("\n" + "="*60)
        print("✨ Обработка завершена!")
        print("="*60)


# Пример использования
if __name__ == '__main__':
    pipeline = DataPipeline(
        raw_path='./raw',
        processed_path='./processed',
        vector_path='./vectors',
        use_vectors=False  # Пока без векторов для теста
    )
    
    stats = pipeline.run()
