import threading
import tkinter as tk
from tkinter import filedialog

from FilterConfigWin import FilterConfigWin
from BaseFilterConfig import BaseFilterConfig
from BaseFilterDispFrm import BaseFilterDispFrm
from NotificationsMngPack.NotifMng import NotifMng
from NotificationsMngPack.NotifMngClient import NotifMngClient
from SpecificFiltersUIMng import SpecificFiltersUIMng
from Utils import print_class_and_method, LMFNotifType, LMFNotifInfoKey

DEFAULT_TEXT_WIDGET_WIDTH = 120


class LogMultiFilterUI(NotifMngClient):
    in_process = False

    def __init__(self, **kwargs):

        # create root window
        self.open_log_button_test2 = None
        self.main_log_txt_widget = None
        self.ui_panel_frm = None
        self.ui_bts_frame = None
        self.filters_disps_frame = None

        self.open_log_button = None
        self.root = tk.Tk()
        self.root.title("LogCat Filtering Dashboard")
        self.root.geometry("1440x760")

        # to handle filters Tops
        self.specific_filters_mng = SpecificFiltersUIMng(self.root)

        # collecting handlers
        self.handle_log_file = kwargs['handle_log_file']

        # setup ui elements
        self.setup_main_ui(**kwargs)

        NotifMng.register_client(LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED, self)

    def setup_main_ui(self, **kwargs):
        # setup main log ui
        self.add_main_log_to_ui()

        # setup ui bts
        self.ui_panel_frm = tk.Frame(self.root, bg='orange')
        self.ui_panel_frm.pack(side=tk.RIGHT, padx=25, pady=25, fill=tk.BOTH, expand=True)

        self.add_ui_bts(**kwargs)

    def add_main_log_to_ui(self):
        # Create a Text widget to display text
        self.main_log_txt_widget = tk.Text(self.root, width=DEFAULT_TEXT_WIDGET_WIDTH, bg="black", fg="white",
                                   insertbackground="white",  # Cursor color
                                   selectbackground="gray",   # Selected text background
                                   selectforeground="black")  # Selected text foreground)
        self.main_log_txt_widget.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Applying default log format
        self.main_log_txt_widget.tag_configure("DEBUG", foreground="orange")
        self.main_log_txt_widget.tag_configure("INFO", foreground="lightgreen")

        # Create a vertical scrollbar and associate it with the Text widget
        scrollbar = tk.Scrollbar(self.root, command=self.main_log_txt_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        self.main_log_txt_widget.config(yscrollcommand=scrollbar.set)

    @print_class_and_method
    def add_ui_bts(self, **kwargs):
        # frame for bts
        self.ui_bts_frame = tk.Frame(self.ui_panel_frm, bg='white')
        self.ui_bts_frame.pack(side=tk.TOP, padx=25, pady=25, fill=tk.BOTH)

        # Open Log  bt
        self.open_log_button = tk.Button(self.ui_bts_frame, text="Open Log File",
                                         command=self.select_log_file_to_filter)
        self.open_log_button.pack(pady=5)

        # Add Filter bt
        self.add_filter_bt =  tk.Button(self.ui_bts_frame, text="Add Filter",
                                         command=self.open_add_filter_dialog)
        self.add_filter_bt.pack(pady=5)

    def open_add_filter_dialog(self):
        FilterConfigWin(self.root, self.set_filter, None)

    def set_filter(self, filter_config:BaseFilterConfig):
        print(f"Filter Name: {filter_config.filter_name}")
        print(f"Sub Filters: {filter_config.sub_filters}")
        print(f"Selected Color: {filter_config.selected_color}")

        # check if ther is frame for filters
        if not self.filters_disps_frame:
            self.filters_disps_frame = tk.Frame(self.ui_panel_frm, bg='white')
            self.filters_disps_frame.pack(side=tk.TOP, padx=25, pady=25, fill=tk.BOTH)

        ffrm = BaseFilterDispFrm(self.filters_disps_frame, filter_config)
        ffrm.pack(pady=5)

        self.clear_log()
        NotifMng.notify(LMFNotifType.FILTER_CREATED, filter_config)



    @print_class_and_method
    def start_gui_and_filtering(self, activate_main_loop=True):
        LogMultiFilterUI.in_process = True

        # Create a thread for the GUI
        # self.filter_thread = threading.Thread(target=self.logcat_filter_func)
        # self.filter_thread.daemon = True
        # self.filter_thread.start()
        if activate_main_loop:
            self.root.mainloop()

    # region functionality for ui

    @print_class_and_method
    def select_log_file_to_filter(self):
        file_path = filedialog.askopenfilename(title="Open Log File (textual)",
                                               filetypes=[("Log Files", "*.log"), ("All Files", "*.*")])
        self.handle_log_file(file_path)

    def add_line(self, ind, line, filter_to_line_msgs, to_default=True):
        if to_default:
            self.add_line_to_main_log(ind, line)
        for log_filter in filter_to_line_msgs:
            print(f'\n\n ========= {log_filter.filter_name} ======\n')
            for msg in filter_to_line_msgs[log_filter]:
                print(f'       {msg}')
                self.specific_filters_mng.add_line(log_filter, msg)

    def add_line_to_main_log(self, ind, line):
        insert_position = self.main_log_txt_widget.index(tk.END)

        start_index = self.main_log_txt_widget.index("end-1c")

        line_content = f'{ind}: {line}\n'
        self.main_log_txt_widget.insert(tk.END, line_content)



        # handling DEBUG and INFO

        # parts = insert_position.split('.')
        # line_start = f'{parts[0]}.0'
        # line_end =  f'{parts[0]}.10'
        # print(f"Insert position: {insert_position}, Line start: {line_start}, Line end: {line_end}")

        # Apply DEBUG tag if "DEBUG" is in the line
        if "DEBUG" in line:
            sub_str = "DEBUG"
            start_pos = self.main_log_txt_widget.search(sub_str, start_index, "end-1c")
            while start_pos:
                end_pos = f"{start_pos} lineend"
                start_pos = f"{start_pos} linestart"
                self.main_log_txt_widget.tag_add(sub_str, start_pos, end_pos)
                start_pos = self.main_log_txt_widget.search(sub_str, end_pos, "end-1c")

            # self.main_log_txt_widget.tag_add("DEBUG", line_start, line_end)

        # Apply INFO tag if "INFO" is in the line
        if "INFO" in line:
            sub_str = "INFO"
            start_pos = self.main_log_txt_widget.search(sub_str, start_index, "end-1c")
            while start_pos:
                end_pos = f"{start_pos} lineend"
                start_pos = f"{start_pos} linestart"
                self.main_log_txt_widget.tag_add(sub_str, start_pos, end_pos)
                start_pos = self.main_log_txt_widget.search(sub_str, end_pos, "end-1c")

            # self.main_log_txt_widget.tag_add("INFO", line_start, line_end)

        # Scroll to the bottom
        self.main_log_txt_widget.see(tk.END)

    def HandleNotif(self, notif_type, notif_info) -> None:
        if notif_type == LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED:
            # finding the line with global ind and going to it
            global_line_index = notif_info[LMFNotifInfoKey.GLOBAL_LINE_IND]

            # Search for the line that starts with global_line_index
            line_start = self.main_log_txt_widget.search(f'^{global_line_index}', '1.0', tk.END, regexp=True)

            if line_start:
                # Scroll to the line
                self.main_log_txt_widget.see(line_start)
                # Optionally, you can also highlight the line or do other actions here

    def clear_log(self):
        # Clear all text from the text widget
        self.main_log_txt_widget.delete("1.0", tk.END)

        # Remove all tags from the text widget
        for tag in self.main_log_txt_widget.tag_names():
            self.main_log_txt_widget.tag_remove(tag, "1.0", tk.END)

    # endregion
