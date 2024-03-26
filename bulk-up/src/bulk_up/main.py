import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Bulk Up
    """


@app.command()
def shoot():
    """
    bulk the thing
    """
    typer.echo("bulk the thing")


@app.command()
def load():
    """
    loading the bulk
    """
    typer.echo("Loading bulk")