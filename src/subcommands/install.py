from pathlib import Path
from typing import Annotated
import typer
from rich import print
from utils import config
import subprocess

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(srcdir: Annotated[Path,typer.Argument(help="postgresql source path")]):
    if not srcdir.exists():
        print(f'[red]ERROR:[/red] path "{srcdir}" does not exist')
        exit(-1)

    ver = get_version_name(srcdir)

    if not ver:
        print(f'[red]ERROR:[/red] unable to retrieve version name')
        exit(-1)

    ver = typer.prompt("Version name", default=ver)

    cfg = config.get_config()

    run_make(srcdir, cfg.buildir / ver)

def run_make(srcdir: Path, buildir: Path) -> None:
    # TODO: delete build dir
    buildir.mkdir(parents=True, exist_ok=True)

    # # run configure
    # print("Configuring ..")
    # subprocess.run([
    #     f'{srcdir}/configure',
    #     f'--prefix={buildir}',
    #     '--enable-debug',
    #     '--enable-cassert',
    #     '--without-icu'
    #     # "CFLAGS='-g3 -O0'", #TODO: fix it
    # ], cwd=buildir)

    # # run make
    # print("Building ..")
    # res = subprocess.run('nproc', capture_output=True)
    # nproc = int(res.stdout.decode('utf8'))

    # subprocess.run([
    #     'make',
    #     f'-j{nproc}'
    # ], cwd=buildir)

    # print("Installing ..")
    # subprocess.run([
    #     'make',
    #     'install'
    # ], cwd=buildir)

    # print("Cleaning ..")
    # subprocess.run([
    #     'make',
    #     'clean'
    # ], cwd=buildir)

    # TODO: assign a port

def get_version_name(srcdir: Path) -> str:
    """
    Returns PACKAGE_VERSION variable from srcdir/configure file.
    """
    try:
        with open(srcdir / 'configure', 'r') as f:
            line = f.readline()
            while line:
                if (line.startswith('PACKAGE_VERSION')):
                    ver = line.split('=')[1]
                    ver = ver[1:-2] # strips off wrapping single quote
                    return ver

                line = f.readline()
        return None
    except:
        return None
