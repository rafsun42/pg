import typer

from subcommands import install, bin, ports, ver, log

# init main typer
pg = typer.Typer()

# register subcommands
pg.add_typer(install.app, name="install")
pg.add_typer(bin.app,     name="bin")
pg.add_typer(ports.app,   name="ports")
pg.add_typer(ver.app,     name="ver")
pg.add_typer(log.app,     name="log")

# run pg
if __name__ == "__main__":
    pg()
