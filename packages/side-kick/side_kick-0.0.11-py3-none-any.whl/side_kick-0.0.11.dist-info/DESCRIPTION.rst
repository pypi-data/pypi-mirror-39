
Side Kick
-

Side Kick is a simple, lightweight scheduler for Django management commands. Assign a task to run by adding the 
`@sidekick` decorator. Anything can be a management command, whether it is doing database back ups or sending emails. 
Simply create the task, add the decorator and then in Django's admin you can set when it should run and also enable or 
disable it. It will also make sure that the task will only run if there is no other instance of the task already running
to avoid unexpected issues if a task takes longer to complete than expected.


Side Kick requires an app to be created within the project, this will allow you to schedule tasks using
the admin page.

Installation

    pip install side-kick

Make sure you add `sidekick` to your installed apps.

Then in your project create a new app called sidekick_tasks:

`./manage.py startapp sidekick_tasks`

Then add `sidekick_tasks` to your installed apps.

In the newly created models.py file, add the following:

```
from django.db import models


class Task(models.Model):
    """Task model used to define tasks that will be run as cron jobs """

    name = models.CharField(max_length=255, help_text='The human readable name of the task')
    registered_task = models.ForeignKey('sidekick_tasks.RegisteredTask', on_delete=models.CASCADE)
    cron_schedule = models.ForeignKey('sidekick_tasks.CronSchedule', on_delete=models.DO_NOTHING)
    enabled = models.BooleanField(default=False, help_text='Whether the task is enabled')

    def __str__(self):
        return self.name

    def task_of(self):
        """The app which this task belongs to """
        return self.registered_task.task_name.split(' ')[0]


class CronSchedule(models.Model):
    """Cron Schedule model for defining different time intervals """

    name = models.CharField(max_length=100, help_text='Human readable version of schedule, i.e Every 10 minutes')
    minute = models.CharField(max_length=100, help_text='At what minute. * for every', default='*')
    hour = models.CharField(max_length=100, help_text='At what hour. * for every', default='*')
    day_of_week = models.CharField(max_length=100, help_text='At what day of the week. * for every', default='*')
    day_of_month = models.CharField(max_length=100, help_text='At what day of the month. * for every', default='*')
    month_of_year = models.CharField(max_length=100, help_text='At what month of the year. * for every', default='*')

    def __str__(self):
        return self.name

    def schedule(self):
        return "{} {} {} {} {}".format(self.minute, self.hour, self.day_of_month, self.month_of_year, self.day_of_week)


class RegisteredTask(models.Model):
    """Model for the registered task to be used by the Task Model """

    task_name = models.CharField(max_length=125, help_text='The task to be run ie. stock --get_stock_updates')

    def __str__(self):
        return self.task_name.replace('--', ' - ').replace('_', ' ')


```

Then create the migrations.

Create a file in sidekick_tasks app called `tasks.txt`.

Then create a new file within the sidekick_tasks app, called settings.py. This is where you will define a few key details.

`SIDEKICK_REGISTERED_APPS` is where you will need to define all the apps which have tasks that sidekick will handle.
You just need to put the app name and then as soon as django loads it will import the tasks.py file of each app in
this list and any tasks that have the `@sidekick_task` decorator will create a new RegisteredTask instance if it does 
not already exist.

Each time you want to register a new task, don't forget to add it to this list.
```
SIDEKICK_REGISTERED_APPS = [
    'stock',
    'customers',
    'pizzas',
]
```

`ENVIRONMENT` is where you will define the user and the start-up file of that user for example:
```
ENVIRONMENT = "root . /root/.profile"
```

`DJANGO_PATH` is the path to your project directory and then the path to python, followed by the manage.py command
which will be used to trigger the tasks. For example:
```
DJANGO_PATH = "/var/www/myproject && /var/www/virtualenv/bin/python manage.py"
```

`CRON_PATH` is the path to the tasks.txt file that you created earlier. This is where the cron files will be written, 
so you can check within this directory once you have registered a task that it is working correctly.
```
CRON_PATH = "/var/www/myproject/sidekick_tasks/tasks.txt"
```
`LOCK_FILE` is the path to the directory where the lock files will be created when a task starts running and deleted 
from when it is completed. The reason for this is to stop the same task running concurrently if the first instance of 
the task hasn't completed.

```
LOCK_PATH = "/var/www/myproject/sidekick_tasks/lock_files/"
```

These settings were designed so you can customise them and use different paths depending on the environment you are
working in.

In apps.py add the following:

```
from django.apps import AppConfig


class SidekickTasksConfig(AppConfig):
    name = 'sidekick_tasks'
    verbose_name = "Side Kick Tasks"
```

and then in the `__init__.py` file add:

``
default_app_config = 'sidekick_tasks.apps.SidekickTasksConfig'
``

In admin.py add:


    from django.contrib import admin
    from sidekick_tasks.models import Task, CronSchedule


    class CronScheduleAdmin(admin.ModelAdmin):
        """
        Admin for the CronSchedule
        """
        model = CronSchedule
        fields = (
            'name',
            'minute',
            'hour',
            'day_of_week',
            'day_of_month',
            'month_of_year'
        )


    admin.site.register(CronSchedule, CronScheduleAdmin)


    class TaskAdmin(admin.ModelAdmin):
        """
        Admin for the task model
        """
        list_display = ['name', 'registered_task', 'cron_schedule', 'enabled']


    admin.site.register(Task, TaskAdmin)

The basic set up is now complete.

When it comes to creating and registering tasks, follow these simple steps:

Add the `sidekick_task` decorator to any tasks you wish to register, make sure the task is in your tasks.py file of your 
app:

```
from sidekick.decorators import sidekick_task

@sidekick_task
def my_task():    
    # Whatever task you wish to complete
    ...

```

Then add the name of the app to the `SIDEKICK_REGISTERED_APPS` list in `sidekick_tasks.settings.py`

Create a new directory within your app called `management` and then a subdirectory called `commands`. Add a 
`__init__.py` file and a file with the name of the app eg. `customers.py` to the `commands` directory.

File structure would be as follows:

```
myproject
|_ customers 
   |_management
     |_commands
        |_ __init__.py
        |_ customers.py
```

Within `customers.py` (or whatever your app is) add the following:

```
import logging

from django.core.management.base import BaseCommand
from sidekick.services.helpers import get_task_name
from sidekick.services.crontab import CronTask

from sidekick_tasks.models import RegisteredTask

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Commands for the Customers app"

    def add_arguments(self, parser):
        """Defines the arguments """

        for task in RegisteredTask.objects.filter(task_name__startswith='customers'):
            task_name = task.task_name.split(' ')[1]
            parser.add_argument(
                task_name,
                action='store_true',
                dest=task_name[2:]
            )

    def handle(self, *args, **options):
        """Handle customer management commands.

        :param args:
        :param options: Arguments passed with command e.g. send_emails_to_customers
        """
        task_name = get_task_name(options)

        try:
            CronTask(task_name=task_name, app='customers').run()
        except Exception as e:
            logger.error(msg=e)

```

Within this file, the only parts you will need to edit are in the arguments of RegisteredTask filter and also
CronTask initialisation, change these over to be the name of your app. You will need to have this same file structure 
in each app you want to have tasks registered to so make sure you change the name in the arguments to match the app it 
is in.

Once this is done, you need to create a file within the `/etc/cron.d` directory called anything you like, I would 
suggest something like `sidekick_tasks`, and then create a sym link between this file and the tasks.txt file you 
created within the sidekick_tasks app.

You can do this by connecting to your server and then:

    cd /etc/cron.d
    touch sidekick_tasks
    ln -sf sidekick_tasks /var/www/myproject/sidekick_tasks/tasks.txt

Once this done then you're all good to go, you can now simply register tasks with a simple decorator and easily manage 
them using django admin.



