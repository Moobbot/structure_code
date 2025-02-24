import os
import sys
from abc import ABC, abstractmethod

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(project_root)

from models.recommendation_system.base_preprocessing import BasePreprocessing

class BaseAlgorithm(ABC):
    @abstractmethod
    def fit(self, dataset: BasePreprocessing):
        pass
    
    @abstractmethod
    def update(self, new_data):
        pass

    @abstractmethod
    def recommend(self, user_id, n):
        pass

    @abstractmethod
    def save(self, path):
        pass
    
    @staticmethod
    @abstractmethod
    def load(path):
        pass