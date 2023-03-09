__all__ = ["execute_csc"]

import asyncio

from . import GISCsc


def execute_csc():
    asyncio.run(GISCsc.amain(index=None))
