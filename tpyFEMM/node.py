from dataclasses import dataclass
from abc import abstractmethod
import femm

from .element import Element, Position


@dataclass
class Node(Element):
    """
    结点基类（抽象类）
    """
    position: Position = None
    """ (x,y) 位置信息, 默认为(0.0, 0.0)"""
    propName: str = ''
    """属性名默认为空, 且此属性仅在电场仿真时会用到"""
    groupNo: int = 0
    """所在组的编号, 默认为0 """

    def translate(self, dx: float = .0, dy: float = .0):
        """
        平移结点
        """
        self.position.translate(dx, dy)
        return self

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        """
        旋转结点
        """
        self.position.rotate(angle, bx, by)
        return self
    
    def render(self):
        self.addNode()
        self.selectNode()
        self.setNodeProp()
        self.clearSelected()
    
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



@dataclass  # 保留父类中的方法
class MagneticsNode(Node):
    """
    磁性节点
    """

    def addNode(self):
        femm.mi_addnode(self.position.x, self.position.y)

    def selectNode(self):
        femm.mi_selectnode(self.position.x, self.position.y)

    def setNodeProp(self):
        femm.mi_setnodeprop(self.propName, self.groupNo)

    def clearSelected(self):
        femm.mi_clearselected()
