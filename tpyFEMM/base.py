'''
base.py -- 基本的接口

该模块包含以下内容, 皆为实现软件功能的基础:  
- IRenderable 接口
- ITransRotatable 接口
- Point 类

作者: Fubiao Ouyang
创建时间: 2023-05-17
'''

from dataclasses import dataclass
from abc import ABC, abstractmethod
import math


class ILoadable(ABC):
    """可加载接口, 主要适用于一些材料、属性, 需要加载到项目中"""

    @abstractmethod
    def load(self) -> str:
        """加载资源, 并返回资源的名称"""
        pass


class IRenderable(ABC):
    """实现此接口的对象可以在FEMM 中被渲染到屏幕"""

    @abstractmethod
    def render(self):
        """渲染元素"""
        pass


class ITransRotatable(ABC):
    """实现此接口的对象内部的某些坐标属性可以被平移或旋转"""

    @abstractmethod
    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        """
        旋转元素

        Args:  
            - angle 旋转的角度  
            - bx, by 基准点坐标
        """
        pass

    @abstractmethod
    def translate(self, dx: float = .0, dy: float = .0):
        """
        平移元素  

        Args:  
            - dx, dy 平移的量
        """
        pass


@dataclass
class Point(ITransRotatable):
    """坐标点类型"""
    x: float = .0
    y: float = .0

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
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
