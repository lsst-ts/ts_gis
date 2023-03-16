import logging

import sshtunnel
from pymodbus.client import ModbusTcpClient


def main():
    log = logging.getLogger(__name__)

    LOCALHOST = "127.0.0.1"
    SSH_PORT = 22
    LOCAL_PORT = 15020

    BASTION_IP = "gis-bastion01.cp.lsst.org"
    BASTION_USERNAME = "gis-bastion"
    PKEY_FILE = "~/.ssh/id_gis_bastion"

    GIS_IP = "192.168.180.1"
    GIS_PORT = 502

    tunnel = sshtunnel.open_tunnel(
        (BASTION_IP, SSH_PORT),
        debug_level=logging.DEBUG,
        ssh_username=BASTION_USERNAME,
        ssh_pkey=PKEY_FILE,
        remote_bind_address=(GIS_IP, GIS_PORT),
        local_bind_address=(LOCALHOST, LOCAL_PORT),
        logger=log,
    )
    tunnel.start()
    if tunnel.tunnel_is_up[(LOCALHOST, LOCAL_PORT)]:
        log.info("Tunnel is up.")
    modbus_client = ModbusTcpClient(LOCALHOST, LOCAL_PORT)
    modbus_client.connect()
    if modbus_client.connected or modbus_client.is_socket_open():
        log.info("Connection successful.")
    else:
        raise RuntimeError("Client did not connect succesfully.")
    reply = modbus_client.read_holding_registers(0, 29)
    log.info(f"{reply.registers=}")
    log.info("Closing connection.")
    modbus_client.close()
    tunnel.close()

    # ======================================================= #
    # Here you want to do the Modbus magic.
    # ======================================================= #

    log.info("finish!")


if __name__ == "__main__":
    main()
