__all__ = ["CONFIG_SCHEMA"]

import yaml

CONFIG_SCHEMA = yaml.safe_load(
    """
$schema: http://json-schema.org/draft-07/schema#
$id: https://github.com/lsst-ts/ts_GIS/blob/main/schema/GIS.yaml
title: GIS v3
description: Schema for GIS configuration files
type: object
properties:
  telemetry_interval:
    description: The interval for the loop to query the device (second).
    type: number
  modbus_host:
    description: The host of the modbus server.
    type: string
    format: hostname
  modbus_port:
    description: The port of the modbus server.
    type: integer
  bastion_host:
    description: The hostname for the bastion server.
    type: string
    format: hostname
  bastion_port:
    description: The ssh port for the bastion server.
    type: integer
  tunnel_host:
    description: This is the hostname for the local bind address of the tunnel.
    type: string
    format: hostname
  tunnel_port:
    description: This is the port for the local bind address of the tunnel.
    type: integer
  ssh_username:
    description: This is the name of the user to authenticate the ssh tunnel.
    type: string
  pkey:
    description: This is the file location of the private key for the user to authenticate the ssh tunnel.
    type: string
required:
  - telemetry_interval
  - modbus_host
  - modbus_port
  - bastion_host
  - bastion_port
  - tunnel_host
  - tunnel_port
  - ssh_username
  - pkey
additionalProperties: false
"""
)
