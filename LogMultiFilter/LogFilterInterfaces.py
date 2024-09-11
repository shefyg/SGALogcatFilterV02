from abc import ABC, abstractmethod


class IProcessedLineHandler(ABC):
    @abstractmethod
    def handle_line_from_processor(self, ind, line, filter_to_line_msgs, to_default=True):
        pass

