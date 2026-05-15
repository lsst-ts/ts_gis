__all__ = [
    "gisCpuInputs",
    "gisCpuOutputs",
    "gisCpuReserve",
    "afeDecentralizedIOInputs",
    "afeDecentralizedIOOutputs",
    "afeDecentralizedIOFree",
    "laserDecentralizedIOInput",
    "laserDecentralizedIOOutputs",
    "laserDecentralizedIOFree",
    "m2cDecentralizedIOInput",
    "m2cDecentralizedIOOutput",
    "m2cDecentralizedIOFree",
    "pfDecentralizedIoInputs",
    "pfDecentralizedIoOutput",
    "pfDecentralizedIoFree",
    "auxCpuInputs",
    "auxCpuOutputs",
    "domeCpuInputs",
    "domeCpuOutputs",
    "m1m3CpuInputs",
    "m1m3CpuOutputs",
    "tmaCpuInputs",
    "tmaCpuOutputs",
    "causes",
    "causes2",
    "causesOverride",
    "causes2Override",
    "effects",
    "effects2",
    "acks",
    "auxTel",
    "subsystem_order",
    "ErrorCode",
    "find_freespace",
    "IsDataclass",
]

from dataclasses import dataclass, fields
from enum import IntEnum, auto
from typing import Any, ClassVar, Protocol

# ruff: noqa: N801

subsystem_order = (
    "gisCpuInputs",
    "gisCpuOutputs",
    "gisCpuReserve",
    "afeDecentralizedIOInputs",
    "afeDecentralizedIOOutputs",
    "afeDecentralizedIOFree",
    "laserDecentralizedIOInput",
    "laserDecentralizedIOOutputs",
    "laserDecentralizedIOFree",
    "m2cDecentralizedIOInput",
    "m2cDecentralizedIOOutput",
    "m2cDecentralizedIOFree",
    "pfDecentralizedIoInputs",
    "pfDecentralizedIoOutput",
    "pfDecentralizedIoFree",
    "auxCpuInputs",
    "auxCpuOutputs",
    "domeCpuInputs",
    "domeCpuOutputs",
    "m1m3CpuInputs",
    "m1m3CpuOutputs",
    "tmaCpuInputs",
    "tmaCpuOutputs",
    "causes",
    "causes2",
    "causesOverride",
    "causes2Override",
    "effects",
    "effects2",
    "acks",
    "auxTel",
    "Reserved",
    "Reserved2",
    "Reserved3",
    "Reserved4",
)


class IsDataclass(Protocol):
    # Check for this attribute as the most reliable way to know
    # if dataclass
    __dataclass_fields__: ClassVar[dict[str, Any]]


def find_freespace(cls: IsDataclass, field_name: str) -> tuple[int, int]:
    """Return the start-inclusive, stop-exclusive range of a free-space field.

    Parameters
    ----------
    cls : `IsDataclass`
        The dataclass to search through.
    field_name : `str`
        The name of the freespace field.
    Returns
    -------
    tuple[int, int]
        The start-inclusive, stop-exclusive range of the free-space field.
    """
    offset = 0
    for field in fields(cls):
        if field.name == field_name:
            break
        else:
            offset += 1
    return offset, offset + len(getattr(cls, field_name))


class ErrorCode(IntEnum):
    """The error codes."""

    TELEMETRY_FAILED = auto()
    """Telemetry loop failed."""
    CONNECT_FAILED = auto()
    """Connection call failed."""
    LOST_CONNECTION = auto()
    """Lost connection."""


@dataclass
class gisCpuInputs:
    """Main GIS CPU inputs.

    Parameters
    ----------
    sdiCPUetw1A : `bool`
        Wireless emergency pushbutton 1 channel 1.
    sdiCPUetw1B : `bool`
        Wireless emergency pushbutton 1 channel 2.
    sdiCPUetw2A : `bool`
        Wireless emergency pushbutton 2 channel 1.
    sdiCPUetw2B : `bool`
        Wireless emergency pushbutton 2 channel 2.
    sdiCPUfree1 : `bool`
        Reserved for future use 1.
    sdiCPUfree2 : `bool`
        Reserved for future use 2.
    sdiCPUfree3 : `bool`
        Reserved for future use 3.
    sdiCPUfree4 : `bool`
        Reserved for future use 4.
    sdiCPUfree5 : `bool`
        Reserved for future use 5.
    sdiCPUfree6 : `bool`
        Reserved for future use 6.
    sdiCPUfree7 : `bool`
        Reserved for future use 7.
    sdiCPUfree8 : `bool`
        Reserved for future use 8.
    sdiCPUfree9 : `bool`
        Reserved for future use 9.
    sdiCPUfree10 : `bool`
        Reserved for future use 10.
    sdiCPUpsr : `bool`
        Power supply redundancy OK.
    sdiCPUpsb : `bool`
        Power supply balancing OK.
    """

    sdiCPUetw1A: bool
    sdiCPUetw1B: bool
    sdiCPUetw2A: bool
    sdiCPUetw2B: bool
    sdiCPUfree1: bool
    sdiCPUfree2: bool
    sdiCPUfree3: bool
    sdiCPUfree4: bool
    sdiCPUfree5: bool
    sdiCPUfree6: bool
    sdiCPUfree7: bool
    sdiCPUfree8: bool
    sdiCPUfree9: bool
    sdiCPUfree10: bool
    sdiCPUpsr: bool
    sdiCPUpsb: bool


@dataclass
class gisCpuOutputs:
    """
    Parameters
    ----------
    sdoCPUetw1rst : `bool`
        Wireless emergency pushbutton 1 reset.
    sdoCPUetw2rst : `bool`
        Wireless emergency pushbutton 2 reset.
    sdoCPUfireA : `bool`
        GIS fire indication channel 1.
    sdoCPUfireB : `bool`
        GIS fire indication channel 2.
    sdoCPUfree1 : `bool`
        Reserved for future use 1.
    sdoCPUfree2 : `bool`
        Reserved for future use 2.
    sdoCPUfree3 : `bool`
        Reserved for future use 3.
    sdoCPUfree4 : `bool`
        Reserved for future use 4.
    sdoCPUfree5 : `bool`
        Reserved for future use 5.
    sdoCPUfree6 : `bool`
        Reserved for future use 6.
    sdoCPUfree7 : `bool`
        Reserved for future use 7.
    sdoCPUfree8 : `bool`
        Reserved for future use 8.
    sdoCPUfree9 : `bool`
        Reserved for future use 9.
    sdoCPUfree10 : `bool`
        Reserved for future use 10.
    sdoCPUfree11 : `bool`
        Reserved for future use 11.
    sdoCPUfree12 : `bool`
        Reserved for future use 12.
    """

    sdoCPUetw1rst: bool
    sdoCPUetw2rst: bool
    sdoCPUfireA: bool
    sdoCPUfireB: bool
    sdoCPUfree1: bool
    sdoCPUfree2: bool
    sdoCPUfree3: bool
    sdoCPUfree4: bool
    sdoCPUfree5: bool
    sdoCPUfree6: bool
    sdoCPUfree7: bool
    sdoCPUfree8: bool
    sdoCPUfree9: bool
    sdoCPUfree10: bool
    sdoCPUfree11: bool
    sdoCPUfree12: bool


@dataclass
class gisCpuReserve:
    """
    Parameters
    ----------
    sdrCPUfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdrCPUfree: tuple[
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdrCPUfree")


@dataclass
class afeDecentralizedIOInputs:
    """
    Parameters
    ----------
    sdiAFEetacA : `bool`
        Emergency channel 1 from access control.
    sdiAFEetacB : `bool`
        Emergency channel 2 from access control.
    sdiAFEetsfA : `bool`
        Emergency channel 1 from summit fire control.
    sdiAFEetsfB : `bool`
        Emergency channel 2 from summit fire control.
    sdiAFEeteaA : `bool`
        Emergency channel 1 from earthquake control.
    sdiAFEeteaB : `bool`
        Emergency channel 2 from earthquake control.
    sdiAFEupieraA : `bool`
        Unauthorized pier access channel 1.
    sdiAFEupieraB : `bool`
        Unauthorized pier access channel 2.
    sdiAFEudomeaA : `bool`
        Unauthorized dome access channel 1.
    sdiAFEdomeaB : `bool`
        Unauthorized dome access channel 2.
    sdiAFEfireA : `bool`
        Fire interlock channel 1.
    sdiAFEfireB : `bool`
        Fire interlock channel 2.
    sdiAFEfree1 : `bool`
        Reserved for future use 1.
    sdiAFEfree2 : `bool`
        Reserve for future use 2.
    sdiAFEpsr : `bool`
        Power supply redundancy OK.
    sdiAFEpsb : `bool`
        Power supply balancing OK.
    """

    sdiAFEetacA: bool
    sdiAFEetacB: bool
    sdiAFEetsfA: bool
    sdiAFEetsfB: bool
    sdiAFEeteaA: bool
    sdiAFEeteaB: bool
    sdiAFEupieraA: bool
    sdiAFEupieraB: bool
    sdiAFEudomeaA: bool
    sdiAFEdomeaB: bool
    sdiAFEfireA: bool
    sdiAFEfireB: bool
    sdiAFEfree1: bool
    sdiAFEfree2: bool
    sdiAFEpsr: bool
    sdiAFEpsb: bool


@dataclass
class afeDecentralizedIOOutputs:
    """
    Parameters
    ----------
    sdoAFEetacA : `bool`
        Emergency channel 1 to access control.
    sdoAFEetacB : `bool`
        Emergency channel 2 to access control.
    sdoAFEetsfA : `bool`
        Emergency channel 1 to summit fire control.
    sdoAFEetsfB : `bool`
        Emergency channel 2 to summit fire control.
    sdoAFEfree1 : `bool`
        Reserved for future use 1.
    sdoAFEfree2 : `bool`
        Reserved for future use 2.
    sdoAFEetacrst : `bool`
        Reset emergency to access control.
    sdoAFEetsfrst : `bool`
        Reset emergency to summit fire control.
    sdoAFEfree : `tuple` [`bool`, ...]
        Reserve.
    """

    sdoAFEetacA: bool
    sdoAFEetacB: bool
    sdoAFEetsfA: bool
    sdoAFEetsfB: bool
    sdoAFEfree1: bool
    sdoAFEfree2: bool
    sdoAFEetacrst: bool
    sdoAFEetsfrst: bool
    sdoAFEfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdoAFEfree")


@dataclass
class afeDecentralizedIOFree:
    """
    Parameters
    ----------
    sdrAFEfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdrAFEfree: tuple[
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdrAFEfree")


@dataclass
class laserDecentralizedIOInput:
    """
    Parameters
    ----------
    sdiLASetA : `bool`
        Emergency channel 1 from laser control.
    sdiLASetB : `bool`
        Emergency channel 2 from laser control.
    sdiLASfree1 : `bool`
        Reserved for future use 1.
    sdiLASfree2 : `bool`
        Reserved for future use 2.
    sdiLASfree3 : `bool`
        Reserved for future use 3.
    sdiLASfree4 : `bool`
        Reserved for future use 4.
    sdiLASpsr : `bool`
        Power supply redundancy OK.
    sdiLASpsb : `bool`
        Power supply balancing OK.
    sdiLASfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdiLASetA: bool
    sdiLASetB: bool
    sdiLASfree1: bool
    sdiLASfree2: bool
    sdiLASfree3: bool
    sdiLASfree4: bool
    sdiLASpsr: bool
    sdiLASpsb: bool
    sdiLASfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdiLASfree")


@dataclass
class laserDecentralizedIOOutputs:
    """
    Parameters
    ----------
    sdoLASetA : `bool`
        Emergency channel 1 to laser control.
    sdoLASetB : `bool`
        Emergency channel 2 to laser control.
    sdoLASfree1 : `bool`
        Reserved for future use 1.
    sdoLASfree2 : `bool`
        Reserved for future use 2.
    sdoLASetrst : `bool`
        Reset emergency to laser control.
    sdoLASfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdoLASetA: bool
    sdoLASetB: bool
    sdoLASfree1: bool
    sdoLASfree2: bool
    sdoLASetrst: bool
    sdoLASfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdoLASfree")


@dataclass
class laserDecentralizedIOFree:
    """
    Parameters
    ----------
    sdrLASfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdrLASfree: tuple[
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdrLASfree")


@dataclass
class m2cDecentralizedIOInput:
    """
    Parameters
    ----------
    sdiM2Cetm2aA : `bool`
        Emergency channel 1 from M2 actuators control.
    sdiM2Cetm2aB : `bool`
        Emergency channel 2 from M2 actuators control.
    sdiM2Cetm2hA : `bool`
        Emergency channel 1 from M2 hexapod control.
    sdiM2Cetm2hB : `bool`
        Emergency channel 2 from M2 hexapod control.
    sdiM2CetcrA : `bool`
        Emergency channel 1 from camera rotator control.
    sdiM2CetcrB : `bool`
        Emergency channel 2 from camera hexapod control.
    sdiM2CetchA : `bool`
        Emergency channel 1 from camera hexapod control.
    sdiM2CetchB : `bool`
        Emergency channel 2 from camera hexapod control.
    sdiM2Cpinins : `bool`
        Camera rotator pin inserted.
    sdiM2Cfree1 : `bool`
        Reserved for future use 1.
    sdiM2Cpsr : `bool`
        Power supply redundancy OK.
    sdiM2Cpsb : `bool`
        Power supply balancing OK.
    sdiM2Cfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdiM2Cetm2aA: bool
    sdiM2Cetm2aB: bool
    sdiM2Cetm2hA: bool
    sdiM2Cetm2hB: bool
    sdiM2CetcrA: bool
    sdiM2CetcrB: bool
    sdiM2CetchA: bool
    sdiM2CetchB: bool
    sdiM2Cpinins: bool
    sdiM2Cfree1: bool
    sdiM2Cpsr: bool
    sdiM2Cpsb: bool
    sdiM2Cfree: tuple[bool, bool, bool, bool] = (False, False, False, False)

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdiM2Cfree")


@dataclass
class m2cDecentralizedIOOutput:
    """
    Parameters
    ----------
    sdoM2Cetm2aA : `bool`
        Emergency channel 1 to M2 actuators control.
    sdoM2Cetm2aB : `bool`
        Emergency channel 2 to M2 actuators control.
    sdoM2Cetm2hA : `bool`
        Emergency channel 1 to M2 hexapod control.
    sdoM2Cetm2hB : `bool`
        Emergency channel 2 to M2 hexapod control.
    sdoM2CetcrA : `bool`
        Emergency channel 1 to camera rotator control.
    sdoM2CetcrB : `bool`
        Emergency channel 2 to camera rotator control.
    sdoM2CetchA : `bool`
        Emergency channel 1 to camera hexapod control.
    sdoM2CetchB : `bool`
        Emergency channel 2 to camera hexapod control.
    sdoM2Cfree1 : `bool`
        Reserved for future use 1.
    sdoM2Cfree2 : `bool`
        Reserved for future use 2.
    sdoM2Cetm2arst : `bool`
        Reset emergency to M2 actuators control.
    sdoM2Cetm2hst : `bool`
        Reset emergency to M2 hexapod control.
    sdoM2Cetcrrst : `bool`
        Reset emergency to camera rotator control.
    sdoM2Cetchrst : `bool`
        Reset emergency to camera hexapod control.
    sdoM2Cfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdoM2Cetm2aA: bool
    sdoM2Cetm2aB: bool
    sdoM2Cetm2hA: bool
    sdoM2Cetm2hB: bool
    sdoM2CetcrA: bool
    sdoM2CetcrB: bool
    sdoM2CetchA: bool
    sdoM2CetchB: bool
    sdoM2Cfree1: bool
    sdoM2Cfree2: bool
    sdoM2Cetm2arst: bool
    sdoM2Cetm2hst: bool
    sdoM2Cetcrrst: bool
    sdoM2Cetchrst: bool
    sdoM2Cfree: tuple[bool, bool] = (False, False)

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdoM2Cfree")


@dataclass
class m2cDecentralizedIOFree:
    """
    Parameters
    ----------
    sdrM2Cfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdrM2Cfree: tuple[
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdrM2Cfree")


@dataclass
class pfDecentralizedIoInputs:
    """
    Parameters
    ----------
    sdiPFLetA : `bool`
        Emergency channel 1 from Pflow & auxiliary control.
    sdiPFLetB : `bool`
        Emergency channel 2 from Pflow & auxiliary control.
    sdiPFLmlnotpark : `bool`
        Man lift not parked.
    sdiPFLpllowlevel : `bool`
        Platform lift above enclosure lower level.
    sdiPFLplnotpark : `bool`
        Platform lift not parked at the telescope level.
    sdiPFLfree1 : `bool`
        Reserved for future use 1.
    sdiPFLpsr : `bool`
        Power supply redundancy OK.
    sdiPFLpsb : `bool`
        Power supply balancing OK.
    sdiPFfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdiPFLetA: bool
    sdiPFLetB: bool
    sdiPFLmlnotpark: bool
    sdiPFLpllowlevel: bool
    sdiPFLplnotpark: bool
    sdiPFLfree1: bool
    sdiPFLpsr: bool
    sdiPFLpsb: bool
    sdiPFfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdiPFfree")


@dataclass
class pfDecentralizedIoOutput:
    """
    Parameters
    ----------
    sdoPFLetpflowA : `bool`
        Emergency channel 1 to Pflow control.
    sdoPFLetpflowB : `bool`
        Emergency channel 2 to Pflow control.
    sdoPFLetauxcA : `bool`
        Emergency channel 1 to aux control.
    sdoPFLetauxcB : `bool`
        Emergency channel 2 to aux control.
    sdoPFLmlSTOA : `bool`
        STO man lift channel 1.
    sdoPFLmlSTOB : `bool`
        STO man lift channel 2.
    sdoPFLetpflowrst : `bool`
        Reset emergency to Pflow control.
    sdoPFLetauxcrst : `bool`
        Reset emergency to aux control.
    sdoPFLmlrst : `bool`
        Reset emergency to man lift control.
    sdoPFLfree1 : `bool`
        Reserved for future use 1.
    sdoPFfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdoPFLetpflowA: bool
    sdoPFLetpflowB: bool
    sdoPFLetauxcA: bool
    sdoPFLetauxcB: bool
    sdoPFLmlSTOA: bool
    sdoPFLmlSTOB: bool
    sdoPFLetpflowrst: bool
    sdoPFLetauxcrst: bool
    sdoPFLmlrst: bool
    sdoPFLfree1: bool
    sdoPFfree: tuple[bool, bool, bool, bool, bool, bool] = (False, False, False, False, False, False)

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdoPFfree")


@dataclass
class pfDecentralizedIoFree:
    """
    Parameters
    ----------
    sdrPFfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    sdrPFfree: tuple[
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "sdrPFfree")


@dataclass
class auxCpuInputs:
    """
    Parameters
    ----------
    gnetAUX_siplatliftabo : `bool`
        Platform lift above enclosure lower level.
    gnetAUX_siplatliftpark : `bool`
        Platform lift not parked.
    gnetAUX_simanliftpark : `bool`
        Man lift not parked.
    gnetAUXfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetAUX_siplatliftabo: bool
    gnetAUX_siplatliftpark: bool
    gnetAUX_simanliftpark: bool
    gnetAUXfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetAUXfree")


@dataclass
class auxCpuOutputs:
    """
    Parameters
    ----------
    gnetAUX_soplatlitfsto : `bool`
        Pflow platform lift disable.
    gnetAUX_soplatlifttop : `bool`
        Pflow platform lift at/to top floor disable.
    gnetAUXfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetAUX_soplatlitfsto: bool
    gnetAUX_soplatlifttop: bool
    gnetAUXfree: tuple[
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
    ] = (False, False, False, False, False, False, False, False, False, False, False, False, False, False)

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetAUXfree")


@dataclass
class domeCpuInputs:
    """
    Parameters
    ----------
    gnetDOME_silockingpin : `bool`
        Dome locking pin retracted or door louvers not closed.
    gnetDOME_sireardoor : `bool`
        Dome rear door not closed.
    gnetDOME_sietpb : `bool`
        Dome ETPB's.
    gnetDOME_sicraneparked : `bool`
        Dome crane not parked.
    gnetDomefree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetDOME_silockingpin: bool
    gnetDOME_sireardoor: bool
    gnetDOME_sietpb: bool
    gnetDOME_sicraneparked: bool
    gnetDomefree: tuple[bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool] = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    )

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetDomefree")


@dataclass
class domeCpuOutputs:
    """
    Parameters
    ----------
    gnetDOME_sowindscreensto : `bool`
        Dome doors and windscreen drives disable.
    gnetDOME_socranesto : `bool`
        Dome crane disable.
    gnetDOME_solockingpinsto : `bool`
        Dome louvers and locking pin disable.
    gnetDOME_soreardoorsto : `bool`
        Dome rear doors drives disable.
    gnetDOME_soazdrivesto : `bool`
        Dome azimuth drives disable.
    gnetDOMEfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetDOME_sowindscreensto: bool
    gnetDOME_socranesto: bool
    gnetDOME_solockingpinsto: bool
    gnetDOME_soreardoorsto: bool
    gnetDOME_soazdrivesto: bool
    gnetDOMEfree: tuple[bool, ...] = (False,) * 11

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetDOMEfree")


@dataclass
class m1m3CpuInputs:
    """
    Parameters
    ----------
    gnetM1M3_siinterlock : `bool`
        M1M3 interlock.
    gnetM1M3_siheartbeat : `bool`
        M1M3 heartbeat input.
    gnetM1M3free : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetM1M3_siinterlock: bool
    gnetM1M3_siheartbeat: bool
    gnetM1M3free: tuple[bool, ...] = (False,) * 14

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetM1M3free")


@dataclass
class m1m3CpuOutputs:
    """
    Parameters
    ----------
    gnetM1M3_soheartbeat : `bool`
        M1M3 heartbeat output.
    gnetM1M3_soearthsto : `bool`
        M1M3 STO earthquake stop.
    gnetM1M3_soemergsto : `bool`
        M1M3 STO emergency stop.
    gnetM1M3free : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetM1M3_soheartbeat: bool
    gnetM1M3_soearthsto: bool
    gnetM1M3_soemergsto: bool
    gnetM1M3free: tuple[bool, ...] = (False,) * 13

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetM1M3free")


@dataclass
class tmaCpuInputs:
    """
    Parameters
    ----------
    gnetTMA_sibrakeoff : `bool`
        TMA brakes not engaged.
    gnetTMA_sipullcord : `bool`
        TMA CCW safety device activated.
    gnetTMA_sietpb : `bool`
        TMA ETPB's.
    gnetTMA_simcsfault : `bool`
        TMA watchdog or loss communication.
    gnetTMAfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetTMA_sibrakeoff: bool
    gnetTMA_sipullcord: bool
    gnetTMA_sietpb: bool
    gnetTMA_simcsfault: bool
    gnetTMAfree: tuple[bool, ...] = (False,) * 12

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetTMAfree")


@dataclass
class tmaCpuOutputs:
    """
    Parameters
    ----------
    gnetTMA_sodischargecap : `bool`
        TMA discharge capacitor banks.
    gnetTMA_soothersto : `bool`
        TMA other equipments disable.
    gnetTMA_somainaxissto : `bool`
        TMA main drives and brakes disable.
    gnetTMA_soccwsto : `bool`
        TMA CCW drives disable.
    gnetTMAfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetTMA_sodischargecap: bool
    gnetTMA_soothersto: bool
    gnetTMA_somainaxissto: bool
    gnetTMA_soccwsto: bool
    gnetTMAfree: tuple[bool, ...] = (False,) * 12

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetTMAfree")


@dataclass
class causes:
    """
    Parameters
    ----------
    gcauses_D1 : `bool`
        GIS fire interlock.
    gcauses_D2 : `bool`
        Catastrophic earthquake interlock.
    gcauses_D3 : `bool`
        GIS internal failure.
    gcauses_D4 : `bool`
        GIS ETPB's.
    gcauses_D5 : `bool`
        Unauthorized pier access.
    gcauses_D6 : `bool`
        Unauthorized dome access.
    gcauses_D7 : `bool`
        TMA brakes not engaged.
    gcauses_D8 : `bool`
        CCW safety device actuated.
    gcauses_D9 : `bool`
        TMA ETPB's.
    gcauses_D10 : `bool`
        Dome locking pin retracted or dome rear door louvers not closed.
    gcauses_D11 : `bool`
        Dome rear doors are not closed.
    gcauses_D12 : `bool`
        Dome ETPB's.
    gcauses_D13 : `bool`
        Dome crane not parked.
    gcauses_D14 : `bool`
        Camera rotator pin inserted.
    gcauses_D15 : `bool`
        Platform lift above enclosure lower level.
    gcauses_D16 : `bool`
        Platform lift not parked at the telescope level.
    """

    gcauses_D1: bool
    gcauses_D2: bool
    gcauses_D3: bool
    gcauses_D4: bool
    gcauses_D5: bool
    gcauses_D6: bool
    gcauses_D7: bool
    gcauses_D8: bool
    gcauses_D9: bool
    gcauses_D10: bool
    gcauses_D11: bool
    gcauses_D12: bool
    gcauses_D13: bool
    gcauses_D14: bool
    gcauses_D15: bool
    gcauses_D16: bool


@dataclass
class causes2:
    """
    Parameters
    ----------
    gcauses_D17 : `bool`
        Failed MCS watchdog or MCS loss communication.
    gcauses_D18 : `bool`
        M1M3 interlock.
    gcauses_D19 : `bool`
        Man lift not parked.
    gcauses_D20 : `bool`
        Cause D20.
    gcauses_D25 : `bool`
        Cause D25.
    gcauses_D26 : `bool`
        Cause D26.
    gcausesfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gcauses_D17: bool
    gcauses_D18: bool
    gcauses_D19: bool
    gcauses_D20: bool
    gcauses_D25: bool
    gcauses_D26: bool
    gcausesfree: tuple[bool, ...] = (False,) * 10

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gcausesfree")


@dataclass
class causesOverride:
    """
    Parameters
    ----------
    govr_D1 : `bool`
        Bypass GIS fire interlock.
    govr_D2 : `bool`
        Bypass catastrophic earthquake interlock.
    govr_D3 : `bool`
        Bypass GIS internal failure.
    govr_D4 : `bool`
        Bypass GIS ETPB's.
    govr_D5 : `bool`
        Bypass unauthorized pier access.
    govr_D6 : `bool`
        Bypass unauthorized dome access.
    govr_D7 : `bool`
        Bypass TMA brakes not engaged.
    govr_D8 : `bool`
        Bypass CCW safety device actuated.
    govr_D9 : `bool`
        Bypass TMA ETPB's.
    govr_D10 : `bool`
        Bypass dome locking pin retracted or dome rear door louvers not closed.
    govr_D11 : `bool`
        Bypass dome rear doors are not closed.
    govr_D12 : `bool`
        Bypass dome ETPB's.
    govr_D13 : `bool`
        Bypass dome crane not parked.
    govr_D14 : `bool`
        Bypass camera rotator pin inserted.
    govr_D15 : `bool`
        Bypass platform above enclosure lower level.
    govr_D16 : `bool`
        Bypass platform lift not parked at the telescope level.
    """

    govr_D1: bool
    govr_D2: bool
    govr_D3: bool
    govr_D4: bool
    govr_D5: bool
    govr_D6: bool
    govr_D7: bool
    govr_D8: bool
    govr_D9: bool
    govr_D10: bool
    govr_D11: bool
    govr_D12: bool
    govr_D13: bool
    govr_D14: bool
    govr_D15: bool
    govr_D16: bool


@dataclass
class causes2Override:
    """
    Parameters
    ----------
    govr_D17 : `bool`
        Bypass failed MCS watchdog or MCS loss communication.
    govr_D18 : `bool`
        Bypass M1M3 interlock.
    govr_D19 : `bool`
        Bypass man lift not parked.
    govr_D20 : `bool`
        Bypass cause D20.
    govr_D25 : `bool`
        Bypass cause D25.
    govr_D26 : `bool`
        Bypass cause D26.
    govrfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    govr_D17: bool
    govr_D18: bool
    govr_D19: bool
    govr_D20: bool
    govr_D25: bool
    govr_D26: bool
    govrfree: tuple[bool, ...] = (False,) * 10

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "govrfree")


@dataclass
class effects:
    """
    Parameters
    ----------
    geffects_A1 : `bool`
        GIS fire indication.
    geffects_A2 : `bool`
        Camera rotator pin inserted indication.
    geffects_A3 : `bool`
        TMA discharge capacitors bank.
    geffects_A4 : `bool`
        TMA disable other equipment.
    geffects_A5 : `bool`
        TMA main drives -STO and engage the brakes.
    geffects_A6 : `bool`
        CCW drives STO.
    geffects_A7 : `bool`
        Dome shutter doors and windscreen drives disable.
    geffects_A8 : `bool`
        Dome crane disable.
    geffects_A9 : `bool`
        Dome louvers and dome locking pin disable.
    geffects_A10 : `bool`
        Dome rear doors drives disable.
    geffects_A11 : `bool`
        Dome azimuth drives disable.
    geffects_A12 : `bool`
        STO M2 hexapods.
    geffects_A13 : `bool`
        STO M2 actuators.
    geffects_A14 : `bool`
        STO camera rotator.
    geffects_A15 : `bool`
        STO camera hexapod.
    geffects_A16 : `bool`
        Pflow platform lift disable.
    """

    geffects_A1: bool
    geffects_A2: bool
    geffects_A3: bool
    geffects_A4: bool
    geffects_A5: bool
    geffects_A6: bool
    geffects_A7: bool
    geffects_A8: bool
    geffects_A9: bool
    geffects_A10: bool
    geffects_A11: bool
    geffects_A12: bool
    geffects_A13: bool
    geffects_A14: bool
    geffects_A15: bool
    geffects_A16: bool


@dataclass
class effects2:
    """
    Parameters
    ----------
    geffects_A17 : `bool`
        Pflow platform lift at/to top floor disable.
    geffects_A18 : `bool`
        STO M1M3 actuators (earthquake stop).
    geffects_A19 : `bool`
        STO M1M3 actuators (emergency stop).
    geffects_A20 : `bool`
        Laser cut-off.
    geffects_A21 : `bool`
        Man lift disable.
    geffects_A22 : `bool`
        Effect A22.
    geffectsfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    geffects_A17: bool
    geffects_A18: bool
    geffects_A19: bool
    geffects_A20: bool
    geffects_A21: bool
    geffects_A22: bool
    geffectsfree: tuple[bool, ...] = (False,) * 10

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "geffectsfree")


@dataclass
class acks:
    """Reset system.

    Parameters
    ----------
    gack_CPUetw1rst : `bool`
        Reset CPU 1.
    gack_CPUetw2rst : `bool`
        Reset CPU 2.
    gack_AFEetacrst : `bool`
        Reset Fire Earthquake CPU access-control channel.
    gack_AFEetsfrst : `bool`
        Reset Fire Earthquake CPU summit-fire channel.
    gack_LASetrst : `bool`
        Reset Laser CPU.
    gack_M2Cetm2arst : `bool`
        Reset M2 actuators CPU.
    gack_M2Cetm2hrst : `bool`
        Reset M2 hexapod CPU.
    gack_M2Cetcrrst : `bool`
        Reset camera rotator CPU.
    gack_M2Cetchrst : `bool`
        Reset camera hexapod CPU.
    gack_PFLetpflowrst : `bool`
        Reset PFlow CPU interlock.
    gack_PFLetauxcrst : `bool`
        Reset auxiliary control CPU interlock.
    gack_PFLmlrst : `bool`
        Reset man lift control.
    gackfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gack_CPUetw1rst: bool
    gack_CPUetw2rst: bool
    gack_AFEetacrst: bool
    gack_AFEetsfrst: bool
    gack_LASetrst: bool
    gack_M2Cetm2arst: bool
    gack_M2Cetm2hrst: bool
    gack_M2Cetcrrst: bool
    gack_M2Cetchrst: bool
    gack_PFLetpflowrst: bool
    gack_PFLetauxcrst: bool
    gack_PFLmlrst: bool
    gackfree: tuple[bool, ...] = (False, False, False, False)

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gackfree")


@dataclass
class auxTel:
    """AuxTel interlock system.

    Parameters
    ----------
    gnetAUXTel_soauxtelearthquakesto : `bool`
        AuxTel earthquake STO.
    gnetAUXTelfree : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    gnetAUXTel_soauxtelearthquakesto: bool
    gnetAUXTelfree: tuple[bool, ...] = (False,) * 15

    @classmethod
    def tuple_range(cls: IsDataclass) -> tuple[int, int]:
        return find_freespace(cls, "gnetAUXTelfree")


@dataclass
class Reserved:
    """Reserved for future use.

    Parameters
    ----------
    reserved : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    reserved: tuple[bool, ...] = (False,) * 16


@dataclass
class Reserved2:
    """Reserved for future use.

    Parameters
    ----------
    reserved : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    reserved: tuple[bool, ...] = (False,) * 16


@dataclass
class Reserved3:
    """Reserved for future use.

    Parameters
    ----------
    reserved : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    reserved: tuple[bool, ...] = (False,) * 16


@dataclass
class Reserved4:
    """Reserved for future use.

    Parameters
    ----------
    reserved : `tuple` [`bool`, ...]
        Reserved for future use.
    """

    reserved: tuple[bool, ...] = (False,) * 16
