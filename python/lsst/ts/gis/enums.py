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
    "subsystem_order",
]

from dataclasses import dataclass

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
)


@dataclass
class gisCpuInputs:
    """Main GIS CPU inputs.

    Parameters
    ----------
    sdiCPUetw1A:
        Wireless emergency pushbutton 1 channel 1.
    sdiCPUetw1B:
        Wireless emergency pushbutton 1 channel 2.
    sdiCPUetw2A:
        Wireless emergency pushbutton 2 channel 1.
    sdiCPUetw2B:
        Wireless emergency pushbutton 2 channel 2.
    sdiCPUfree1:
        Reserved for future use.
    sdiCPUpsr:
        Power supply redundancy OK.
    sdiCPUpsb:
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
    sdoCPUetw1rst:
        Wireless emergency pushbutton 1 reset.
    sdoCPUetw2rst:
        Wireless emergency pushbutton 2 reset.
    sdoCPUfireA:
        GIS fire indication channel 1.
    sdoCPUfireB:
        GIS fire indication channel 2.
    sdoCPUfree1:
        Reserved for future use 1.
    sdoCPUfree2:
        Reserved for future use 2.
    sdoCPUfree:
        Reserved for future use.
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
    sdrCPUfree:
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
    ]

    @classmethod
    def tuple_range(cls):
        return 0, 15


@dataclass
class afeDecentralizedIOInputs:
    """
    Parameters
    ----------
    sdiAFEetacA:
        Emergency channel 1 from access control.
    sdiAFEetacB:
        Emergency channel 2 from access control.
    sdiAFTetsfA:
        Emergency channel 1 from summit fire control.
    sdiAFEetsfB:
        Emergency channel 2 from summit fire control.
    sdiAFEeteaA:
        Emergency channel 1 from earthquake control.
    sdiAFEeteaB:
        Emergency channel 2 from earthquake control.
    sdiAFEupieraA:
        Unauthorized pier access channel 1.
    sdiAFEupieraB:
        Unauthorized pier access channel 2.
    sdiAFEudomeaA:
        Unauthorized dome access channel 1.
    sdiAFEudomeaB:
        Unauthorized dome access channel 2.
    sdiAFEfireA:
        Fire interlock channel 1.
    sdiAFEfireB:
        Fire interlock channel 2.
    sdiAFEfree1:
        Reserved for future use 1.
    sdiAFEfree2:
        Reserve for future use 2.
    sdiAFEpsr:
        Power supply redundancy OK.
    sdiAFEpsb:
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
    sdoAFEetacA:
        Emergency channel 1 to access control.
    sdoAFEetacB:
        Emergency channel 2 to access control.
    sdoAFEetsfA:
        Emergency channel 1 to summit fire control.
    sdoAFEetsfB:
        Emergency channel 2 to summit fire control.
    sdoAFEfree1:
        Reserved for future use 1.
    sdoAFEfree2:
        Reserved for future use 2.
    sdoAFEetacrst:
        Reset emergency to access control.
    sdoAFEetsfrst:
        Reset emergency to summit fire control.
    sdoAFEfree:
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
    sdoAFEfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool]

    @classmethod
    def tuple_range(cls):
        return 8, 15


@dataclass
class afeDecentralizedIOFree:
    """
    Parameters
    ----------
    sdrAFEfree:
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
    ]

    @classmethod
    def tuple_range(cls):
        return 0, 15


@dataclass
class laserDecentralizedIOInput:
    """
    Parameters
    ----------
    sdiLASetA:
        Emergency channel 1 from laser control.
    sdiLASetB:
        Emergency channel 2 from laser control.
    sdiLASfree1:
        Reserved for future use 1.
    sdiLASfree2:
        Reserved for future use 2.
    sdiLASfree3:
        Reserved for future use 3.
    sdiLASfree4:
        Reserved for future use 4.
    sdiLASpsr:
        Power supply redundancy OK.
    sdiLASpsb:
        Power supply balancing OK.
    sdiLASfree:
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
    sdiLASfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool]

    @classmethod
    def tuple_range(cls):
        return 8, 15


@dataclass
class laserDecentralizedIOOutputs:
    """
    sdoLASetA:
        Emergency channel 1 to laser control.
    sdoLASetB:
        Emergency channel 2 to laser control.
    sdoLASfree1:
        Reserved for future use 1.
    sdoLASfree2:
        Reserved for future use 2.
    sdoLASetrst:
        Reset emergency to laser control.
    sdoLASfree:
        Reserved for future use.
    """

    sdoLASetA: bool
    sdoLASetB: bool
    sdoLASfree1: bool
    sdoLASfree2: bool
    sdoLASetrst: bool
    sdoLASfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool]

    @classmethod
    def tuple_range(cls):
        return 5, 15


@dataclass
class laserDecentralizedIOFree:
    """
    Parameters
    ----------
    sdrLASfree:
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
    ]

    @classmethod
    def tuple_range(cls):
        return 0, 15


@dataclass
class m2cDecentralizedIOInput:
    """
    Parameters
    ----------
    sdiM2Cetm2aA:
        Emergency channel 1 from M2 actuators control.
    sdiM2Cetm2aB:
        Emergency channel 2 from M2 actuators control.
    sdiM2Cetm2hA:
        Emergency channel 1 from M2 hexapod control.
    sdiM2Cetm2hB:
        Emergency channel 2 from M2 hexapod control.
    sdiM2CetcrA:
        Emergency channel 1 from camera rotator control.
    sdiM2CetcrB:
        Emergency channel 2 from camera hexapod control.
    sdiM2Cpinins:
        Camera rotator pin inserted.
    sdiM2Cfree1:
        Reserved for future use 1.
    sdiM2Cpsr:
        Power supply redundancy OK.
    sdiM2Cpsb:
        Power supply balancing OK.
    sdiM2Cfree:
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
    sdiM2Cfree: tuple[bool, bool, bool, bool]

    @classmethod
    def tuple_range(cls):
        return 12, 15


@dataclass
class m2cDecentralizedIOOutput:
    """
    Parameters
    ----------
    sdoM2Cetm2aA:
        Emergency channel 1 to M2 actuators control.
    sdoM2Cetm2aB:
        Emergency channel 2 to M2 actuators control.
    sdoM2Cetm2hA:
        Emergency channel 1 to M2 hexapod control.
    sdoM2Cetm2hB:
        Emergency channel 2 to M2 hexapod control.
    sdoM2CetcrA:
        Emergency channel 1 to camera rotator control.
    sdoM2CetcrB:
        Emergency channel 2 to camera rotator control.
    sdoM2CetchA:
        Emergency channel 1 to camera hexapod control.
    sdoM2CetchB:
        Emergency channel 2 to camera hexapod control.
    sdoM2Cfree1:
        Reserved for future use 1.
    sdoM2Cfree2:
        Reserved for future use 2.
    sdoM2Cetm2arst:
        Reset emergency to M2 actuators control.
    sdoM2Cetm2hst:
        Reset emergency to M2 hexapod control.
    sdoM2Cetcrrst:
        Reset emergency to camera rotator control.
    sdoM2Cetchrst:
        Reset emergency to camera hexapod control.
    sdoM2Cfree:
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
    sdoM2Cfree: tuple[bool, bool]

    @classmethod
    def tuple_range(cls):
        return 14, 15


@dataclass
class m2cDecentralizedIOFree:
    """
    Parameters
    ----------
    sdrM2Cfree:
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
    ]

    @classmethod
    def tuple_range(cls):
        return 0, 15


@dataclass
class pfDecentralizedIoInputs:
    """
    Parameters
    ----------
    sdiPFLetA:
        Emergency channel 1 from Pflow & auxiliary control.
    sdiPFLetB:
        Emergency channel 2 from Pflow & auxiliary control.
    sdiPFLmlnotpark:
        Man lift not parked.
    sdiPFLpllowlevel:
        Platform lift above enclosure lower level.
    sdiPFLplnotpark:
        Platform lift not parked at the telescope level.
    sdiPFLfree1:
        Reserved for future use 1.
    sdiPFLpsr:
        Power supply redundancy OK.
    sdiPFLpsb:
        Power supply balancing OK.
    sdiPFLfree:
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
    sdiPFfree: tuple[bool, bool, bool, bool, bool, bool, bool, bool]

    @classmethod
    def tuple_range(cls):
        return 8, 15


@dataclass
class pfDecentralizedIoOutput:
    """
    Parameters
    ----------
    sdoPFLetpflowA:
        Emergency channel 1 to Pflow control.
    sdoPFLetpflowB:
        Emergency channel 2 to Pflow control.
    sdoPFLetauxcA:
        Emergency channel 1 to aux control.
    sdoPFLetauxcB:
        Emergency channel 2 to aux control.
    sdoPFLmlSTOA:
        STO man lift channel 1.
    sdoPFLmlSTOB:
        STO man lift channel 2.
    sdoPFLetpflowrst:
        Reset emergency to Pflow control.
    sdoPFLetauxcrst:
        Reset emergency to aux control.
    sdoPFLmlrst:
        Reset emergency to man lift control.
    sdoPFLfree1:
        Reserved for future use 1.
    sdoPFLfree:
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
    sdoPFfree: tuple[bool, bool, bool, bool, bool, bool]

    @classmethod
    def tuple_range(cls):
        return 10, 15


@dataclass
class pfDecentralizedIoFree:
    """
    Parameters
    ----------
    sdrPFLfree:
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
    ]

    @classmethod
    def tuple_range(cls):
        return 0, 15


@dataclass
class auxCpuInputs:
    """
    Parameters
    ----------
    gnetAUX_siplatliftabo:
        Platform lift above enclosure lower level.
    gnetAUX_siplatliftpark:
        Platform lift not parked.
    gnetAUX_simanliftpark:
        Man lift not parked.
    gnetAUXfree:
        Reserved for future use.
    """

    gnetAUX_siplatliftabo: bool
    gnetAUX_siplatliftpark: bool
    gnetAUX_simanliftpark: bool
    gnetAUXfree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 3, 15


@dataclass
class auxCpuOutputs:
    """
    Parameters
    ----------
    gnetAUX_soplatlitfsto:
        Pflow platform lift disable.
    gnetAUX_soplatifttop:
        Pflow platform lift at/to top floor disable.
    gnetAUXfree:
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
    ]

    @classmethod
    def tuple_range(cls):
        return 2, 15


@dataclass
class domeCpuInputs:
    """
    Parameters
    ----------
    gnetDOME_silockingpin:
        Dome locking pin retracted or door louvers not closed.
    gnetDOME_sireardoor:
        Dome rear door not closed.
    gnetDOME_sietpb:
        Dome ETPB's.
    gnetDOME_sicraneparked:
        Dome crane not parked.
    gnetDOMEfree:
        Reserved for future use.
    """

    gnetDOME_silockingpin: bool
    gnetDOME_sireardoor: bool
    gnetDOME_sietpb: bool
    gnetDOME_sicraneparked: bool
    gnetDomefree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 4, 15


@dataclass
class domeCpuOutputs:
    """
    Parameters
    ----------
    gnetDOME_sowindscreensto:
        Dome doors and windscreen drives disable.
    gnetDOME_socranesto:
        Dome crane disable.
    gnetDOME_solockingpinsto:
        Dome louvers and locking pin disable.
    gnetDOME_soreardoorsto:
        Dome rear doors drives disable.
    gnetDOME_soazdrivesto:
        Dome azimuth drives disable.
    gnetDOMEfree:
        Reserved for future use.
    """

    gnetDOME_sowindscreensto: bool
    gnetDOME_socranesto: bool
    gnetDOME_solockingpinsto: bool
    gnetDOME_soreardoorsto: bool
    gnetDOME_soazdrivesto: bool
    gnetDOMEfree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 5, 15


@dataclass
class m1m3CpuInputs:
    """
    Parameters
    ----------
    gnetM1M3_siinterlock:
        M1M3 interlock.
    gnetM1M3_siheartbeat:
        M1M3 heartbeat input.
    gnetM1M3free:
        Reserved for future use.
    """

    gnetM1M3_siinterlock: bool
    gnetM1M3_siheartbeat: bool
    gnetM1M3free: tuple[
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
    ]

    @classmethod
    def tuple_range(cls):
        return 2, 15


@dataclass
class m1m3CpuOutputs:
    """
    Parameters
    ----------
    gnetM1M3_soheartbeat:
        M1M3 heartbeat output.
    gnetM1M3_soearthsto:
        M1M3 STO earthquake stop.
    gnetM1M3_soemergsto:
        M1M3 STO emergency stop.
    gnetM1M3free:
        Reserved for future use.
    """

    gnetM1M3_soheartbeat: bool
    gnetM1M3_soearthsto: bool
    gnetM1M3_soemergsto: bool
    gnetM1M3free: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 3, 15


@dataclass
class tmaCpuInputs:
    """
    Parameters
    ----------
    gnetTMA_sibrakeoff:
        TMA brakes not engaged.
    gnetTMA_sipullcord:
        TMA CCW safety device activated.
    gnetTMA_sietpb:
        TMA ETPB's.
    gnetTMA_simcsfault:
        TMA watchdog or loss communication.
    """

    gnetTMA_sibrakeoff: bool
    gnetTMA_sipullcord: bool
    gnetTMA_sietpb: bool
    gnetTMA_simcsfault: bool
    gnetTMAfree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 4, 15


@dataclass
class tmaCpuOutputs:
    """
    Parameters
    ----------
    gnetTMA_sodischargecap:
        TMA discharge capacitor banks.
    gnetTMA_soothersto:
        TMA other equipments disable.
    gnetTMA_somainaxissto:
        TMA main drives and brakes disable.
    gnetTMA_soccwsto:
        TMA CCW drives disable.
    gnetTMAfree:
        Reserved for future use.
    """

    gnetTMA_sodischargecap: bool
    gnetTMA_soothersto: bool
    gnetTMA_somainaxissto: bool
    gnetTMA_soccwsto: bool
    gnetTMAfree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 4, 15


@dataclass
class causes:
    """
    Parameters
    ----------
    gcauses_D1:
        GIS fire interlock.
    gcauses_D2:
        Catastrophic earthquake interlock.
    gcauses_D3:
        GIS internal failure.
    gcauses_D4:
        GIS ETPB's.
    gcauses_D5:
        Unauthorized pier access.
    gcauses_D6:
        Unauthorized dome access.
    gcauses_D7:
        TMA brakes not engaged.
    gcauses_D8:
        CCW safety device actuated.
    gcauses_D9:
        TMA ETPB's.
    gcauses_D10:
        Dome locking pin retracted or dome rear door louvers not closed.
    gcauses_D11:
        Dome rear doors are not closed.
    gcauses_D12:
        Dome ETPB's.
    gcauses_D13:
        Dome crane not parked.
    gcauses_D14:
        Camera rotator pin inserted.
    gcauses_D15:
        Platform lift above enclosure lower level.
    gcauses_D16:
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
    gcauses_D17:
        Failed MCS watchdog or MCS loss communication.
    gcauses_D18:
        M1M3 interlock.
    gcauses_D19:
        Man lift not parked.
    gcausesfree:
        Reserved for future use.
    """

    gcauses_D17: bool
    gcauses_D18: bool
    gcauses_D19: bool
    gcausesfree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 3, 15


@dataclass
class causesOverride:
    """
    Parameters
    ----------
    govr_D1:
        Bypass GIS fire interlock.
    govr_D2:
        Bypass catastrophic earthquake interlock.
    govr_D3:
        Bypass GIS internal failure.
    govr_D4:
        Bypass GIS ETPB's.
    govr_D5:
        Bypass unauthorized pier access.
    govr_D6:
        Bypass unauthorized dome access.
    govr_D7:
        Bypass TMA brakes not engaged.
    govr_D8:
        Bypass CCW safety device actuated.
    govr_D9:
        Bypass TMA ETPB's.
    govr_D10:
        Bypass dome locking pin retracted or dome rear door louvers not closed.
    govr_D11:
        Bypass dome rear doors are not closed.
    govr_D12:
        Bypass dome ETPB's.
    govr_D13:
        Bypass dome crane not parked.
    govr_D14:
        Bypass camera rotator pin inserted.
    govr_D15:
        Bypass platform above enclosure lower level.
    govr_D16:
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
    govr_D17:
        Bypass failed MCS watchdog or MCS loss communication.
    govr_D18:
        Bypass M1M3 interlock.
    govr_D19:
        Bypass man lift not parked.
    govrfree:
        Reserved for future use.
    """

    govr_D17: bool
    govr_D18: bool
    govr_D19: bool
    govrfree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 3, 15


@dataclass
class effects:
    """
    Parameters
    ----------
    geffects_A1:
        GIS fire indication.
    geffects_A2:
        Camera rotator pin inserted indication.
    geffects_A3:
        TMA discharge capacitors bank.
    geffects_A4:
        TMA disable other equipment.
    geffects_A5:
        TMA main drives -STO and engage the brakes.
    geffects_A6:
        CCW drives STO.
    geffects_A7:
        Dome shutter doors and windscreen drives disable.
    geffects_A8:
        Dome crane disable.
    geffects_A9:
        Dome louvers and dome locking pin disable.
    geffects_A10:
        Dome rear doors drives disable.
    geffects_A11:
        Dome azimuth drives disable.
    geffects_A12:
        STO M2 hexapods.
    geffects_A13:
        STO M2 actuators.
    geffects_A14:
        STO camera rotator.
    geffects_A15:
        STO camera hexapod.
    geffects_A16:
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
    geffects_A17:
        Pflow platform lift at/to top floor disable.
    geffects_A18:
        STO M1M3 actuators (earthquake stop).
    geffects_A19:
        STO M1M3 actuators (emergency stop).
    geffects_A20:
        Laser cut-off.
    geffects_A21:
        Man lift disable.
    geffectsfree:
        Reserved for future use.
    """

    geffects_A17: bool
    geffects_A18: bool
    geffects_A19: bool
    geffects_A20: bool
    geffects_A21: bool
    geffectsfree: tuple[
        bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool
    ]

    @classmethod
    def tuple_range(cls):
        return 5, 15
