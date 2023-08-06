from abc import ABCMeta, abstractmethod
from .base import Task


class LinkTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.url = task.params.url

    @abstractmethod
    def run(self):
        self.driver.get(self.url)
