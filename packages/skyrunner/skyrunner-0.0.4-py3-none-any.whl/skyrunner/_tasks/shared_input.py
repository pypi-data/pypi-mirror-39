from abc import abstractmethod

from .base import Task
from .._enums.supported_selector_type import SupportedSelectorType

class SharedInputTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.selector_type = task.params.type
        self.path = task.params.path
        self.data = task.params.data

    @abstractmethod
    def run(self):
        if self.selector_type == SupportedSelectorType.XPATH.value:
            self.driver.find_element_by_xpath(self.path).send_keys(self.get_shared_data(self.data))
        elif self.selector_type == SupportedSelectorType.ID.value:
            self.driver.find_element_by_id(self.path).send_keys(self.get_shared_data(self.data))
