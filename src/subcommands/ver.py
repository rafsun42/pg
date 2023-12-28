from pathlib import Path
from typing import Annotated
import typer
from rich import print
from utils import config

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
         ver:
         Annotated[str, typer.Argument(
             help="available postgresql version (i.e. 15, 15.4, 16devel)"
         )] = None):
    if not ver:
        for v in get_versions():
            print(v)
        return

    ver = resolve_ver(ver)
    print(ver)

def get_versions():
    """
    Returns name of all versions. This is essentially dir names inside the
    build directory.
    """
    out = []
    cfg = config.get_config()
    for v in cfg.buildir.iterdir():
        if v.is_dir():
            out.append(v.name)
    return out

def resolve_ver(ver:str):
    """
    Resolves 'ver'.

    NOTE: this algorithm may not be very smart and needs to be upgraded
    occasionally.
    """
    versions = get_versions()
    cfg = config.get_config()

    # if there is dir exists with the name of ver, then return it
    if (cfg.buildir / ver).exists():
        return ver

    # if already fully qualified version name i.e. 14.5
    if '.' in ver:
        return ver

    # if ver is an int, then it is a major version i.e. 14
    # returns the one with highest minor version
    if ver.isdigit():
        allmajors = list(filter(lambda x: x.split('.')[0] == ver and x.split('.')[1].isdigit(), versions))
        allmajors.sort(key=lambda x: x.split('.')[1], reverse=True)

        if len(allmajors) != 0:
            return allmajors[0]

    guesses = list(filter(lambda x: x.startswith(ver), versions))
    guesses.sort(reverse=True)

    if len(guesses) != 0:
        return guesses[0]

    print(f'ERROR: unable to resolve version "{ver}"')
    exit(-1)
