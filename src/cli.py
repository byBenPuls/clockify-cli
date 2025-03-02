from datetime import datetime

import click

from src.clockify import Clockify
from src.environment import Environment
from src.methods import AllWorkspaces, StartEntryTime, StopTimeEntry

environment = Environment()


@click.group()
def cli():
    pass


@cli.command()
@click.option("--name", help="Task name")
@click.argument("workspace", default=environment.get("workspace_id"))
def start(name, workspace) -> None:
    response = StartEntryTime(Clockify(environment.password.value).http).execute(
        workspace_id=workspace, entry_time_name=name
    )

    environment["last_time_entry"] = response.id

    click.echo("Successfully started!")
    click.echo(
        f"DESC: {response.description}\tID: {response.id}\tSTART TIME: {datetime.strftime(response.start, '%d/%m/%Y, %H:%M:%S')}"
    )


@cli.command()
@click.argument("id", default=environment.get("last_time_entry"))
@click.argument("workspace", default=environment.get("workspace_id"))
def stop(workspace, id) -> None:
    del environment["last_time_entry"]

    response = StopTimeEntry(Clockify(environment.password.value).http).execute(
        workspace_id=workspace, time_entry_id=id
    )

    click.echo("Successfully stopped!")
    click.echo(
        f"DESC: {response.description}\tID: {response.id}\tSTART TIME: {datetime.strftime(response.start, '%d/%m/%Y, %H:%M:%S')}\tEND TIME: {response.end}"
    )


@cli.command()
def workspaces() -> None:
    result = AllWorkspaces(Clockify(environment.password.value).http).execute()
    name = "workspaces" if len(result) > 1 else "workspace"

    click.echo(f"You have {len(result)} {name}:")
    for i in result:
        click.echo(f"NAME: {i.name}\tID: {i.id}")


@cli.command()
@click.option("--workspace")
@click.option("--token")
def settings(workspace: str | None, token: str | None) -> None:
    if workspace:
        environment["workspace_id"] = workspace
    if token:
        environment.password.value = token
