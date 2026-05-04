"""Parse PLC Send_TCS structured text into GIS register mappings."""

import re
from dataclasses import dataclass

SEND_BLOCK_RE = re.compile(r"sendW(?P<word>\d+)\((?P<body>.*?)code\s*=>\s*ModBusS(?P<output>\d+)\s*\)", re.S)
BIT_RE = re.compile(r"bit(?P<bit>\d+)\s*:=\s*(?P<expr>[^,\n]+)")
COMMENT_RE = re.compile(r"//.*")


@dataclass(frozen=True)
class BitAssignment:
    """One PLC expression assigned to one bit in a Modbus word.

    Attributes
    ----------
    word : `int`
        Modbus word number.
    bit : `int`
        Bit number within the word.
    expression : `str`
        PLC expression assigned to the bit.
    """

    word: int
    bit: int
    expression: str


@dataclass(frozen=True)
class WordAssignment:
    """All bit assignments for one ``sendW`` block.

    Attributes
    ----------
    word : `int`
        Word number from the ``sendW`` block name.
    output : `int`
        Modbus output word number from the ``code => ModBusS`` target.
    bits : `tuple` [`BitAssignment`, ...]
        Bit assignments parsed from the block body.
    """

    word: int
    output: int
    bits: tuple[BitAssignment, ...]


@dataclass(frozen=True)
class RegisterBitMapping:
    """Mapping from a Modbus bit to a GIS subsystem and PLC expression.

    Attributes
    ----------
    word : `int`
        Modbus word number.
    bit : `int`
        Bit number within the word.
    subsystem : `str`
        GIS subsystem name associated with the word.
    expression : `str`
        PLC expression assigned to the bit.
    """

    word: int
    bit: int
    subsystem: str
    expression: str


def strip_comments(text: str) -> str:
    """Remove structured-text line comments.

    Parameters
    ----------
    text : `str`
        Structured text to process.

    Returns
    -------
    text : `str`
        Input text with ``//`` comments removed.
    """
    return COMMENT_RE.sub("", text)


def parse_send_tcs(text: str) -> tuple[WordAssignment, ...]:
    """Parse Send_TCS structured text into word assignments.

    Parameters
    ----------
    text : `str`
        Contents of a PLC ``Send_TCS`` structured-text program.

    Returns
    -------
    words : `tuple` [`WordAssignment`, ...]
        Parsed word assignments in the order found in ``text``.
    """
    text = strip_comments(text)
    words: list[WordAssignment] = []

    for match in SEND_BLOCK_RE.finditer(text):
        word = int(match.group("word"))
        output = int(match.group("output"))
        body = match.group("body")
        bits = parse_bits(word, body)
        words.append(WordAssignment(word=word, output=output, bits=bits))

    return tuple(words)


def parse_bits(word: int, body: str) -> tuple[BitAssignment, ...]:
    """Parse bit assignments from one ``sendW`` block body.

    Parameters
    ----------
    word : `int`
        Modbus word number associated with the block.
    body : `str`
        Body text of one ``sendW`` call.

    Returns
    -------
    bits : `tuple` [`BitAssignment`, ...]
        Parsed bit assignments in the order found in ``body``.
    """
    bits: list[BitAssignment] = []

    for match in BIT_RE.finditer(body):
        bits.append(
            BitAssignment(word=word, bit=int(match.group("bit")), expression=match.group("expr").strip())
        )

    return tuple(bits)


def validate_words(words: tuple[WordAssignment, ...], expected_words: int, bits_per_word: int) -> None:
    """Validate parsed word and bit assignments.

    Parameters
    ----------
    words : `tuple` [`WordAssignment`, ...]
        Parsed word assignments to validate.
    expected_words : `int`
        Expected number of contiguous Modbus words.
    bits_per_word : `int`
        Expected number of bit assignments per word.

    Raises
    ------
    ValueError
        Raised if word numbers are not contiguous, a ``sendW`` block writes
        to the wrong ``ModBusS`` output, or bit numbers are not contiguous.
    """
    word_numbers = [word.word for word in words]
    expected_word_numbers = list(range(expected_words))

    if word_numbers != expected_word_numbers:
        raise ValueError(f"Expected words {expected_word_numbers}, got {word_numbers}")

    for word in words:
        if word.word != word.output:
            raise ValueError(f"sendW{word.word} write to ModBusS{word.output}")

        bit_numbers = [bit.bit for bit in word.bits]
        expected_bit_numbers = list(range(bits_per_word))
        if bit_numbers != expected_bit_numbers:
            raise ValueError(f"sendW{word.word} expected bits {expected_bit_numbers}, got {bit_numbers}")


def map_to_subsystems(
    words: tuple[WordAssignment, ...], subsystem_order: tuple[str, ...]
) -> tuple[RegisterBitMapping, ...]:
    """Map parsed word assignments to GIS subsystem names.

    Parameters
    ----------
    words : `tuple` [`WordAssignment`, ...]
        Parsed word assignments.
    subsystem_order : `tuple` [`str`, ...]
        GIS subsystem names ordered by Modbus register index.

    Returns
    -------
    mappings : `tuple` [`RegisterBitMapping`, ...]
        Flat mapping from word and bit positions to subsystem names and PLC
        expressions.

    Raises
    ------
    IndexError
        Raised if ``subsystem_order`` does not contain an entry for a parsed
        word.
    """
    mappings: list[RegisterBitMapping] = []

    for word in words:
        subsystem = subsystem_order[word.word]
        for bit in word.bits:
            mappings.append(
                RegisterBitMapping(
                    word=word.word, bit=bit.bit, subsystem=subsystem, expression=bit.expression
                )
            )

    return tuple(mappings)


def render_register_map(words: tuple[WordAssignment, ...], subsystem_order: tuple[str, ...]) -> str:
    """Render parsed assignments as a Python register-map module.

    Parameters
    ----------
    words : `tuple` [`WordAssignment`, ...]
        Parsed word assignments.
    subsystem_order : `tuple` [`str`, ...]
        GIS subsystem names ordered by Modbus register index.

    Returns
    -------
    source : `str`
        Python source defining ``REGISTER_MAP``.

    Raises
    ------
    IndexError
        Raised if ``subsystem_order`` does not contain an entry for a parsed
        word.
    """
    lines = [
        "# This file is generated by bin/generate_register_map.py.",
        "# Do not edit manually.",
        "",
        "REGISTER_MAP = {",
    ]

    for word in words:
        subsystem = subsystem_order[word.word]
        lines.append(f'    "{subsystem}": (')
        for bit in word.bits:
            lines.append(f'        "{bit.expression}",')
        lines.append("    ),")

    lines.append("}")
    lines.append("")
    return "\n".join(lines)
