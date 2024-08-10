from abc import ABC, abstractmethod


class InstanceExporterInterface(ABC):
    @abstractmethod
    def export_instance(self, instances):
        pass
