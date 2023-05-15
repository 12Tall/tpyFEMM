from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple
import femm

from .element import Element
from .group import Group


class DocType(Enum):
    """
    文档类型，枚举
    """
    Magnetics = 0
    Electrostatics = 1
    HeatFlow = 2
    CurrentFlow = 3


@dataclass
class Document(Element):
    """
    文档类：  
        目前只能创建新的文档  
    
    ⚠警告⚠:  
        因为文档中重合的点会覆盖掉前一个, 所以永远不要有位置重合的元素存在, 否则程序可能会有严重的bug
    """
    name: str = "untitled"
    docType: DocType = None
    groups: List[Group] = field(default_factory=list)
    groupNo = 0

    def getUniqueGroupNo(self):
        self.groupNo = self.groupNo + 1
        return self.groupNo

    def render(self):
        """
        根据文档内容生成内容  
        """
        femm.openfemm()
        femm.newdocument(self.docType.value)

        for grp in self.groups:
            grp.render()

    def translate(self, dx: float = .0, dy: float = .0):
        """
        平移所有文档内容  
        """
        for grp in self.groups:
            grp.translate(dx, dy)
        return self

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        """
        旋转整个文档的内容
        """
        for grp in self.groups:
            grp.rotate(angle, bx, by)
        return self

    def createGroup(self):
        """
        创建组
        """
        grp = Group()
        self.addGroup(grp)
        return grp

    def addGroup(self, *args: Group):
        for grp in args:
            # 在添加group 时会更新组编号
            grp.no = self.getUniqueGroupNo()
            self.groups.append(grp)
        return self
