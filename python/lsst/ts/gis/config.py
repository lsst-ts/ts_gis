__all__ = ["CONFIG_SCHEMA"]

import yaml

CONFIG_SCHEMA = yaml.safe_load(
    """
$schema: http://json-schema.org/draft-07/schema#
$id: https://github.com/lsst-ts/ts_GIS/blob/master/schema/GIS.yaml
title: GIS v1
description: Schema for CBP configuration files
type: object
properties:
  telemetry_interval:
    description: The interval for the loop to query the device.
    type: number
  host:
    description: The host of the modbus server
    type: string
    format: hostname
  port:
    description: The port of the modbus server.
    type: integer
required: [telemetry_interval]
additionalProperties: false
"""
)
