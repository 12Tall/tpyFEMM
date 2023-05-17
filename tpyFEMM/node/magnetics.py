import femm
from dataclasses import dataclass

from .node import Node
from ..property import Property


@dataclass  # 保留父类中的方法
class MagNode(Node):
    """
    磁学节点
    """

    def addNode(self):
        femm.mi_addnode(self.pos.x, self.pos.y)

    def selectNode(self):
        femm.mi_selectnode(self.pos.x, self.pos.y)

    def setNodeProp(self):
        femm.mi_setnodeprop(self.prop, self.grpNo)

    def clearSelected(self):
        femm.mi_clearselected()
