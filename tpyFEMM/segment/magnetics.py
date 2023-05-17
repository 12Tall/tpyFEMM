import femm
from dataclasses import dataclass
from .segment import ArcSegment, LineSegment
from ..property import Property


@dataclass
class MagLineSegment(LineSegment):
    """磁学直线"""

    def addSegment(self):
        femm.mi_addsegment(self.start.pos.x, self.start.pos.y, self.end.pos.x,
                           self.end.pos.y)

    def selectSegment(self):
        x, y = self.getMidPoint()
        femm.mi_selectsegment(x, y)

    def setSegmentProp(self):
        femm.mi_setsegmentprop(self.prop, self.elementSize, self.autoMesh,
                               self.hide, self.grpNo)

    def clearSelected(self):
        femm.mi_clearselected()


@dataclass
class MagArcSegment(ArcSegment):
    """
    磁学圆弧
    """

    def addSegment(self):
        femm.mi_addarc(self.start.pos.x, self.start.pos.y, self.end.pos.x,
                       self.end.pos.y, self.angle, self.maxseg)

    def selectSegment(self):
        x, y = self.getMidPoint()
        femm.mi_selectarcsegment(x, y)

    def setSegmentProp(self):
        femm.mi_setarcsegmentprop(self.maxSegDeg, self.prop, self.hide,
                                  self.grpNo)

    def clearSelected(self):
        femm.mi_clearselected()
