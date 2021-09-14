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
    default: 0.5
  host:
    description: The host of the modbus server
    type: string
    format: hostname
    default: 192.168.180.1
  port:
    description: The port of the modbus server.
    type: integer
    default: 502
required: [telemetry_interval]
additionalProperties: false
"""
)
