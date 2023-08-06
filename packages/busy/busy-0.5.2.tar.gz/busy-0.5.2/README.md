# Busy

A command-line task and plan management tool.

To install:

```
pip3 install busy
```

## Introduction

Busy is a system for keeping track of tasks. Some of the guiding philosophies:

- There are "active" tasks, which is an ordered list of things to work on (also called "todos"), and there are "plans", which are things that have been deferred to a specific future date
- The "current" task is the top of the "active" task list, so it's the thing to do right now
- Everything is based on a POSIX command line interface, making it easy to use from the terminal prompt on Linux and MacOS systems
- Data is stored in easily edited files, so if the tool doesn't do something you want, you can just edit the files

## Commands

The main command is `busy`.

Otherwise, the first positional argument is a command, which is one of the following.

| **Command** | **Description** |                                    **Designate tasks?** | **Default** |
| --- | ---  | --- | --- |
| `get`       | Get the current task, no options                                  | -   | Current task       |
| `list`      | List active tasks (or plans, with an option) in order, with sequence numbers | YES | All active tasks |
| `add`       | Add a new active task                                                | -   | - |
| `drop`      | Drop a task to the bottom of the active order                       | YES | Current task |
| `pop`       | Pop a task or tasks to the top of the active order                   | YES | The last task on the active list |
| `delete`    | Delete a task                        | YES | Current task |
| `defer`     | Convert an active task into a plan for a specific later date       | YES | Current task |
| `activate`  | Make a plan or plans active, include a 'today' option           | YES - plans | - |
| `start`     | Starts work on a particular project (see below)                 | -   | - |
| `manage`    | Edit tasks in an editor                                           | YES | All active tasks |

### Task tags

Tasks can have tags, which are designated with space-separated hashtags in the task description, for example:

```
go to the supermarket #errands
```

Tags can be used in task designation, for example:

```
busy pop errands
```

A task can have no tags, one tag, or more than one tag.

## Editing the tasks directly with the `manage` command

The `manage` command launches the user's default text editor to directly edit tasks. Note that it only works with active tasks (not plans) and that once the tasks are edited they will be dropped to the bottom of the list.

Busy uses the `sensible-editor` command to select a text editor, which works with default Ubuntu Linux installations and might or might not work with other operating systems.

## Designating tasks

For some commands, it's possible to designate tasks to be acted upon. Designating tasks is always optional.

Tasks are identified by number, which is the line number of that task within the list of tasks. It's easy to see the numbers of tasks using the `list` command. Note that the numbering starts with 1, and is not an ID -- the number of a task will change as the active task list is reordered. So always reference the most recent list.

`busy list` lists all the tasks

`busy list 5` shows only task number 5

`busy list 3-7` shows tasks 3-7

`busy list 3-` show tasks 3 through the end

`busy list 3 5 7 9` shows the tasks designated

`busy list -` shows the last task

`busy list -4` is an error! Use `busy list 1-4` instead.

`busy list admin` list all the tasks with the `#admin` hashtag somewhere in their description.

Task designation criteria are additive -- that is, a logical OR. So:

`busy list admin sales 3 4` will list all the admin tasks, sales tasks, and tasks 3 and 4.

Note the result is always in the order the tasks appear in the queue, regardless of the order the criteria are provided.

## Command line options

| **Option** | **Description** |
| --- | ---|
| `--root`  | Defines the root for only this command |
| `--plan`  | Include tasks that are scheduled for a future date (only for `list`) |
| `--task`  | Provide the task description (only for `add`) |
| `--yes`   | Don't require confirmation of deletions |
| `--today` | Activate tasks for today or earlier (only for `activate`) |

## Deferral

Deferral is about scheduling a task to reappear on the task list on a future date. To defer a task, you have to designate the date using the `--to` or `--for` option (they are interchangable). Some options:

- `1 day` or `1d` Tomorrow (the default) - can also write `tomorrow`
- `2 days` or `2d` The day after tomorrow
- `2018-10-28` A specific date in `YYYY-MM-DD` format

Example:

```
busy defer 4-6 --for 4 days
```

## Piping to the `add` command

Task descriptions always come from stdin. To read from a file, try:

```
cat list-of-tasks.txt | busy add --multiple
```

## Projects and the `start` command

If a task has tags, the first tag is considered to be its "project" for the purposes of the `start` command.

The `start` command is used to start work on a project. If an argument is passed to the command, that's the chosen project. Otherwise the chosen project is the project of the current task. The command basically combines steps:

- Calls `activate --today` so the active task list is up-to-date
- Calls `manage` on the project, to edit the list of tasks for the project
- Calls `pop` on the project, so its tasks are at the top of the list

## Data storage

Tiger requires a "root", which is the directory containing the two data files:

- `todo.txt` - active tasks
- `plan.txt` - future tasks, with dates

Technically, they are pipe-delimited data files, though `todo.txt` only has one field.

How to tell busy its root (in order)

- The `--root` option
- The `BUSY_ROOT` environment variable
- Otherwise, `~/.busy` which will be generated as needed

The "root" setup allows you to have separate task queues for separate projects.

## Development

Although it requires Python 3.6.5 or higher, Busy is designed to function with the Python standard library without any additional pip modules.

However, we use coverage during unit testing, so:

```
pip3 install coverage
```

Then to run the test suite:

```
make test
```

Or to run test coverage:

```
make cover
```
