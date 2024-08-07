from Utils import LMFNotifType
from LogMultiFilterProcessor import LogMultiFilterProcessor
from LogMultiFilterUI import LogMultiFilterUI
from NotificationsMngPack.NotifMng import NotifMng
from NotificationsMngPack.NotifMngClient import NotifMngClient


class LogMultiFilter(NotifMngClient):

    def __init__(self):

        self.processor = LogMultiFilterProcessor(self.handle_processed_line)
        self.ui = LogMultiFilterUI(handle_log_file=self.processor.process_log_file)
        self.ui.start_gui_and_filtering()
        NotifMng.register_client(LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED, self)

    def handle_processed_line(self, ind, line, filter_to_line_msgs, to_default=True):
        self.ui.add_line(ind, line, filter_to_line_msgs, to_default)

    def HandleNotif(self, notif_type, notif_info) -> None:
        if(notif_type == LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED):
            pass #TBD - handle if needed



