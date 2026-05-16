from abc import ABC
from .logger import Logger

class BaseComponent(ABC):

    def __init__(self, name: str=None, **kwargs):
        self.name = name or self.__class__.__name__
        self.logger = Logger(self.name)

    def initialize(self) -> bool:
        return True