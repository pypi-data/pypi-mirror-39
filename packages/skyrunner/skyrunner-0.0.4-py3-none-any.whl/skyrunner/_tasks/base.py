import logging
from time import sleep

logger = logging.getLogger(__name__)


class Task:
    def __init__(self, task, driver, shared_data):
        self.driver = driver
        self.shared_data = shared_data
        self.description = task.description
        self.action = task.action
        self.before_sleep = int(task.before_sleep) if hasattr(task, 'before_sleep') else 1
        self.after_sleep = int(task.after_sleep) if hasattr(task, 'after_sleep') else 1
        self.before_implicitly_wait = int(task.before_implicitly_wait) if hasattr(task, 'before_implicitly_wait') else 0
        self.after_implicitly_wait = int(task.after_implicitly_wait) if hasattr(task, 'after_implicitly_wait') else 0

    def execute(self):
        self.before_execute()
        self.run()
        self.after_execute()

    def before_execute(self):
        logger.info("[>>>> Start task] {}".format(self.description))
        sleep(self.before_sleep)
        self.driver.implicitly_wait(self.before_implicitly_wait)

    def run(self):
        pass

    def after_execute(self):
        logger.info("[<<<< End task] {}".format(self.description))
        sleep(self.after_sleep)
        self.driver.implicitly_wait(self.after_implicitly_wait)

    def set_shared_data(self, key, value):
        self.shared_data.attributes[key] = value

    def get_shared_data(self, key):
        return self.shared_data.attributes[key]


