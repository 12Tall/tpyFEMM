from dataclasses import dataclass
from abc import ABC, abstractmethod, abstractstaticmethod
from enum import Enum

from ..base import ILoadable


class DefaultMaterial(Enum):
    """默认材料类型"""
    pass


class IMaterial(ILoadable):
    """材料接口"""
    pass


@dataclass
class Material(IMaterial):
    """
    材料(抽象类)
    """
    name: str = ""
    """材料名称"""
    _existed: bool = False
    """材料是否已存在(软件自带)"""

    def getName(self) -> str:
        return self.name


NoMesh = "<No Mesh>"
Default = "<None>"