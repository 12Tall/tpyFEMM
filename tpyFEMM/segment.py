from dataclasses import dataclass
from typing import Tuple
from abc import ABC, abstractmethod
import femm
import math

from .element import Element


@dataclass
class Segment(Element):
    """
    连线基类(抽象类)
    """
    start: Tuple[float, float] = (.0, .0)
    """ (x,y) 起始位置, 默认为(0.0, 0.0)"""
    end: Tuple[float, float] = (.0, .0)
    """ (x,y) 终止位置(0.0, 0.0)"""
    propName: str = ''
    """属性名默认为空, 且此属性仅在电场仿真时会用到"""
    groupNo: int = 0
    """所在组的编号, 默认为0 """
    hide: 0 | 1 = 0
    """在后处理中隐藏线条"""

    @abstractmethod
    def getMidPoint(self):
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
        x1, y1 = self.start
        x2, y2 = self.end
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

    def render(self):
        x1, y1 = self.start
        x2, y2 = self.end
        x, y = self.getMidPoint()
        femm.mi_addsegment(x1, y1, x2, y2)
        femm.mi_selectsegment(x, y)
        femm.mi_setsegmentprop(self.propName, self.elementSize, self.autoMesh,
                               self.hide, self.groupNo)
        femm.mi_clearselected()


@dataclass  # 保留父类中的方法
class MagneticsArcSegment(ArcSegment):
    """
    磁性曲线
    """

    def render(self):
        x1, y1 = self.start
        x2, y2 = self.end
        x, y = self.getMidPoint()
        femm.mi_addarc(x1, y1, x2, y2, self.angle, self.maxseg)
        femm.mi_selectarcsegment(x, y)  # 这里的方法有可能导致无法选择曲线
        femm.mi_setarcsegmentprop(self.maxSegDeg, self.propName, self.hide,
                                  self.groupNo)
        femm.mi_clearselected()
