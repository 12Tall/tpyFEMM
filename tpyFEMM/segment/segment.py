from abc import ABC, abstractmethod
from dataclasses import dataclass
import math

from ..base import IRenderable, ITransRotatable
from ..node import Node
from ..property import Property


class ISegment(ABC):

    @abstractmethod
    def getMidPoint(self):
        """获取连线的中点坐标"""
        pass

    @abstractmethod
    def addSegment(self):
        """绘制连线"""
        pass

    @abstractmethod
    def selectSegment(self):
        """选择连线"""
        pass

    @abstractmethod
    def clearSelected(self):
        """清空选择"""
        pass

    @abstractmethod
    def setSegmentProp(self):
        """设置连线的属性"""
        pass


@dataclass
class Segment(ITransRotatable, IRenderable, ISegment):
    """
    连线基类, 不能直接使用  
    """
    start: Node = None
    end: Node = None
    prop: str = ""
    """连线属性名"""
    grpNo: int = 0
    """所在组(的编号)信息, 尽量减少对象的引用"""
    hide: 0 | 1 = 0
    """是否在后处理中隐藏线条, 默认为否"""

    def translate(self, dx: float = 0, dy: float = 0):
        self.start.translate(dx, dy)
        self.end.translate(dx, dy)

    def rotate(self, angle: float = 0, bx: float = 0, by: float = 0):
        self.start.rotate(angle, bx, by)
        self.end.rotate(angle, bx, by)

    def render(self):
        self.addSegment()
        self.selectSegment()
        self.setSegmentProp()
        self.clearSelected()


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
        x1 = self.start.pos.x
        y1 = self.start.pos.y
        x2 = self.end.pos.x
        y2 = self.end.pos.y
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
        x1 = self.start.pos.x
        y1 = self.start.pos.y
        x2 = self.end.pos.x
        y2 = self.end.pos.y
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
        return center_x, center_y
