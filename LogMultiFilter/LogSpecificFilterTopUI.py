import tkinter as tk
from tkinter import Toplevel

from BaseFilter import BaseFilter
from NotificationsMngPack.NotifMng import NotifMng
from Utils import TagRangeConf, LMFNotifType, LMFNotifInfoKey
from SGAUtils2024.SGAUtils import SGAUtils

TEXT_WIDGET_HEIGHT = 75


class LogSpecificFilterTop(Toplevel):
    filters_top_count = 0
    log_specific_filter_tops = []

    def __init__(self, parent, id="Log Filter", tag_configs=None):
        super().__init__(parent)

        LogSpecificFilterTop.log_specific_filter_tops.append(self)
        self.title(id)

        self.text_widget = None

        self.instance_id = LogSpecificFilterTop.filters_top_count
        LogSpecificFilterTop.filters_top_count += 1
        x_pos = (self.instance_id%4) * 640

        # Get screen width
        screen_width = self.winfo_screenwidth()

        # Ensure the x position is within the screen width
        if x_pos + 640 > screen_width:
            x_pos %= screen_width # Adjust x_pos to fit within screen

        self.title(id)
        self.geometry(f"640x1280+{x_pos}+0")
        self.bg_color = SGAUtils.bg_color_from_string(id)
        self.configure(bg=self.bg_color)
        self.add_text_widget(id, tag_configs)

    def get_pressed_line(self, event):
        # Get the index of the mouse click
        index = self.text_widget.index(f"@{event.x},{event.y}")
        # Extract the line number from the index
        line_number = index.split(".")[0]
        # Get the text of the entire line
        line_text = self.text_widget.get(f"{line_number}.0", f"{line_number}.end")
        print(f"Clicked line: {line_number}, Text: {line_text}")
        global_line_ind = line_text.split('-')[0]
        NotifMng.notify(LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED, {LMFNotifInfoKey.GLOBAL_LINE_IND: global_line_ind})

    def add_text_widget(self, id, tag_configs):
        # Create a new frame for the text widget and scrollbar
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH)

        label = tk.Label(self.text_frame, text=f"{id}")
        label.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        # Create a new text widget
        self.text_widget = tk.Text(self.text_frame, height=TEXT_WIDGET_HEIGHT, width=20, bg="black", fg="white",
                                   insertbackground="white",  # Cursor color
                                   selectbackground="gray",   # Selected text background
                                   selectforeground="black")  # Selected text foreground)
        # Bind the click event to the get_line function
        self.text_widget.bind("<Button-1>", self.get_pressed_line)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # apply tags for format by filter
        if tag_configs:
            for tag_name, tag_settings in tag_configs.items():
                self.text_widget.tag_configure(tag_name, **tag_settings)

        # Create a vertical scrollbar for the text widget
        scrollbar = tk.Scrollbar(self.text_frame, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the text widget to use the scrollbar
        self.text_widget.config(yscrollcommand=scrollbar.set)

    def add_line(self, line, log_filter: BaseFilter):

        # Append the new line and the custom line passed as an argument
        appended_content = line + "\n"  # Include a newline to separate lines

        # Insert the updated content at the end
        start_index = self.text_widget.index("end-1c")  # Record the start index
        self.text_widget.insert("end-1c", appended_content)

        # applying format (tags)
        for sub_filter, sub_filter_tags in log_filter.sub_filter_to_tags.items():
            start_pos = self.text_widget.search(sub_filter, start_index, "end-1c")
            range_conf = log_filter.sub_filter_to_range_conf.get("all", log_filter.sub_filter_to_range_conf.get(sub_filter, None))

            while start_pos:
                end_pos = f"{start_pos}+{len(sub_filter)}c"

                # handling range of format
                if TagRangeConf.SUB_FILTER_TO_END in range_conf:
                    end_pos = f"{start_pos} lineend"

                for sub_filter_tag in sub_filter_tags:
                    self.text_widget.tag_add(sub_filter_tag, start_pos, end_pos)
                start_pos = self.text_widget.search(sub_filter, end_pos, "end-1c")

            start_pos = self.text_widget.search(sub_filter, start_index, "end-1c")
            if start_pos and TagRangeConf.TAG_MARK_INDEXES in range_conf:
                start_ind_pos = start_index
                colon_index = line.find(":")
                end_ind_pos = f"{start_pos.split('.')[0]}.{colon_index}"
                self.text_widget.tag_add("indexes_filter_tag", start_ind_pos, end_ind_pos)

        # Scroll to the bottom
        self.text_widget.see("end")

    def clear_log(self):
        # Clear all text from the text widget
        self.text_widget.delete("1.0", tk.END)

        # Remove all tags from the text widget
        for tag in self.text_widget.tag_names():
            self.text_widget.tag_remove(tag, "1.0", tk.END)

    @staticmethod
    def clear_all_logs():
        for log_top in LogSpecificFilterTop.log_specific_filter_tops:
            log_top.clear_log()
            log_top.destroy()

