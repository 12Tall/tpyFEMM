from enum import Enum
import femm


class DocType(Enum):
    """
    文档类型，枚举
    """
    Magnetics = 0
    Electrostatics = 1
    HeatFlow = 2
    CurrentFlow = 3


class Document(object):
    """
    文档类：  
        目前只能创建新的文档  
    """

    def __init__(self,
                 name: str = "untitled",
                 docType: DocType = None) -> None:
        self.docType = docType

    def render(self):
        """
        根据文档内容生成内容  
        """
        femm.openfemm()
        femm.newdocument(self.docType.value)
