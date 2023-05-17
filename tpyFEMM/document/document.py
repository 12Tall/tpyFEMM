from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple
import femm

from ..base import IRenderable, ITransRotatable
from ..group import Group
from ..material import Material
from ..property import Property


class DocType(Enum):
    """
    文档类型，枚举
    """
    Magnetics = 0
    Electrostatics = 1
    HeatFlow = 2
    CurrentFlow = 3


class DocUnit(Enum):
    inches = "inches"
    millimeters = "millimeters"
    centimeters = "centimeters"
    mils = "mils"
    meters = "meters"
    micrometers = "micrometers"


class ProbType(Enum):
    planar = "planar"
    axi = "axi"


class ACSolver(Enum):
    SuccApprox = 0
    Newton = 1


@dataclass
class Document(IRenderable, ITransRotatable):
    """
    文档类：  
        目前只能创建新的文档  
    
    ⚠警告⚠:  
        因为文档中重合的点会覆盖掉前一个, 所以永远不要有位置重合的元素存在, 否则程序可能会有严重的bug
    """

    name: str = "untitled"
    docType: DocType = None
    units: DocUnit = DocUnit.inches
    probType: ProbType = ProbType.planar
    precision: float = 1e-8
    depth: float = 1
    minangle: float = 30

    groups: List[Group] = field(default_factory=list)
    groupNo = 0
    materials: List[Material] = field(default_factory=list)
    props: List[Property] = field(default_factory=list)

    def getUniqueGroupNo(self):
        self.groupNo = self.groupNo + 1
        return self.groupNo

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

    def loadMaterial(self, matrial: Material):
        """返回材料名"""
        self.materials.append(matrial)
        return matrial.name

    def loadCircuit(self, prop: Property):
        """返回材料名"""
        self.props.append(prop)
        return prop.name

    def loadBoundary(self, prop: Property):
        """返回材料名"""
        self.props.append(prop)
        return prop.name

    def render(self):
        """
        根据文档内容生成内容  
        """
        femm.openfemm()
        femm.newdocument(self.docType.value)

        for p in self.props:
            p.load()

        for m in self.materials:
            m.load()

        for grp in self.groups:
            grp.render()

    @abstractmethod
    def preProcess(self):
        """渲染前的准备工作"""
        pass

    @abstractmethod
    def process(self):
        """计算"""
        pass

    @abstractmethod
    def postProcess(self):
        """渲染前的准备工作"""
        pass