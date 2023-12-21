from pathlib import Path
import subprocess
from typing import Annotated
import typer
from rich import print
from utils import portmgr
from utils.vermgr import getver

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main():
    pass


@app.command()
def set(ver:  Annotated[str, typer.Argument(help="available postgresql version (i.e. 15, 15.4, 16devel)")],
        port: Annotated[int, typer.Argument(help="port number (not necessary with -r option)")] = None,
        is_random: Annotated[bool, typer.Option("--random", "-r", help="set random available port")] = False):
    if not port and not is_random:
        print(f'[red]ERROR:[/red] port arg must be provided if -r is not set')
        exit(-1)

    if is_random:
        port = portmgr.availport()

    portmgr.setport(ver, port)

    print(f'Port {port} is set')