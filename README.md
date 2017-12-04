# Proactive (Work-in-progress)
###  (*Cli based application*)

Uses Click, colorama, arrow - Python libs

---

Hey, if you would rather try the app, clone it and go
```python
cd proactive-master
pip install .
act tut
```
### Task basics

* Name - The name of the task
* Length - The time that shall be needed to complete the task
* Deadline - The date of completion
---

Sample command line parsing usage:

__$ act add -n "Clean room" -l 3.5 -d 20 Dec__
  > -n/--name  - The name of the task
  > -l/--length - The time required for the task
  > -d/--due - The due/deadline of the task


__$ act list__ (empty or -l 3.5)
> If empty, prints task of at least 3 hr long task or based on the available time(-l)

__$ act do__(empty or -i 3)
>Do a task based on id(-i)


Why another todo app?
---------------------
Note:

I know, I know. Another todo application. But bear with me.
I've tried and used a lot of "minimal" todo applications.
Todoist, any.do, wunderlist, ctodo, todo.txt, taskwarrir, etc.

Don't mistake me, I'm still trying to find an optimal one for me among them. But I'm finding each of them lacking(or really abundant) with too many options distracting me. They are beautifully designed with so many features, and they rock on their own forte.

This app, for eg. is heavily inspired by taskwarrior, but I am finding it hard to use it too. I need patience, which I obviously don't have.

And I'm strangely attracted to command line applications. Hey, I'm a linux fan, can't help it. And I love working with python, so just gave it a shot.
1. Minimal
    * Minimalism is part and parcel of the application. The purpose of the application is to help stop procrastination, not encourage it by being too extensive.
    * User should be able to add a task straight away with __act add__ (name, length and due are necessary)
2. Listing
    * Listing tasks should be as easy as calling the application with __act list__.
    * Or sort out based on available time for the user __act list -l__ <hours> (*eg: act -l 3.5*)
3. Deadlines
    * Deadlines can only be days: Some-date(of the format <DD MMM> and not particular time

6. Length of tasks
    * Available length of task is hour (Show minutes in hours, eg: 30m = 0.5)
    * Having a task of length greater than a few hrs doesn't work - You will not complete it, Trust me. We need to stop procrastinating.
    * Even if you have a task of days, chunk it down to hours in multiple parts and add separately. :)
7. Give emphasis in this order RED>GREEN>YELLOW>BLUE>WHITE.
    * Blinking added, but not supported across platforms
    * Red shows tasks over-due





----
