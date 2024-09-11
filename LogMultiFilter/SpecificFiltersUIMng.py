import tkinter as tk

from BaseFilter import BaseFilter
from NotificationsMngPack.NotifMng import NotifMng
from Utils import LMFNotifType
from LogSpecificFilterTopUI import LogSpecificFilterTop
from NotificationsMngPack.NotifMngClient import NotifMngClient

TEXT_WIDGET_HEIGHT = 10


class SpecificFiltersUIMng(tk.Frame, NotifMngClient):

    def __init__(self, parent):
        super().__init__(parent)

        self.id_to_filter_top_window = {}


        # Create widgets and layout for your custom frame
        label = tk.Label(self, text="Filtered Logs")
        label.pack()

        self.all_text_widgets_frm = tk.Frame(self)
        self.all_text_widgets_frm.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        NotifMng.register_client(LMFNotifType.FILTER_CREATED, self)

    def reset_everything(self):
        for id, filter_top in self.id_to_filter_top_window.items():
            filter_top.destroy()

    def add_line(self, log_filter:BaseFilter, line):
        filtered_log_id = log_filter.filter_win_name
        if filtered_log_id not in self.id_to_filter_top_window:
            self.id_to_filter_top_window[filtered_log_id] = LogSpecificFilterTop(self, filtered_log_id, tag_configs=log_filter.tag_configs)

        self.id_to_filter_top_window[filtered_log_id].add_line(line, log_filter)

    def add_line_with_filters(self, win_name, log_filters, line):
        all_tag_configs = {}
        for log_filter in log_filters:
            all_tag_configs.update(log_filter.tag_configs)

        if win_name not in self.id_to_filter_top_window:
            self.id_to_filter_top_window[win_name] = LogSpecificFilterTop(self, win_name, tag_configs=all_tag_configs)
        self.id_to_filter_top_window[win_name].add_line_with_filters(line, log_filters)



    def HandleNotif(self, notif_type, notif_info) -> None:
        if(notif_type == LMFNotifType.FILTER_CREATED):
            for spec_filter_top in self.id_to_filter_top_window.values():
                spec_filter_top.clear_log()

    def clear_filters(self):
        NotifMng.notify(LMFNotifType.CLEAR_FILTERS, None)

