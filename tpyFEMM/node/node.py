from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..base import IRenderable, ITransRotatable, Point
from ..property import Property


class INode(ABC):
    """结点操作接口"""

    @abstractmethod
    def addNode(self):
        """
        添加结点
        """
        pass

    @abstractmethod
    def selectNode(self):
        """
        选择结点
        """
        pass

    @abstractmethod
    def setNodeProp(self):
        """
        设置结点属性
        """
        pass

    @abstractmethod
    def clearSelected(self):
        """
        清除选择项
        """
        pass


@dataclass
class Node(ITransRotatable, IRenderable, INode):
    """
    结点基类, 不可直接初始化. 需要根据不同的结点类型实现自定义的节点操作
    """
    pos: Point = None
    """位置"""
    prop: str = ""
    """结点属性, 但是只有属性名会用到"""
    grpNo: int = 0
    """所在组(的编号)信息, 尽量减少对象的引用"""

    def translate(self, dx: float = 0, dy: float = 0):
        self.pos.translate(dx, dy)

    def rotate(self, angle: float = 0, bx: float = 0, by: float = 0):
        self.pos.rotate(angle, bx, by)

    def render(self):
        self.addNode()
        self.selectNode()
        self.setNodeProp()
        self.clearSelected()
