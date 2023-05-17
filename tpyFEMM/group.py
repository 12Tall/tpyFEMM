import copy
from dataclasses import dataclass, field
from typing import Callable, List, Type
from .base import IRenderable, ITransRotatable
from .node import Node
from .segment import Segment
from .block import Block


@dataclass
class Group(IRenderable, ITransRotatable):
    """
    定义`组` 是用户操作的最小单位  
    todo: 因为元素的类型比较多, 所以暂时不添加创建元素的方法
    """
    no: int = 0
    nodes: List[Node] = field(default_factory=lambda: [])
    segments: List[Segment] = field(default_factory=lambda: [])
    blocks: List[Block] = field(default_factory=lambda: [])

    def render(self):
        """
        迫于种种原因, 只好在渲染时自动修改元素所在组的编号
        """
        for node in self.nodes:
            node.grpNo = self.no
            node.render()
        for segment in self.segments:
            segment.grpNo = self.no
            segment.render()
        for label in self.blocks:
            label.grpNo = self.no
            label.render()

    def translate(self, dx: float = .0, dy: float = .0):
        """
        平移组中的所有内容
        """
        for node in self.nodes:
            node.translate(dx, dy)
        ## 因为连线与结点绑定，所以不需要重复移动 ##
        # for segment in self.segments:
        #     segment.translate(dx, dy)
        for label in self.blocks:
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
        for label in self.blocks:
            label.rotate(angle, bx, by)
        return self

    def addNode(self, *args: Node):
        """
        添加结点
        """
        for node in args:
            self.nodes.append(node)
        return self

    def addSegment(self, *args: Segment):
        """
        添加连线
        """
        for segment in args:
            self.segments.append(segment)
        return self

    def addBlock(self, *args: Block):
        """
        添加标签
        """
        for block in args:
            self.blocks.append(block)
        return self

    def clone(self):
        """
        位置信息相同的元素会覆盖掉旧的元素, 所以克隆后直接使用会有问题
        """
        return copy.deepcopy(self)

    def Polygon(factory: Callable[[int, Node, Node], Segment], block: Block,
                *args: Node):
        """
        绘制一个闭合的多边形区域, 因为语法限制, 不能使用泛型, 只好传入工厂方法  


        Args:  
            - factory: Callable[[int, Node, Node], Segment] 用于构造连线的工厂函数, 接收三个参数: 当前连线的序号以及起始位置
            - blockLable: BlockLabel 区域内的属性标签  
            - *args: Node 顶点
        """
        grp = Group()
        for node in args:
            grp.addNode(node)
        for i in range(len(grp.nodes)):
            grp.addSegment(factory(i - 1, grp.nodes[i - 1], grp.nodes[i]))
        grp.addBlock(block)
        return grp