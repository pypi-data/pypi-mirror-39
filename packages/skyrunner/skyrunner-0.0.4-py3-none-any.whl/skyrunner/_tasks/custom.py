from abc import abstractmethod
import importlib.machinery as imm

from .base import Task
from .._enums.supported_script_lang import SupportedScriptLang


class CustomTask(Task):
    def __init__(self, task, driver, shared_data):
        super().__init__(task, driver, shared_data)
        self.type = task.params.type
        self.script_file = task.params.script_file
        self.class_name = task.params.class_name

    @abstractmethod
    def run(self):
        if self.type == SupportedScriptLang.PYTHON.value:
            datam = imm.SourceFileLoader(self.class_name, self.script_file).load_module()
            cls = getattr(datam, self.class_name)
            custom = cls(self.driver, self.shared_data)
            custom.run()
