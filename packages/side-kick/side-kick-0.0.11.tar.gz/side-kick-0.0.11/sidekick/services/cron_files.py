import logging

from sidekick_tasks.models import Task
from sidekick_tasks.settings import SIDEKICK_REGISTERED_APPS, ENVIRONMENT, DJANGO_PATH, CRON_PATH

logger = logging.getLogger(__name__)


class CronService:
    """Service to create or re-write the cron files """

    def __init__(self):
        self.environment = ENVIRONMENT
        self.joiner = "&& cd"
        self.django_path = DJANGO_PATH

    def write_cron_file(self, tasks):
        """For each task in list, write to the cron file. """

        with open(CRON_PATH, 'w+') as ws_cron_file:
            for task in tasks:
                ws_cron_file.write(
                    "# {name}\n"
                    "{schedule} {environment} {joiner} {django_path} {task}\n\n".format(
                        name=task.name,
                        environment=self.environment,
                        joiner=self.joiner,
                        django_path=self.django_path,
                        schedule=task.cron_schedule.schedule(),
                        task=task.registered_task.task_name)
                )

    def generate_cron_tasks(self):
        """Create a new cron file on the post save of a Registered Task"""
        try:
            tasks = Task.objects.filter(enabled=True)
            self.write_cron_file(tasks=tasks)
            logger.info(msg='Cron tasks successfully created.')
        except Exception as e:
            logger.error(msg='Failed to write cron tasks due to {}'.format(e))
