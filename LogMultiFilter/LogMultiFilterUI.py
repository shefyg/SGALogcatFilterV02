import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional

from FilterConfigWin import FilterConfigWin
from BaseFilterConfig import BaseFilterConfig
from BaseFilterDispFrm import BaseFilterDispFrm
from LogFilterInterfaces import IProcessedLineHandler
from MultiLogFilterConfig import MultiLogFilterConfig, LogRange, LogRangeType
from LogSpecificFilterTopUI import LogSpecificFilterTop
from NotificationsMngPack.NotifMng import NotifMng
from NotificationsMngPack.NotifMngClient import NotifMngClient
from SpecificFiltersUIMng import SpecificFiltersUIMng
from Utils import print_class_and_method, LMFNotifType, LMFNotifInfoKey
from LogMultiFilterProcessor import LogMultiFilterProcessor

DEFAULT_TEXT_WIDGET_WIDTH = 120


class LogMultiFilterUI(NotifMngClient, IProcessedLineHandler):
    in_process = False

    #region init and setup + ui setup ----------------------------
    def __init__(self, **kwargs):
        # Attributes that default to None
        default_attributes = [
            'file_path', 'process_log_button', 'ui_lines_range_frame',
            'end_line_entry', 'start_line_entry', 'open_log_button_test2',
            'main_log_txt_widget', 'ui_panel_frm', 'ui_bts_frame',
            'open_log_button', 'ui_bts_frame', 'filters_displays_frame'
        ]

        # Dynamically set default None attributes
        for attr in default_attributes:
            setattr(self, attr, None)

        # for communication
        # Retrieve processor from kwargs if it exists, otherwise set to None
        processor = kwargs.get('processor', None)

        # for communication, assign to self.log_processor
        self.log_processor: Optional[LogMultiFilterProcessor] = processor

        # create root window
        self.root = tk.Tk()
        self.root.title("LogCat Filtering Dashboard")
        self.root.geometry("1440x760")

        # tkinter vars
        self.start_line_tkstr = tk.StringVar()
        self.end_line_tkstr = tk.StringVar()

        # to handle filters Tops
        self.specific_filters_mng = SpecificFiltersUIMng(self.root)

        # collecting handlers
        self.handle_log_file = kwargs['handle_log_file']

        # setup ui elements
        self.setup_main_ui(**kwargs)

        # register for notifications.
        NotifMng.register_client(LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED, self)
        NotifMng.register_client(LMFNotifType.FILTER_CREATED_FROM_CONFIG, self)

    def setup_main_ui(self, **kwargs):
        # setup main log ui
        self.add_main_log_to_ui()

        # setup ui bts
        self.ui_panel_frm = tk.Frame(self.root, bg='orange')
        self.ui_panel_frm.pack(side=tk.RIGHT, padx=25, pady=25, fill=tk.BOTH, expand=True)

        self.add_log_start_end_line_inputs()
        self.add_ui_bts(**kwargs)
        self.add_multi_filter_config_ui()

    def add_main_log_to_ui(self):
        # Create a Text widget to display text
        self.main_log_txt_widget = tk.Text(self.root, width=DEFAULT_TEXT_WIDGET_WIDTH, bg="black", fg="white",
                                           insertbackground="white",  # Cursor color
                                           selectbackground="gray",  # Selected text background
                                           selectforeground="black")  # Selected text foreground
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
    def add_log_start_end_line_inputs(self):
        self.ui_lines_range_frame = tk.Frame(self.ui_panel_frm, bg='#ffffbb')
        self.ui_lines_range_frame.pack(side=tk.TOP, padx=25, pady=25, fill=tk.X)

        # Configure column 1 (the column where Entry widgets are located) to expand
        self.ui_lines_range_frame.grid_columnconfigure(1, weight=1)

        # Label and input for Start Line
        tk.Label(self.ui_lines_range_frame, text="Process Start Line:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.start_line_entry = tk.Entry(self.ui_lines_range_frame, textvariable=self.start_line_tkstr)
        self.start_line_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.start_line_entry.bind("<KeyRelease>", self.on_log_lines_process_range_input_change)

        # Label and input for End Line
        tk.Label(self.ui_lines_range_frame, text="Process End Line:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.end_line_entry = tk.Entry(self.ui_lines_range_frame, textvariable=self.end_line_tkstr)
        self.end_line_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.end_line_entry.bind("<KeyRelease>", self.on_log_lines_process_range_input_change)


    @print_class_and_method
    def add_ui_bts(self, **kwargs):
        # frame for bts
        self.ui_bts_frame = tk.Frame(self.ui_panel_frm, bg='white')
        self.ui_bts_frame.pack(side=tk.TOP, padx=25, pady=25, fill=tk.BOTH)

        # Open Log  bt
        self.open_log_button = tk.Button(self.ui_bts_frame, text="Open Log File",
                                         command=self.select_log_file_to_filter)
        self.open_log_button.pack(pady=5)

        # Process Log bt
        self.process_log_button = tk.Button(self.ui_bts_frame, text="Process Log File", command=self.process_log_file, bg="#FFA500")
        self.process_log_button.pack(pady=5)

        # Add Filter bt
        self.add_filter_bt = tk.Button(self.ui_bts_frame, text="Add Filter",
                                       command=self.open_add_filter_dialog)
        self.add_filter_bt.pack(pady=5)

        # Clear custom filters bt
        self.add_filter_bt = tk.Button(self.ui_bts_frame, text="Clear custom Filters",
                                       command=self.clear_custom_filters)
        self.add_filter_bt.pack(pady=5)

    def add_multi_filter_config_ui(self):
        # Create a frame to hold the UI elements
        self.ui_config_frame = tk.Frame(self.ui_panel_frm, bg='#d3d3d3')
        self.ui_config_frame.pack(side=tk.TOP, padx=25, pady=25, fill=tk.BOTH, expand=True)

        # Button to load the configuration
        self.load_config_button = tk.Button(self.ui_config_frame, text="Load Config", command=self.load_config)
        self.load_config_button.grid(row=0, column=0, columnspan=2, pady=10)

        # # Label and input for Config Name
        # tk.Label(self.ui_config_frame, text="Config Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        # self.config_name_entry = tk.Entry(self.ui_config_frame)
        # self.config_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Button to save the configuration
        self.save_config_button = tk.Button(self.ui_config_frame, text="Save Config", command=self.save_config)
        self.save_config_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Configure column 1 to expand to fill available space
        self.ui_config_frame.grid_columnconfigure(1, weight=1)
    #endrange

    #region ui actions and commands ---------------------------------------------
    def load_config(self):
        """Opens a file dialog to load a .multiLogConf file."""
        file_path = filedialog.askopenfilename(
            title="Select Configuration File",
            filetypes=[("Multi Log Config Files", "*.multiLogConf"), ("All Files", "*.*")]
        )

        if file_path:
            config = MultiLogFilterConfig.load_from_file(file_path)
            print(config)
            self.log_processor.setup_filters() # for defaults, override if exists
            self.log_processor.add_custom_filters(config.filters)
            # The range
            self.start_line_tkstr.set(config.log_range.range_start)
            self.end_line_tkstr.set(config.log_range.range_end)
            self.log_processor.log_start_process_line = config.log_range.range_start
            self.log_processor.log_stop_process_line = config.log_range.range_end

    def save_config(self):

        """Opens a Save As dialog and saves the config to the selected path."""
        # Open Save As dialog to get the file path where config will be saved
        file_path = filedialog.asksaveasfilename(
            defaultextension=".multiLogConf",
            filetypes=[("Multi Log Config Files", "*.multiLogConf"), ("All Files", "*.*")],
            title="Save Configuration File"
        )
        config_name = os.path.splitext(os.path.basename(file_path))[0]

        if not config_name.strip():
            print("Config name cannot be empty!")
            return

        # Save the configuration
        config = MultiLogFilterConfig(config_name=config_name)
        config.set_range(LogRange(range_start=self.log_processor.log_start_process_line,
                                  range_end=self.log_processor.log_stop_process_line))
        for log_filter in self.log_processor.filters.values():
            if not log_filter.is_default_filter:
                config.add_filter(log_filter=log_filter)
        config.save_to_file(file_path=file_path)


    def on_log_lines_process_range_input_change(self, event):
        """Handles updates whenever the user types in the Entry widgets."""
        start_line = self.start_line_entry.get()
        end_line = self.end_line_entry.get()
        self.log_processor.log_start_process_line = start_line
        self.log_processor.log_stop_process_line = end_line

    def process_log_file(self):
        self.clear_log()
        LogSpecificFilterTop.clear_all_logs(destroy_wins=False)
        self.handle_log_file(self.file_path)

    def open_add_filter_dialog(self):
        FilterConfigWin(self.root, self.set_filter, None)

    def clear_custom_filters(self):
        self.specific_filters_mng.clear_filters()
        for widget in self.filters_displays_frame.winfo_children():
            widget.destroy()
        LogSpecificFilterTop.clear_all_logs()

    def set_filter(self, filter_config: BaseFilterConfig, from_config=False):
        print(f"Filter Win Name: {filter_config.filter_win_name}")
        print(f"Filter Name: {filter_config.filter_name}")
        print(f"Sub Filters: {filter_config.sub_filters}")
        print(f"Selected Color: {filter_config.selected_color}")

        self.add_filter_frame_to_ui(filter_config)

        if not from_config:
            self.clear_log()
            NotifMng.notify(LMFNotifType.FILTER_CREATED, filter_config)

    # TODO: function to add frame for custom filter

    def add_filter_frame_to_ui(self, filter_config: BaseFilterConfig):
        # check if there is frame for filters
        if not self.filters_displays_frame:
            self.filters_displays_frame = tk.Frame(self.ui_panel_frm, bg='white')
            self.filters_displays_frame.pack(side=tk.TOP, padx=25, pady=25, fill=tk.BOTH)

        ffrm = BaseFilterDispFrm(self.filters_displays_frame, filter_config)
        ffrm.pack(pady=5)

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
        self.file_path = filedialog.askopenfilename(title="Open Log File (textual)",
                                                    filetypes=[("Log Files", "*.log"), ("All Files", "*.*")])
        # self.handle_log_file(file_path)

    def add_line(self, ind, line, filter_to_line_msgs, to_default=True):
        if to_default:
            self.add_line_to_main_log(ind, line)
        win_name_to_log_filters = {}

        for log_filter in filter_to_line_msgs:
            if log_filter.filter_win_name not in win_name_to_log_filters:
                win_name_to_log_filters[log_filter.filter_win_name] = set()
            win_name_to_log_filters[log_filter.filter_win_name].add(log_filter)

        for win_name, log_filters in win_name_to_log_filters.items():
            msg = f'{ind}-{list(log_filters)[0].sub_ind}: {line}'
            self.specific_filters_mng.add_line_with_filters(win_name, log_filters, msg)

            #
            # for msg in filter_to_line_msgs[log_filter]:
            #     self.specific_filters_mng.add_line(log_filter, msg)

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

    #region interfaces implementations   -------------------------------------------

    def handle_line_from_processor(self, ind, line, filter_to_line_msgs, to_default=True):
        self.add_line(ind, line, filter_to_line_msgs, to_default)

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
        elif notif_type == LMFNotifType.FILTER_CREATED_FROM_CONFIG:
            filter_config_info = notif_info[LMFNotifInfoKey.FILTER_CONFIG]
            fc = BaseFilterConfig(filter_config_info)

            self.set_filter(fc, from_config=True)

    #endregion
    def clear_log(self):
        # Clear all text from the text widget
        self.main_log_txt_widget.delete("1.0", tk.END)

        # Remove all tags from the text widget
        for tag in self.main_log_txt_widget.tag_names():
            self.main_log_txt_widget.tag_remove(tag, "1.0", tk.END)

    # endregion
