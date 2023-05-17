from dataclasses import dataclass

from ..base import ILoadable


@dataclass
class Property(ILoadable):
    name: str = ""
    _existed: bool = False
    """软件已经自带了该属性, 一般用于材料的选择"""
