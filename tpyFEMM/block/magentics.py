import femm
from dataclasses import dataclass

from .block import Block


@dataclass
class MagBlock(Block):
    """
    磁学标签块
    """
    inCircuit: str = ''
    """电路名称"""
    turns: int = 1
    """匝数"""
    magDirection: float | str = .0
    """磁化方向, 可以是一个角度或者一个由字符串组成的表达式"""

    def addBlock(self):
        femm.mi_addblocklabel(self.pos.x, self.pos.y)

    def selectBlock(self):
        femm.mi_selectlabel(self.pos.x, self.pos.y)

    def setBlockProp(self):
        femm.mi_setblockprop(self.materialType, self.autoMesh, self.meshSize,
                             self.inCircuit, self.magDirection, self.grpNo,
                             self.turns)

    def clearSelected(self):
        femm.mi_clearselected()
