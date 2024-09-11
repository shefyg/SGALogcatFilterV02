import tkinter as tk
from tkinter import colorchooser
from typing import Optional

from BaseFilterConfig import BaseFilterConfig


class FilterConfigWin(tk.Toplevel):
    def __init__(self, parent, set_filter_callback, filter_config: Optional[BaseFilterConfig], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.set_filter_callback = set_filter_callback

        # Set up the window
        self.title("Filter Configuration")
        self.geometry("300x200")

        # Keep the window on top
        self.attributes('-topmost', True)

        # Filter Win Name Label and Entry
        self.filter_win_name_label = tk.Label(self, text="Filter Win Name:")
        self.filter_win_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.filter_win_name_entry = tk.Entry(self)
        self.filter_win_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Filter Name Label and Entry
        self.filter_name_label = tk.Label(self, text="Filter Name:")
        self.filter_name_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.filter_name_entry = tk.Entry(self)
        self.filter_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        # Set value if exists in filter_config
        if filter_config:
            self.filter_name_entry.insert(0, filter_config.filter_name)
            self.filter_win_name_entry.insert(0, filter_config.filter_win_name)


        # Sub Filters Label and Entry
        self.sub_filters_label = tk.Label(self, text="Sub Filters:")
        self.sub_filters_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.sub_filters_entry = tk.Entry(self)
        self.sub_filters_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        if filter_config:
            self.sub_filters_entry.insert(0, filter_config.sub_filters)

        # Color selection
        self.color_button = tk.Button(self, text="Choose Color", command=self.choose_color)
        self.color_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.selected_color_label = tk.Label(self, text="Selected Color: None")
        self.selected_color_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        if filter_config:
            self.selected_color_label.config(text=f"Selected Color: {filter_config.selected_color}")
            self.selected_color_label.config(bg=filter_config.selected_color)

        # Save Button
        self.save_button = tk.Button(self, text="Save", command=self.save_and_close)
        self.save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[1]:  # If the user selected a color
            self.selected_color_label.config(text=f"Selected Color: {color_code[1]}", bg=color_code[1])

    def save_and_close(self):
        # Collect the current values
        filter_win_name = self.filter_win_name_entry.get()
        filter_name = self.filter_name_entry.get()
        sub_filters = self.sub_filters_entry.get()
        selected_color = self.selected_color_label.cget("text").replace("Selected Color: ", "")

        # Call the callback function with these values
        bfc = BaseFilterConfig()

        bfc.filter_name = filter_name
        bfc.sub_filters = sub_filters
        bfc.selected_color = selected_color
        bfc.filter_win_name = filter_win_name

        self.set_filter_callback(bfc)

        # Close the frame by destroying the parent window
        self.destroy()

