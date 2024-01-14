import tkinter as tk

from LogFilterTop import LogFilterTop

TEXT_WIDGET_HEIGHT = 10
LOG_ID_UPLOAD_STATE = 'App Upload State'
LOG_ID_PRE_PROCESS = 'PreProcess status'
LOG_ID_KEEP_TRACK = 'Keep track of Bg Upload'
LOG_ID_APP_CALL_PLUGIN = 'Calls to BgUpPlugin'
LOG_ID_BG_UPLOAD_SERVICE = 'From Bg Upload Service'

class MultiFilteredLogsTkFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # List to store the added text widgets
        #TODO: Remove these later as starting to use custom windows.
        # self.text_widgets_frms = []
        # self.id_to_text_widget = {}
        self.id_to_filter_top_window = {}


        # Create widgets and layout for your custom frame
        label = tk.Label(self, text="Filtered Logs")
        label.pack()

        self.all_text_widgets_frm = tk.Frame(self)
        self.all_text_widgets_frm.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    def reset_everything(self):
        for id, filter_top in self.id_to_filter_top_window.items():
            filter_top.destroy()


    def add_line(self, filtered_log_id, line):
        if filtered_log_id not in self.id_to_filter_top_window:
            self.id_to_filter_top_window[filtered_log_id] = LogFilterTop(self, filtered_log_id)

        self.id_to_filter_top_window[filtered_log_id].add_line(line)
