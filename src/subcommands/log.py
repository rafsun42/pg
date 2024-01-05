from pathlib import Path
from typing import Annotated
import typer
from rich import print
from utils import config
from subcommands.ver import resolve_ver
from utils.vermgr import Version, getver
from sys import exit

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
         ver:
         Annotated[str, typer.Argument(
             help="available postgresql version (i.e. 15, 15.4, 16devel)"
         )],

         is_filename:
         Annotated[bool, typer.Option("--filepath", "-f",
              help="prints filepath instead of printing the log"
         )] = False):

    ver = resolve_ver(ver)
    verobj = getver(ver)
    logfile = verobj.logfile

    if is_filename:
        print(logfile)
        exit(0)

    with open(logfile, 'r') as f:
        print(f.read())
