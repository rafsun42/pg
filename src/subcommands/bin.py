import subprocess
import typer
from pathlib import Path
from typing import Annotated
from utils.vermgr import Version, getver
from sys import exit

app = typer.Typer()

# Subcommand: pg bin
@app.callback(invoke_without_command=True)
def main(
         ver:
         Annotated[str, typer.Argument(
             help="available postgresql version (i.e. 15, 15.4, 16devel)"
         )],

         prgm:
         Annotated[str, typer.Argument(
             help="a program in the bin directory"
                  " (i.e. pg_ctl, psql, createdb)"
         )],

         return_path:
         Annotated[bool, typer.Option("--filepath", "-f",
              help="prints filepath of the program instead of executing it"
         )] = False,

         args:
         Annotated[list[str], typer.Argument(
             help="options and arguments for that program (data, logfile and"
                  "port number is auto included)"
         )] = None
         ):
    """
    Exmaple:\n
      pg bin 15.5 initdb\n
      pg bin 15.5 pg_ctl start\n
      pg bin 15.5 createdb mydatabase\n
      pg bin 15.5 psql mydatabase\n
    \n
    Following arguments and option are auto included:\n
      Data directory\n
      Logfile path\n
      Port number\n
    """
    verobj = getver(ver)
    prgm_path = verobj.builddir / 'bin' / prgm

    if return_path:
        print(prgm_path)
        exit(0)

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
