from dataclasses import dataclass
from typing import Tuple
import femm

from .element import Element


@dataclass
class BlockLabel(Element):
    """
    标签基类(抽象类)
    """
    position: Tuple[float, float] = (.0, .0)
    """ (x,y) 标签位置, 默认为(0.0, 0.0)"""
    propName: str = ''
    """属性名默认为空"""
    groupNo: int = 0
    """所在组的编号, 默认为0 """
    autoMesh: 0 | 1 = 1
    """自动划分网格"""
    meshSize: 0 | 1 = 0
    """网格精度, 仅在autoMesh=0 时生效"""


@dataclass  # 保留父类中的方法
class MagneticsBlockLabel(BlockLabel):
    """
    磁性直线(需要依赖正确的节点)
    """
    inCircuit: str = ''
    """电路名称"""
    turns: int = 1
    """匝数"""
    magDirection: float | str = 0
    """磁化方向, 可以是一个角度或者一个由字符串组成的表达式"""

    def render(self):
        x, y = self.position
        femm.mi_addblocklabel(x, y)
        femm.mi_selectlabel(x, y)
        femm.mi_setblockprop(self.propName, self.autoMesh, self.meshSize,
                             self.inCircuit, self.magDirection, self.groupNo,
                             self.turns)
        femm.mi_clearselected()