import typer

from subcommands import install, bin, ports, ver

# init main typer
pg = typer.Typer()

# register subcommands
pg.add_typer(install.app, name="install")
pg.add_typer(bin.app,     name="bin")
pg.add_typer(ports.app,   name="ports")
pg.add_typer(ver.app,     name="ver")

# run pg
if __name__ == "__main__":
    pg()
