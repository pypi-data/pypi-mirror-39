import logging

from .click import ClickTask
from .link import LinkTask
from .input import InputTask
from .enter import EnterTask
from .shared_input import SharedInputTask
from .custom import CustomTask
from .._enums.supported_actions import SupportedActions


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TaskManager:
    def __init__(self, driver, task_config, shared_data):
        self.driver = driver
        self.task_config = task_config
        self.shared_data = shared_data
        self.tasks = self.__setup_tasks()
        self.shared_data = shared_data

    def __setup_tasks(self):
        tasks = list()
        for task in self.task_config:
            if task.action == SupportedActions.LINK.value:
                tasks.append(LinkTask(task, self.driver, self.shared_data))
            elif task.action == SupportedActions.INPUT.value:
                tasks.append(InputTask(task, self.driver, self.shared_data))
            elif task.action == SupportedActions.SHARED_INPUT.value:
                tasks.append(SharedInputTask(task, self.driver, self.shared_data))
            elif task.action == SupportedActions.ENTER.value:
                tasks.append(EnterTask(task, self.driver, self.shared_data))
            elif task.action == SupportedActions.CLICK.value:
                tasks.append(ClickTask(task, self.driver, self.shared_data))
            elif task.action == SupportedActions.CUSTOM.value:
                tasks.append(CustomTask(task, self.driver, self.shared_data))

        return tasks

    def execute_tasks(self):
        try:
            for task in self.tasks:
                task.execute()
        except Exception as e:
            logging.fatal("[FATAL] Exception", e.args)
        finally:
            self.driver.quit()
            self.driver.close()
            self.tasks.clear()
