from pathlib import Path

class Config:
    basedir:   Path = None
    buildir:   Path = None
    datadir:   Path = None
    srcdir:    Path = None

    def __init__(self) -> None:
        self.basedir = Path.home()  / 'postgres'
        self.buildir = self.basedir / 'build'
        self.datadir = self.basedir / 'data'
        self.srcdir  = self.basedir / 'src'

_config: Config = None

def get_config() -> Config:
    global _config
    if not _config:
        _config = Config()
    return _config
