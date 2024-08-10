from pathlib import Path

import typer

from typing_extensions import Annotated

app = typer.Typer()


def main(
    file_path: Annotated[
        Path,
        typer.Argument(
            help=(
                """
            Path of the file containing OpenStack authentication information.

            The expected JSON file format is as follows:

\b
[
    {
	"auth_url": "string",
	"project_name": "string",
	"username": "string",
	"password": "string",
	"user_domain_name": "string",
	"project_domain_name": "string"
    }
]
            """
            )
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="""
\b
Path of the output file, will override if file already exists
             
                """
        ),
    ] = "output.xlsx",
):
    pass


app.command()(main)

if __name__ == "__main__":
    app()
