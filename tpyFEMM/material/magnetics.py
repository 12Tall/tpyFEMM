from dataclasses import dataclass
import femm
from enum import Enum

from .material import Material, DefaultMaterial


class DefaultMagMaterial(DefaultMaterial):
    """默认磁性材料名"""
    Air = "Air"
    PureIron = "Pure Iron"
    SWG_14 = "14 SWG"


class MagLamType(Enum):
    """磁性材料的堆叠类型"""
    Not_laminated_or_laminated_in_plane = 0
    Laminated_x_or_r = 1
    Laminated_y_or_z = 2
    Magnet_wire = 3
    Plain_stranded_wire = 4
    Litz_wire = 5
    Square_wire = 6
    CCA_10pct = 7
    CCA_15pct = 8


@dataclass
class MagMaterial(Material):
    """
    自定义磁性材料
    """

    muX: float = 1.
    muY: float = 1.
    hC: float = .0
    j: float = .0
    cDuct: float = .0
    lamD: float = .0
    phiHmax: float = .0
    lamFill: float = 1
    lamType: MagLamType = MagLamType.Not_laminated_or_laminated_in_plane
    phiHX: float = .0
    phiHY: float = .0
    nStrands: int = 0
    wireD: float = .0

    def load(self) -> str:
        if self._existed:
            femm.mi_getmaterial(self.name)
        else:
            femm.mi_addmaterial(self.name, self.muX, self.muY, self.hC, self.j,
                                self.cDuct, self.lamD, self.phiHmax,
                                self.lamFill, self.lamType.value, self.phiHX,
                                self.phiHY, self.nStrands, self.wireD)
        return self.name

    @staticmethod
    def GetDefault(material: DefaultMagMaterial):
        return MagMaterial(material.value, True)