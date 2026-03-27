"""
Dog Wisdom Datasets - Система подготовки датасетов.

Проект: "Собачья мудрость. Секрет счастья"
"""

__version__ = '0.1.0'
__author__ = 'Олег Сдвижков'

from src.loader import TextLoader
from src.cleaner import TextCleaner
from src.tagger import TextTagger
from src.vectorizer import Vectorizer, ChromaDBManager
from src.pipeline import DataPipeline

__all__ = [
    'TextLoader',
    'TextCleaner',
    'TextTagger',
    'Vectorizer',
    'ChromaDBManager',
    'DataPipeline',
]
