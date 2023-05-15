from dataclasses import dataclass
from typing import List, Tuple
from abc import ABC, abstractmethod
import femm
import math

from .element import Element, Position


@dataclass
class Segment(Element):
    """
    连线基类(抽象类)
    """
    start: Position = None
    """ (x,y) 起始位置, 默认为(0.0, 0.0)"""
    end: Position = None
    """ (x,y) 终止位置(0.0, 0.0)"""
    propName: str = ''
    """属性名默认为空, 且此属性仅在电场仿真时会用到"""
    groupNo: int = 0
    """所在组的编号, 默认为0 """
    hide: 0 | 1 = 0
    """在后处理中隐藏线条"""

    def translate(self, dx: float = .0, dy: float = .0):
        """
        平移连线
        """
        self.start.translate(dx, dy)
        self.end.translate(dx, dy)
        return self

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        """
        旋转连线
        """
        self.start.rotate(angle, bx, by)
        self.end.rotate(angle, bx, by)
        return self

    def render(self):
        self.addSegment()
        self.selectSegment()
        self.setSegmentProp()
        self.clearSelected()

    @abstractmethod
    def getMidPoint(self):
        pass

    @abstractmethod
    def addSegment(self):
        pass

    @abstractmethod
    def selectSegment(self):
        pass

    @abstractmethod
    def clearSelected(self):
        pass

    @abstractmethod
    def setSegmentProp(self):
        pass


@dataclass
class LineSegment(Segment):
    """
    直线基类(抽象类)
    """
    elementSize: float = 1
    """绘制网格时的精度"""
    autoMesh: 0 | 1 = 1
    """自动生成网格, 为0 时根据elementSize(!=0 时) 生成网格"""

    def getMidPoint(self):
        """计算直线中点"""
        x1, y1 = self.start
        x2, y2 = self.end
        return (x1 + x2) / 2, (y1 + y2) / 2


@dataclass
class ArcSegment(Segment):
    """
    圆弧基类(抽象类)  
      圆弧的形状是从起点到终点, 沿逆时针绘制的  
    """
    angle: float = 0
    """圆弧包含的角度(不是弧度)"""
    maxseg: float = 0
    """圆弧将被分为几段"""
    maxSegDeg: float = 1
    """划分网格时, 单个元素最大的角度"""

    def getMidPoint(self):
        """
        计算圆弧的中点
        """
        x1 = self.start.x
        y1 = self.start.y
        x2 = self.end.x
        y2 = self.end.y
        # 转换为弧度
        angle = math.radians(self.angle)
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        distance = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        radius = distance / (2 * math.sin(angle / 2))
        # 首先计算弦的垂直平分线与x 轴的夹角
        c = math.atan2(y1 + y2, x1 + x2)
        # 垂直平分线靠近弧的一小段与半径长度的比值
        k = 1 - math.cos(angle / 2)

        center_x = mid_x + radius * math.cos(c) * k
        center_y = mid_y + radius * math.sin(c) * k
        return (center_x, center_y)


@dataclass  # 保留父类中的方法
class MagneticsLineSegment(LineSegment):
    """
    磁性直线(需要依赖正确的节点)
    """

    def addSegment(self):
        femm.mi_addsegment(self.start.x, self.start.y, self.end.x, self.end.y)

    def selectSegment(self):
        x, y = self.getMidPoint()
        femm.mi_selectsegment(x, y)

    def setSegmentProp(self):
        femm.mi_setsegmentprop(self.propName, self.elementSize, self.autoMesh,
                               self.hide, self.groupNo)

    def clearSelected(self):
        femm.mi_clearselected()


@dataclass  # 保留父类中的方法
class MagneticsArcSegment(ArcSegment):
    """
    磁性曲线
    """

    def addSegment(self):
        femm.mi_addarc(self.start.x, self.start.y, self.end.x, self.end.y,
                       self.angle, self.maxseg)

    def selectSegment(self):
        x, y = self.getMidPoint()
        femm.mi_selectarcsegment(x, y)

    def setSegmentProp(self):
        femm.mi_setarcsegmentprop(self.maxSegDeg, self.propName, self.hide,
                                  self.groupNo)

    def clearSelected(self):
        femm.mi_clearselected()
