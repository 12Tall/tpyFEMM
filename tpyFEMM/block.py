from abc import abstractmethod
from dataclasses import dataclass
import femm

from .element import Element, Position


@dataclass
class BlockLabel(Element):
    """
    标签基类(抽象类)
    """
    position: Position = None
    """ (x,y) 标签位置, 默认为(0.0, 0.0)"""
    propName: str = ''
    """属性名默认为空"""
    groupNo: int = 0
    """所在组的编号, 默认为0 """
    autoMesh: 0 | 1 = 1
    """自动划分网格"""
    meshSize: 0 | 1 = 0
    """网格精度, 仅在autoMesh=0 时生效"""

    def translate(self, dx: float = .0, dy: float = .0):
        """
        平移标签
        """
        self.position.translate(dx, dy)
        return self

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        """
        旋转标签
        """
        self.position.rotate(angle, bx, by)
        return self

    def render(self):
        self.addBlockLabel()
        self.selectBlockLabel()
        self.setBlockLabelProp()
        self.clearSelected()

    @abstractmethod
    def addBlockLabel(self):
        """
        添加属性标签
        """
        pass

    @abstractmethod
    def selectBlockLabel(self):
        """
        选择属性标签
        """
        pass

    @abstractmethod
    def setBlockLabelProp(self):
        """
        设置属性标签属性
        """
        pass

    @abstractmethod
    def clearSelected(self):
        """
        清除选择项
        """
        pass


@dataclass  # 保留父类中的方法
class MagneticsBlockLabel(BlockLabel):
    """
    磁性直线(需要依赖正确的节点)
    """
    inCircuit: str = ''
    """电路名称"""
    turns: int = 1
    """匝数"""
    magDirection: float | str = .0
    """磁化方向, 可以是一个角度或者一个由字符串组成的表达式"""

    def addBlockLabel(self):
        femm.mi_addblocklabel(self.position.x, self.position.y)

    def selectBlockLabel(self):
        femm.mi_selectlabel(self.position.x, self.position.y)

    def setBlockLabelProp(self):
        femm.mi_setblockprop(self.propName, self.autoMesh, self.meshSize,
                             self.inCircuit, self.magDirection, self.groupNo,
                             self.turns)

    def clearSelected(self):
        femm.mi_clearselected()
