"""Minimal todo list manager for procrastinators"""
import click # for the command line interfacing
import arrow # for date handling (due/deadline)
import json  # for parsing tasks.json file; contains all the tasks.
import os    # for handling file manipulations. (saving and deleting tasks)

file_dir = click.get_app_dir('proactive')
file_path = os.path.join(file_dir, 'tasks.json')
first_time = True


class TaskSet:
    """The list of tasks at hand"""

    def __init__(self):
        self.data = [{"id": 0}]
        self.file = None
        if not os.path.exists(file_path):
            click.echo(f"tasks.json file doesn't exist at {file_path}, Creating...")
            os.makedirs(file_dir, exist_ok=True)
            if not os.path.exists(file_path):
                with open(file_path, 'w+') as self.file:
                    json.dump(self.data, self.file)
        else:
            with open(file_path, 'r+') as self.file:
                self.data = json.load(self.file)

pass_taskset = click.make_pass_decorator(TaskSet, ensure=True)


@click.group()
@pass_taskset
def cli(taskset):
    """A simple command-line todo application"""


@cli.command()
@pass_taskset
# @click.option('-l', '--list')
def list(taskset):
    if len(taskset.data) <= 1:
        click.echo("No tasks - Hurray!")
    else:
        for task in taskset.data:
            click.secho(task['name'], fg='green', blink=True, bold=True)
        taskset.file.close()