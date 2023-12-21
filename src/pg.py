import typer

from subcommands import install, bin, ports

# init main typer
pg = typer.Typer()

# register subcommands
pg.add_typer(install.app, name="install")
pg.add_typer(bin.app,     name="bin")
pg.add_typer(ports.app,   name="ports")

# run pg
if __name__ == "__main__":
    pg()
