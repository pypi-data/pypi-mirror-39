import json

from ._tasks.task_manager import TaskManager
from ._driver import Driver
from ._direction import Direction


def execute(config_file_path, task_shared_data):
    config = __config_file_parse(config_file_path)
    driver = Driver(config.driver)
    manager = TaskManager(driver.driver, config.tasks, task_shared_data)
    manager.execute_tasks()


def __config_file_parse(config_file_path):
    with open(config_file_path, 'r', encoding='utf-8_sig') as file:
        return json.load(file, object_hook=hook)


def hook(dct):
    return Direction(**dct)

