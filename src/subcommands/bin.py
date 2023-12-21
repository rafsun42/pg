from pathlib import Path
import subprocess
from typing import Annotated
import typer

from utils.vermgr import Version, getver

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ver:  Annotated[str, typer.Argument(help="available postgresql version (i.e. 15, 15.4, 16devel)")],
         prgm: Annotated[str, typer.Argument(help="a program in the bin directory")],
         args: Annotated[list[str], typer.Argument(help="options and arguments for that program (data, logfile and port number is auto included)")] = None):
    """
    bruh
    """
    verobj = getver(ver)
    prgm_path = verobj.builddir / 'bin' / prgm

    if not prgm_path.exists():
        # TODO: error
        pass

    spargs = []
    spargs.append(str(prgm_path))
    spargs = spargs + autoinclude_spargs(prgm, verobj)

    if args:
        spargs = spargs + args

    print(' '.join(spargs))

    subprocess.run(spargs)

def autoinclude_spargs(prgm:str, verobj:Version):
    spargs = []
    match prgm:
        case 'pg_ctl':
            spargs = spargs + ['-D', str(verobj.datadir)]
            spargs = spargs + ['-l', str(verobj.logfile)]
            spargs = spargs + ['-o', f'"-p {verobj.port}"']

        case 'psql':
            spargs = spargs + ['-p', str(verobj.port)]

        case 'initdb':
            spargs = spargs + ['-D', str(verobj.datadir)]

        case 'createdb':
            spargs = spargs + ['-p', str(verobj.port)]

        case _:
            spargs = []

    return spargs