实践证明通过面向对象的方法封装这个库是可行的，但是需要做的工作太多，尤其是在搭建模型的时候。倒不如只用程序做数据分析和后处理部分。  

下面是参考[FEMM SOFTWARE VIDEO TUTORIALS](https://comprogexpert.com/femm-software-video-tutorials/) 做的例子：  

```python  
from tpyFEMM import MagDocument,DocType,MagBlock, MagBoundary,MagNode,MagLineSegment,Group,Point,MagCiruit,MagMaterial,DefaultMagMaterial 

doc =MagDocument(docType=DocType.Magnetics)

# 创建材料
iron = doc.loadMaterial(MagMaterial.GetDefault(DefaultMagMaterial.PureIron))
air = doc.loadMaterial(MagMaterial.GetDefault(DefaultMagMaterial.Air))
swg_14 = doc.loadMaterial(MagMaterial.GetDefault(DefaultMagMaterial.SWG_14))

# 创建电路属性
cIn = doc.loadCircuit(MagCiruit("cIn", 1, 1))
cOut = doc.loadCircuit(MagCiruit("cOut", -1, 1))

# 定义边界条件
bdry = doc.loadBoundary(MagBoundary("bdry"))

# C 形钢  
def getIronCSegment(i:int, start:MagNode, end:MagNode ):
    return MagLineSegment(start, end)
ironCLabel =  MagBlock(Point(0.1,0.1), iron)
ironC = Group.Polygon(getIronCSegment,ironCLabel,
                      MagNode(Point(0,0)),
                      MagNode(Point(80,0)),
                      MagNode(Point(80,15)),
                      MagNode(Point(15,15)),
                      MagNode(Point(15,65)),
                      MagNode(Point(80,65)),
                      MagNode(Point(80,80)),
                      MagNode(Point(0,80))
                      )
doc.addGroup(ironC)

# I 形钢
def getIronBarSegment(i:int, start:MagNode, end:MagNode ):
    return MagLineSegment(start, end)
ironBarLabel =  MagBlock(Point(83.1,0.1), iron)
ironBar = Group.Polygon(getIronBarSegment,ironBarLabel,
                      MagNode(Point(83,0)),
                      MagNode(Point(98,0)),
                      MagNode(Point(98,80)),
                      MagNode(Point(83,80))
                      )
doc.addGroup(ironBar)


# 绕组  
def getWindingSegment(i:int, start:MagNode, end:MagNode ):
    return MagLineSegment(start, end)
windingLeftLabel =  MagBlock(Point(-1.1,20.1), swg_14, inCircuit=cIn, turns=100)
windingRightLabel =  MagBlock(Point(16.1,20.1),swg_14, inCircuit=cIn, turns=100)
windingLeft = Group.Polygon(getWindingSegment,windingLeftLabel,
                      MagNode(Point(-1,20)),
                      MagNode(Point(-11,20)),
                      MagNode(Point(-11,60)),
                      MagNode(Point(-1,60))
                      )
windingRight = Group.Polygon(getWindingSegment,windingRightLabel,
                      MagNode(Point(16,20)),
                      MagNode(Point(26,20)),
                      MagNode(Point(26,60)),
                      MagNode(Point(16,60))
                      )

doc.addGroup(windingLeft, windingRight)

# 边界条件
def getBoundarySegment(i:int, start:MagNode, end:MagNode ):
    return MagLineSegment(start, end, prop=bdry )
boundaryLabel =  MagBlock(Point(.1,.1), air)
boundary = Group.Polygon(getBoundarySegment,boundaryLabel,
                         MagNode(Point(0,0)),
                         MagNode(Point(220,0)),
                         MagNode(Point(220,220)),
                         MagNode(Point(0,220)),
                         )
boundary.translate(-55,-70)
doc.addGroup(boundary)

doc.render()

doc.preProcess()

# 没有想好怎么在Doc 类中实现这类分析
import femm
for i in range(100):
    femm.mi_selectgroup(ironBar.no)
    femm.mi_movetranslate(i/500.0,0)
    doc.process()
    doc.postProcess(i=100+i)

```

程序的输出结果合并后如下图所示：    
![](./output.gif)