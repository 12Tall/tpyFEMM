from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Element(ABC):
    """
    基本元素类（抽象类）
    """

    @abstractmethod
    def render(self):
        """绘制元素"""
        pass
