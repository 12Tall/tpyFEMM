from dataclasses import dataclass
from typing import Tuple
from abc import ABC
import femm

from .element import Element


@dataclass
class Node(Element):
    """
    结点基类（抽象类）
    """
    position: Tuple[float, float] = (.0, .0)
    """ (x,y) 位置信息，默认为(0.0, 0.0)"""
    propName: str = ''
    """属性名默认为空，且此属性仅在电场仿真时会用到"""
    groupNo: int = 0
    """所在组的编号，默认为0 """


@dataclass  # 保留父类中的方法
class MagneticsNode(Node):
    """
    磁性节点
    """

    def render(self):
        """
        绘制节点，并设置属性，将其添加到组
        """
        x, y = self.position
        femm.mi_addnode(x, y)
        femm.mi_selectnode(x, y)
        femm.mi_setnodeprop(self.propName, self.groupNo)
        femm.mi_clearselected()
