import pathlib
import unittest
from typing import cast

from lsst.ts.gis.enums import subsystem_order
from lsst.ts.gis.register_map import (
    BitAssignment,
    WordAssignment,
    map_to_subsystems,
    parse_send_tcs,
    render_register_map,
    validate_words,
)
from lsst.ts.gis.wizardry import BITS_PER_REGISTER, NUMBER_OF_SUBSYSTEMS

SEND_TCS_PATH = pathlib.Path(__file__).resolve().parents[1] / "Send_TCS.txt"


@unittest.skipUnless(SEND_TCS_PATH.exists(), "Send_TCS.txt is not available.")
class RegisterMapTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.words = parse_send_tcs(SEND_TCS_PATH.read_text())

    def test_parse_finds_35_words(self) -> None:
        self.assertEqual(len(self.words), NUMBER_OF_SUBSYSTEMS)

    def test_each_word_has_16_bits(self) -> None:
        for word in self.words:
            self.assertEqual(len(word.bits), BITS_PER_REGISTER)

    def test_each_send_word_targets_matching_modbus_word(self) -> None:
        validate_words(self.words, NUMBER_OF_SUBSYSTEMS, BITS_PER_REGISTER)

    def test_map_to_subsystems_matches_subsystem_order(self) -> None:
        mappings = map_to_subsystems(self.words, subsystem_order=subsystem_order)

        self.assertEqual(len(mappings), NUMBER_OF_SUBSYSTEMS * BITS_PER_REGISTER)
        self.assertEqual(mappings[0].subsystem, subsystem_order[0])
        self.assertEqual(mappings[BITS_PER_REGISTER].subsystem, subsystem_order[1])


class RegisterMapParserTestCase(unittest.TestCase):
    def test_comments_are_ignored(self) -> None:
        text = """
               sendW0(
                   bit0 := TRUE,
                   //bit1 := should_not_be_seen,
                   bit1 := FALSE,
                   bit2 := FALSE,
                   bit3 := FALSE,
                   bit4 := FALSE,
                   bit5 := FALSE,
                   bit6 := FALSE,
                   bit7 := FALSE,
                   bit8 := FALSE,
                   bit9 := FALSE,
                   bit10 := FALSE,
                   bit11 := FALSE,
                   bit12 := FALSE,
                   bit13 := FALSE,
                   bit14 := FALSE,
                   bit15 := FALSE,
                   code => ModBusS0
               );
               """

        words = parse_send_tcs(text)

        self.assertEqual(words[0].bits[0].expression, "TRUE")
        self.assertEqual(words[0].bits[1].expression, "FALSE")

    def test_render_register_map_escapes_expressions(self) -> None:
        expression = 'quoted "value" and path C:\\Temp\\Send_TCS'
        words = (
            WordAssignment(
                word=0,
                output=0,
                bits=(BitAssignment(word=0, bit=0, expression=expression),),
            ),
        )

        source = render_register_map(words, subsystem_order=("gisCpuInputs",))
        namespace: dict[str, object] = {}

        exec(source, namespace)

        register_map = cast(dict[str, tuple[str, ...]], namespace["REGISTER_MAP"])
        self.assertEqual(register_map["gisCpuInputs"][0], expression)
