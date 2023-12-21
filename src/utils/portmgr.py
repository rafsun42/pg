import json
from pathlib import Path
import socket

from . import config

PORT_FILE = 'ports.json'

def getport(ver:str, autoset:bool=False) -> int:
    """
    Returns port number of `ver` stored in a config file. Availability of the
    port is not checked.

    Returns None if no port found in config. Unless `autoset` is set. In that
    case, an available port is stored in config and returned.
    """
    ports:dict = {}
    with open(__port_filepath(), 'r') as f:
        ports = json.load(f)

    if ver not in ports.keys():
        if autoset:
            # TODO: implement autoset
            pass
        else:
            return None
    else:
        return ports[ver]

def setport(ver:str, port:int) -> None:
    ports = {}
    if __port_filepath().exists():
        with open(__port_filepath(), 'r') as f:
            ports = json.load(f)

    ports[ver] = port
    with open(__port_filepath(), 'w') as f:
        ports = json.dump(ports, f)

def availport() -> int:
    """
    Returns an available port number
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    addr = s.getsockname()
    s.close()
    return int(addr[1])

def __port_filepath() -> Path:
    cfg = config.get_config()
    port_filepath = cfg.basedir / PORT_FILE
    return port_filepath