from django.apps import AppConfig


class SidekickConfig(AppConfig):
    name = 'sidekick'

    def ready(self):
        import sidekick.signals.post_save

        self.register_tasks()

    @staticmethod
    def register_tasks():
        """
        For each app listed in sidekick_tasks.settings SIDEKICK_REGISTERED_APPS import the task to trigger the decorator
        :return:
        """
        import importlib
        from sidekick_tasks.settings import SIDEKICK_REGISTERED_APPS

        for app in SIDEKICK_REGISTERED_APPS:
            app_task = app + '.tasks'
            importlib.import_module("%s" % app_task)
