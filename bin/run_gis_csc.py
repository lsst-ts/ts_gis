#!/usr/bin/env python

import asyncio
from lsst.ts.gis import GISCsc

asyncio.run(GISCsc.amain(index=False))
