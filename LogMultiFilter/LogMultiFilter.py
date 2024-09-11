from Utils import LMFNotifType
from LogMultiFilterProcessor import LogMultiFilterProcessor
from LogMultiFilterUI import LogMultiFilterUI
from NotificationsMngPack.NotifMng import NotifMng
from NotificationsMngPack.NotifMngClient import NotifMngClient


class LogMultiFilter:

    def __init__(self):

        self.processor = LogMultiFilterProcessor()
        self.ui = LogMultiFilterUI(handle_log_file=self.processor.process_log_file, processor=self.processor)

        self.processor.register_processed_line_client(self.ui)

        self.ui.start_gui_and_filtering()






