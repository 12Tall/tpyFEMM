import copy
from dataclasses import dataclass, field
from typing import List
from .element import Element
from .node import Node
from .segment import Segment
from .block import BlockLabel


@dataclass
class Group(Element):
    """
    定义`组` 是用户操作的最小单位  
    todo: 因为元素的类型比较多, 所以暂时不添加创建元素的方法
    """
    no: int = 0
    nodes: List[Node] = field(default_factory=lambda: [])
    segments: List[Segment] = field(default_factory=lambda: [])
    blockLabels: List[BlockLabel] = field(default_factory=lambda: [])

    def render(self):
        for node in self.nodes:
            node.groupNo = self.no
            node.render()
        for segment in self.segments:
            segment.groupNo = self.no
            segment.render()
        for label in self.blockLabels:
            label.groupNo = self.no
            label.render()

    def translate(self, dx: float = .0, dy: float = .0):
        """
        平移组中的所有内容
        """
        for node in self.nodes:
            node.translate(dx, dy)
        for segment in self.segments:
            segment.translate(dx, dy)
        for label in self.blockLabels:
            label.translate(dx, dy)
        return self

    def rotate(self, angle: float = .0, bx: float = .0, by: float = .0):
        """
        旋转组中的所有内容
        """
        for node in self.nodes:
            node.rotate(angle, bx, by)
        for segment in self.segments:
            segment.rotate(angle, bx, by)
        for label in self.blockLabels:
            label.rotate(angle, bx, by)
        return self

    def addNode(self, *args: Node):
        """
        添加结点: 自动修改组号
        """
        for node in args:
            node.groupNo = self.no
            self.nodes.append(node)
        return self

    def addSegment(self, *args: Segment):
        """
        添加连线: 自动修改组号
        """
        for segment in args:
            segment.groupNo = self.no
            self.segments.append(segment)
        return self

    def addBlockLabel(self, *args: BlockLabel):
        """
        添加标签: 自动修改组号
        """
        for blockLabel in args:
            blockLabel.groupNo = self.no
            self.blockLabels.append(blockLabel)
        return self

    def clone(self):
        """
        位置信息相同的元素会覆盖掉旧的元素, 所以克隆后直接使用会有问题
        """
        return copy.deepcopy(self)


class PolygonGroup(Group):
    """
    多边形组
    """
    pass
