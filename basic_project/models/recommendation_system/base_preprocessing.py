
from abc import ABC, abstractmethod


class BasePreprocessing(ABC):

    @abstractmethod
    def fit(self, data):
        pass

    @abstractmethod
    def build(self, data):
        pass