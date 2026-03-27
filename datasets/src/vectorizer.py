"""
Векторизация текстов и работа с ChromaDB.
Создание эмбеддингов для семантического поиска.
"""

import os
import json
import hashlib
from typing import List, Dict, Optional
from pathlib import Path
from sentence_transformers import SentenceTransformer


class Vectorizer:
    """Создание векторных представлений текстов"""
    
    # Многоязычная модель (поддерживает русский и английский)
    MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
    
    def __init__(self, model_name: str = None, device: str = None):
        """
        Инициализация векторизатора.
        
        Args:
            model_name: Название модели (по умолчанию многоязычная)
            device: 'cpu' или 'cuda' (по умолчанию автовыбор)
        """
        self.model_name = model_name or self.MODEL_NAME
        self.device = device
        
        print(f"📥 Загрузка модели: {self.model_name}")
        self.model = SentenceTransformer(self.model_name, device=self.device)
        print("✅ Модель загружена")
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Создаёт векторное представление текста.
        
        Args:
            text: Исходный текст
            
        Returns:
            Вектор (список float)
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def create_batch_embeddings(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Создаёт векторы для батча текстов.
        
        Args:
            texts: Список текстов
            batch_size: Размер батча
            
        Returns:
            Список векторов
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings.tolist()
    
    @staticmethod
    def generate_id(text: str) -> str:
        """Генерирует уникальный ID для текста"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()


class ChromaDBManager:
    """Управление векторной базой данных ChromaDB"""
    
    def __init__(self, db_path: str, collection_name: str = 'dog_wisdom'):
        """
        Инициализация ChromaDB.
        
        Args:
            db_path: Путь к папке с базой данных
            collection_name: Название коллекции
        """
        import chromadb
        from chromadb.config import Settings
        
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Создаём постоянный клиент
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Получаем или создаём коллекцию
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Косинусное расстояние
        )
        
        print(f"✅ ChromaDB инициализирована: {self.db_path}")
        print(f"📊 Коллекция: {collection_name}, документов: {self.collection.count()}")
    
    def add_document(self, doc_id: str, text: str, embedding: List[float], metadata: Dict):
        """
        Добавляет документ в базу.
        
        Args:
            doc_id: Уникальный ID документа
            text: Исходный текст
            embedding: Векторное представление
            metadata: Метаданные (теги, автор, и т.д.)
        """
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )
    
    def add_documents(self, ids: List[str], texts: List[str], 
                     embeddings: List[List[float]], metadatas: List[Dict]):
        """
        Добавляет батч документов.
        
        Args:
            ids: Список ID
            texts: Список текстов
            embeddings: Список векторов
            metadatas: Список метаданных
        """
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
    
    def search(self, query_embedding: List[float], n_results: int = 5) -> Dict:
        """
        Семантический поиск.
        
        Args:
            query_embedding: Вектор запроса
            n_results: Количество результатов
            
        Returns:
            Dict с результатами поиска
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
    
    def search_by_text(self, query_text: str, vectorizer: Vectorizer, 
                       n_results: int = 5) -> Dict:
        """
        Поиск по текстовому запросу.
        
        Args:
            query_text: Текстовый запрос
            vectorizer: Векторизатор для создания эмбеддинга
            n_results: Количество результатов
            
        Returns:
            Dict с результатами поиска
        """
        embedding = vectorizer.create_embedding(query_text)
        return self.search(embedding, n_results)
    
    def get_stats(self) -> Dict:
        """Возвращает статистику базы"""
        return {
            'count': self.collection.count(),
            'name': self.collection.name,
            'path': str(self.db_path)
        }
    
    def reset(self):
        """Очищает базу (удаление всех документов)"""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
        print("🗑️  База данных очищена")


# Пример использования
if __name__ == '__main__':
    # Векторизация
    vectorizer = Vectorizer()
    
    texts = [
        "Смельчак был храбрым псом",
        "Генрих мудр и проницателен",
        "Счастье в служении другим"
    ]
    
    embeddings = vectorizer.create_batch_embeddings(texts)
    print(f"Создано векторов: {len(embeddings)}")
    print(f"Размер вектора: {len(embeddings[0])}")
    
    # ChromaDB
    db = ChromaDBManager('./vectors')
    
    for i, (text, emb) in enumerate(zip(texts, embeddings)):
        db.add_document(
            doc_id=f'doc_{i}',
            text=text,
            embedding=emb,
            metadata={'type': 'test', 'language': 'ru'}
        )
    
    print(f"📊 Добавлено документов: {db.get_stats()['count']}")
