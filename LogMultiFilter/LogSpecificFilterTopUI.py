import tkinter as tk
import traceback
from tkinter import Toplevel

from BaseFilter import BaseFilter
from NotificationsMngPack.NotifMng import NotifMng
from NotificationsMngPack.NotifMngClient import NotifMngClient
from Utils import TagRangeConf, LMFNotifType, LMFNotifInfoKey
from SGAUtils2024.SGAUtils import SGAUtils

TEXT_WIDGET_HEIGHT = 75


class LogSpecificFilterTop(Toplevel, NotifMngClient):
    filters_top_count = 0
    log_specific_filter_tops = []

    def __init__(self, parent, id="Log Filter", tag_configs=None):
        super().__init__(parent)

        self.tag_configs = tag_configs

        LogSpecificFilterTop.log_specific_filter_tops.append(self)
        self.title_str = id
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

        # register for notification
        NotifMng.register_client(LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED, self)

    def update_tag_configs(self, tag_configs):
        need_tags_reconfigure = False
        for k,v in tag_configs.items():
            if k not in self.tag_configs or self.tag_configs[k] != v:
                self.tag_configs[k] = v
                need_tags_reconfigure = True
        if tag_configs and need_tags_reconfigure:
            for tag_name, tag_settings in tag_configs.items():
                self.text_widget.tag_configure(tag_name, **tag_settings)

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

    def add_line_with_filters(self, line, log_filters:[BaseFilter]):
        # Append the new line and the custom line passed as an argument
        appended_content = line + "\n"  # Include a newline to separate lines

        # Insert the updated content at the end
        start_index = self.text_widget.index("end-1c")  # Record the start index
        self.text_widget.insert("end-1c", appended_content)

        for log_filter in log_filters:

            # applying format (tags)
            for sub_filter, sub_filter_tags in log_filter.sub_filter_to_tags.items():
                start_pos = self.text_widget.search(sub_filter, start_index, "end-1c")
                range_conf = log_filter.sub_filter_to_range_conf.get("all", log_filter.sub_filter_to_range_conf.get(sub_filter, None))

                while start_pos:
                    end_pos = f"{start_pos}+{len(sub_filter)}c"

                    # # handling range of format
                    # if TagRangeConf.SUB_FILTER_TO_END in range_conf:
                    #     end_pos = f"{start_pos} lineend"

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

    #region handle log utils -----------------------
    def clear_log(self):
        if not self.text_widget or not self.text_widget.winfo_exists():
            return
        try:
            # Clear all text from the text widget
            self.text_widget.delete("1.0", tk.END)

            # Remove all tags from the text widget
            for tag in self.text_widget.tag_names():
                self.text_widget.tag_remove(tag, "1.0", tk.END)
        except Exception as e:
            print(f'Exception occurred: {e} for {self.title_str}')
            print("Call stack:\n%s", ''.join(traceback.format_exc()))


    @staticmethod
    def clear_all_logs(destroy_wins=True):
        for log_top in LogSpecificFilterTop.log_specific_filter_tops:
            log_top.clear_log()
            if destroy_wins:
                log_top.destroy()

    def find_closest_line(self, target_number):
        target_number = int(target_number)
        closest_line_index = None
        closest_difference = float('inf')  # Initialize with a large number

        # Start from the beginning of the text widget
        current_line = 1.0  # Tkinter uses '1.0' for the start position (line 1, column 0)

        while True:
            # Get the current line
            line_text = self.text_widget.get(f'{current_line} linestart', f'{current_line} lineend')

            # Check if we reached the end of the text widget (tk.END means the end of the widget)
            if current_line >= float(self.text_widget.index(tk.END)):
                break  # Break if we have reached the last line

            # Skip empty lines (no characters)
            if not line_text.strip():
                current_line += 1.0
                continue

            # Try to extract the number at the start of the line
            try:
                line_number = int(line_text.split('-')[0])  # Assumes each line starts with a number
            except (ValueError, IndexError):
                # If there's no number at the start of the line or the line is empty, skip it
                current_line += 1.0
                continue

            # Calculate the difference between the current line number and the target number
            difference = abs(line_number - target_number)

            # If this is the closest number so far, store it
            if difference < closest_difference:
                closest_difference = difference
                closest_line_index = current_line

            # Move to the next line
            current_line += 1.0

        # If a closest line was found, return the position of that line
        if closest_line_index is not None:
            return f'{int(closest_line_index)}.0'  # Return the position in the text widget

        return None  # Return None if no matching line was found

    #endregion

    #region handle notifications -----------------------
    def HandleNotif(self, notif_type, notif_info) -> None:
        if notif_type == LMFNotifType.SPECIFIC_FILTER_LINE_PRESSED:
            line_start = self.find_closest_line(notif_info[LMFNotifInfoKey.GLOBAL_LINE_IND])

            if line_start:
                # Scroll to the line
                self.text_widget.see(line_start)


    #endregion
