"""Minimal todo list manager for procrastinators"""
import click   # for the command line interfacing
import arrow   # for date handling (due/deadline)
import json    # for parsing tasks.json file; contains all the tasks.
import os      # for handling file manipulations. (saving and deleting tasks)
import shutil  # for copying the tasks.json file into appconfig directory.
from collections import deque # for manipulations on tasks.json

file_dir = click.get_app_dir('proactive')
file_path = os.path.join(file_dir, 'tasks.json')
first_time = True


class TaskSet:
    """The list of tasks at hand"""
    # TODO: --hard-reset option to generate a new tasks.json
    def __init__(self):
        # self.data = [{"id": 0}]
        self.file = None
        self.tasks = []
        if not os.path.exists(file_path):
            click.secho(f"tasks.json file doesn't exist at {file_path}, Creating...", dim=True)
            os.makedirs(file_dir, exist_ok=True)
            if not os.path.exists(file_path):
                shutil.copy('tasks.json', file_dir)
                with open(file_path, 'r+') as self.file:
                    self.data = json.load(self.file)
        else:
            with open(file_path, 'r+') as self.file:
                self.data = json.load(self.file)
        self.sort()
    def sync(self):
        with open(file_path, 'w') as file:
            json.dump(self.data, file)

    def sort(self):
        """Initially sort based on deadline"""
        # print(type(self.data))
        # a = [self.data]
        # print(a)
        # a = list(self.data)
        # print(a)
        tasks = deque(self.data)
        tasks.popleft() # remove the tutorial content from tasks.json
        for item in tasks:
            self.tasks.append(item)
        # inline sorting of the list of tasks in ascending order of due dates
        self.tasks.sort(key=lambda task: task['due'], reverse=False)
        # print(self.tasks)
        # self.tasks = list(tasks)  # I honestly have no idea why this doesn't work! :(
        # print(type(self.tasks), self.tasks)

pass_taskset = click.make_pass_decorator(TaskSet, ensure=True)


@click.group()
@pass_taskset
def cli(taskset):
    """A simple command-line todo application\n
       Intended to help(force, actually) kill procrastination.
       Or better, intended to get you to habituate acting over thinking!\n
       ஐந்தில் வளையாதது ஐம்பதில் வளையாது
    """


@cli.command()
@pass_taskset
# TODO:List tasks based on category, tags, deadlines
@click.option('-l', '--length', 'length', type=str, help="How long do you have?(xm/xh/xd)")
def list(taskset, length):
    """Lists available tasks to ACT on"""
    # sorted_taskset = taskset.sort()
    if len(taskset.tasks) <= 1:
        click.echo("No tasks - Hurray!")
    else:
        for task in taskset.tasks:
            click.echo(task.get('name'))# Why does dict.get(key) work and not dict[key]?
        # taskset.file.close()

@cli.command()
@pass_taskset
@click.option('-n', '--name', 'name', help="Name/Title of the task")
@click.option('-l', '--length', 'length', help="How long does this task take?(xm/xh/xd as in minutes/hours/days)")
# TODO: Add humanized date methods
@click.option('-d', '--due', 'due', type=(int, str), help="When's the deadline?(DD MMM) (Eg: 2 mar")
@click.option('-c', '--category', 'category', default='personal', help="Classify the task under a category")
@click.option('-t', '--tags', 'tags', default='misc', help="Classify the task under a tag")
def add(taskset, name, length, due, category, tags):
    """Let's add something to ACT upon"""
    task = {} # a task is a dictionary with at least name, length and deadline.
    id = len(taskset.data) + 2
    task['id'] = id
    # if not name:
    #     click.echo("Really? You wanna do nothing?")
    if name and length and due:
        task['name'] = name
        task['length'] = length
        date = str(due[0]).zfill(2) + ' ' + due[1] + ' ' + str(arrow.utcnow().year)
        date1 = arrow.get(date, 'DD MMM YYYY').timestamp
        task['due'] = date1

    # click.echo(task)
    taskset.data.append(task)
    taskset.sync()