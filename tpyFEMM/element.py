from abc import ABC, abstractmethod
from dataclasses import dataclass
import math


@dataclass
class Element(ABC):
    """
    基本元素类（抽象类）
    """

    @abstractmethod
    def render(self):
        """
        绘制元素
        
        新创建的元素似乎会覆盖旧元素, 如果两者位置完全一样
        """
        pass

    @abstractmethod
    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        pass

    @abstractmethod
    def translate(self, dx: float = .0, dy: float = .0):
        pass


@dataclass
class Position(Element):
    """
    坐标类型, 因为Tuple 类型不能重新赋值, 只能自定义新的类型
    """
    x: float = .0
    y: float = .0

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        """
        旋转一个点  
        Args:  
            basePoint(x,y) 基准点的坐标  
            angle 旋转的角度(不是弧度)
        """
        # 将角度转换为弧度
        angle = math.radians(angle)

        x, y = self.x, self.y
        dx = x - bx
        dy = y - by

        # 计算旋转后的坐标
        sin_angle = math.sin(angle)
        cos_angle = math.cos(angle)
        self.x = dx * cos_angle - dy * sin_angle + bx
        self.y = dx * sin_angle + dy * cos_angle + by

        return self

    def translate(self, dx: float = .0, dy: float = .0):
        self.x += dx
        self.y += dy
        return self
    
    def render(self):
        pass