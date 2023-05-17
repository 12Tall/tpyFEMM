from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..base import IRenderable, ITransRotatable, Point
from ..material import Material


class IBlock(ABC):
    """标签块接口"""

    @abstractmethod
    def addBlock(self):
        """
        添加标签块
        """
        pass

    @abstractmethod
    def selectBlock(self):
        """
        选择标签块
        """
        pass

    @abstractmethod
    def setBlockProp(self):
        """
        设置标签块属性
        """
        pass

    @abstractmethod
    def clearSelected(self):
        """
        清除选择项
        """
        pass


@dataclass
class Block(IRenderable, ITransRotatable, IBlock):
    """标签块基类(不可直接使用)"""

    pos: Point = None
    """标签块位置"""
    materialType: str = None
    """标签块属性"""
    grpNo: int = 0
    """所在组的编号, 默认为0 """
    autoMesh: 0 | 1 = 1
    """自动划分网格"""
    meshSize: 0 | 1 = 0
    """网格精度, 仅在autoMesh=0 时生效"""

    def translate(self, dx: float = .0, dy: float = .0):
        self.pos.translate(dx, dy)
        return self

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        self.pos.rotate(angle, bx, by)
        return self

    def render(self):
        self.addBlock()
        self.selectBlock()
        self.setBlockProp()
        self.clearSelected()