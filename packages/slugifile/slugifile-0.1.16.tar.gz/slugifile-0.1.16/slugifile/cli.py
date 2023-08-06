# -*- coding: utf-8 -*-

"""Console script for slugifile."""
import sys
import click

from slugifile.slugifile import slugifile_directory


@click.command()
@click.option(
    "-p",
    "--path",
    type=str,
    help="Path to the folder you what to peform the action on.",
)
def main(path=None):
    """Console script for slugifile."""
    click.echo("Processing: {}".format(path))
    click.echo()
    result = slugifile_directory(path)

    if (
        "success" in result
        and "messages" in result
        and result["success"]
        and len(result["messages"])
    ):
        for message in result["messages"]:
            click.echo(message)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
