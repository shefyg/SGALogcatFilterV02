import tkinter as tk

from BaseFilterConfig import BaseFilterConfig


class BaseFilterDispFrm(tk.Frame):
    def __init__(self, parent, filter_config: BaseFilterConfig, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.filter_config = filter_config
        # Filter Win Name Label
        self.filter_win_name_label = tk.Label(self, text=f"{self.filter_config.filter_win_name or 'None'}")
        self.filter_win_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # Filter Name Label
        self.filter_name_label = tk.Label(self, text=f"{self.filter_config.filter_name or 'None'}")
        self.filter_name_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        # Sub Filters Label
        self.sub_filters_label = tk.Label(self, text=f"{self.filter_config.sub_filters or 'None'}")
        self.sub_filters_label.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Selected Color Display
        self.selected_color_label = tk.Label(self, text=" ", bg=self.filter_config.selected_color or 'white')
        self.selected_color_label.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.selected_color_label.config(width=6, height=2)
