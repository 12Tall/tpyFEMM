from dataclasses import dataclass, field
from enum import Enum
import os
from typing import List, Tuple
import femm

from ..base import IRenderable, ITransRotatable
from ..group import Group
from ..material import Material
from ..property import Property

from .document import DocType, ACSolver, Document


@dataclass
class MagDocument(Document):
    """
    文档类：  
        目前只能创建新的文档  
    
    ⚠警告⚠:  
        因为文档中重合的点会覆盖掉前一个, 所以永远不要有位置重合的元素存在, 否则程序可能会有严重的bug
    """
    name: str = "untitled"
    docType: DocType = None
    frequency: float = 0
    acsolver: ACSolver = ACSolver.Newton

    groups: List[Group] = field(default_factory=list)
    groupNo = 0
    materials: List[Material] = field(default_factory=list)
    props: List[Property] = field(default_factory=list)

    def preProcess(self):
        femm.mi_probdef(self.frequency, self.units.value, self.probType.value,
                        self.precision, self.depth, self.minangle,
                        self.acsolver.value)

        target_folder = "%s\out" % os.getcwd()
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        target = ("%s\\%s.FEM" % (target_folder, self.name)).replace(
            "\\", "\\\\")

        femm.mi_saveas(target)

    def process(self):
        femm.mi_createmesh()  # 这一步不是必须的
        femm.mi_analyze(0)
        femm.mi_loadsolution()
        pass

    def postProcess(self, i):
        target = ("%s\out\\%s.%d.bmp" % (os.getcwd(), self.name, i)).replace(
            "\\", "\\\\")
        # femm.mo_showdensityplot(1, 1, 0, 0, "bimag")  # 灰度 
        # femm.mo_showcontourplot(19, 0, 0, "real")  # 彩图 
        femm.mo_showdensityplot(-1, 0, 1, 0, "bimag")  # 彩图 
        femm.mo_savebitmap(target)
        pass