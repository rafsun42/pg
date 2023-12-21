from rich import print

from . import config
from . import portmgr


class Version:
    def __init__(self, ver: str) -> None:
        pass

def resolvever(ver:str) -> str:
    return ver

def getver(ver:str) -> Version:
    """
    Returns Version object for `ver`.

    `ver` is a folder name in the build directory. If only major version name
    is provided (i.e. 15), then it is resolved to available highest minor (i.e.
    15.5).
    """
    cfg = config.get_config()
    ver = resolvever(ver)

    verobj = Version(ver)
    verobj.ver = ver
    verobj.builddir = cfg.buildir / ver
    verobj.srcdir   = cfg.srcdir  / ver
    verobj.datadir  = cfg.datadir / ver
    verobj.logfile  = verobj.datadir / 'logfile'
    verobj.port     = portmgr.getport(ver)

    if verobj.port is None:
        print(f'ERROR: port is not set for {ver}')
        print(f'Try pg ports --help')
        exit(-1)

    return verobj
