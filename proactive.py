"""Minimal todo list manager for procrastinators"""
import click   # for the command line interfacing
import arrow   # for date handling (due/deadline)
import json    # for parsing tasks.json file; contains all the tasks.
import os      # for handling file manipulations. (saving and deleting tasks)
import shutil  # for copying the tasks.json file into appconfig directory.
import math    # for ceiling user task lengths
from collections import deque  # for manipulations on tasks.json

file_dir = click.get_app_dir('proactive')
file_path = os.path.join(file_dir, 'tasks.json')
first_time = True


class TaskSet:
    """The list of tasks at hand"""
    # TODO: --hard-reset option to generate a new tasks.json
    def __init__(self):
        self.file = None
        self.tasks = []
        self.id_list = []
        self.current_task = None
        self.change_settings = False
        if not os.path.exists(file_path):
            click.secho("tasks.json file doesn't exist at %s, Creating..." % file_path, dim=True)
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
        # self.settings_update()
        # print("Current data dump: %s " % self.data)
        with open(file_path, 'w') as file:
            json.dump(self.data, file)

    def settings_update(self):
        # print("Calling settings: %s" % self.current_task)
        settings = self.data[1]  # 0 is tutorial, 1 is settings
        # print("Current settings: %s" % self.data[1])
        settings['current_task'] = self.current_task
        self.data[1] = settings
        # print("Current settings: %s" % self.data[1])
        self.sync()

    def sort(self):
        """Initially sort based on deadline"""
        tasks = deque(self.data)
        tasks.popleft()  # remove the tutorial content from tasks.json
        self.settings = tasks.popleft()  # remove the settings content from tasks.json
        self.current_task = self.settings['current_task'] if 'current_task' in self.settings else None
        for item in tasks:
            if item['id'] > 0:
                self.tasks.append(item)
                self.id_list.append(item['id'])
        # inline sorting of the list of tasks in ascending order of due dates
        self.tasks.sort(key=lambda task: task['due'], reverse=False)

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
# The following default of 3 signifies default availability of 3 hrs
@click.option('-l', '--length', 'length', type=float, default=3, help="How long do you have in hours?(xh/x.yh)")
def list(taskset, length):
    """Lists available tasks to ACT on"""
    # sorted_taskset = taskset.sort()
    tasks = []
    if not length:
        click.secho("Assuming you have 3 hrs...", dim=True)
    if length:
        for task in taskset.tasks:
            if math.floor(float(task['length'])) <= math.ceil(length):
                tasks.append(task)
    if len(taskset.tasks) == 0:
        click.echo("No tasks - Hurray!")
    elif len(tasks) == 0:
        if click.confirm("Uh oh... We have tasks, but shall take longer. Wanna take a peek?"):
            for task in taskset.tasks:
                blink_flag = False
                t = "(ID:%s) %s needs %s hr(s) due on %s" % (task['id'],
                                                             task['name'],
                                                             task['length'],
                                                             arrow.get(task['due']).format('DD-MMM'))
                if arrow.get(task['due']).format('DD-MMM') <= arrow.now().format('DD-MMM'):
                    fg_color = 'red'
                    if arrow.get(task['due']).format('DD-MMM') == arrow.now().format('DD-MMM'):
                        fg_color = 'yellow'
                        blink_flag = True
                else:
                    fg_color = 'blue'
                # if taskset.tasks.index(task) == 0:
                click.secho(t, fg=fg_color, blink = blink_flag)
                # else:
                #     click.echo(t)
    else:
        for task in tasks:
            blink_flag = False
            t = "(ID:%s) %s needs %s hr(s) due on %s" % (task['id'],
                                               task['name'],
                                               task['length'],
                                               arrow.get(task['due']).format('DD-MMM'))
            if arrow.get(task['due']).format('DD-MMM') <= arrow.now().format('DD-MMM'):
                fg_color = 'red'
                if arrow.get(task['due']).format('DD-MMM') == arrow.now().format('DD-MMM'):
                    blink_flag = True
                    fg_color = 'yellow'
            else:
                fg_color = 'green'

            if tasks.index(task) == 0:
                t += " <--- Current task"
                taskset.current_task = task
                click.secho(t, fg=fg_color, blink=blink_flag)
            else:
                click.secho(t, fg='blue')
    taskset.settings_update()

@cli.command()
@pass_taskset
@click.option('-n', '--name', 'name', help="Name/Title of the task")
@click.option('-l', '--length', 'length', type=float, help="How long does this task take in hours?(xh or x.yh)")
# TODO: This date method works for the current year only. Need to resolve.
# Made available only for current year to support the philosophy. (This is not for long-term tasks)
@click.option('-d', '--due', 'due', type=(int, str), help="When's the deadline?(DD MMM) (Eg: 2 mar")
@click.option('-c', '--category', 'category', default='personal', help="Classify the task under a category")
@click.option('-t', '--tags', 'tags', default='misc', help="Classify the task under a tag")
def add(taskset, name, length, due, category, tags):
    """Let's add something to ACT upon"""
    task = {}  # a task is a dictionary with at least name, length and deadline.
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

    taskset.data.append(task)
    taskset.sync()

@cli.command()
@click.option('-i', '--id', 'id', type=int, help="Give the ID of the task you wanna do.")
@pass_taskset
def do(taskset, id):
    """Do 'current task' if selected, or give an ID by -i"""
    # if not id:
        # click.echo(id, taskset.current_task)
    click.echo("(Available task IDs for ref: %s )" % taskset.id_list)
    if taskset.current_task is not None:
        id = taskset.current_task['id']
    while (id is None or taskset.current_task is None or (id not in taskset.id_list)):
        id = click.prompt("Enter a (valid) task ID: ", type=int)
        if id in taskset.id_list:
            taskset.current_task = [task if task['id'] == id else None for task in taskset.tasks].pop()
            taskset.settings_update()
    click.echo("Do task (ID: %s)?" % id)
    if click.confirm("If you 'do' a task, it gets 'done' by default. There's no going back. Proceed?"):
        for item in taskset.data:
            if item['id'] == id:
                item['id'] = -id
        taskset.sync()

    # if not id == -2: # 0 represents tuts, 1 represents default_settings, -1 represents archived
    #     id = taskset.current_task[]