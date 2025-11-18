import tkinter as tk

from BaseFilterConfig import BaseFilterConfig


class BaseFilterDispFrm(tk.Frame):
    def __init__(self, parent, filter_config: BaseFilterConfig, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.filter_config = filter_config
        
        # Configure frame styling with border and background
        self.config(relief='raised', borderwidth=2, bg='#f0f0f0')
        
        # Configure column to expand for full width
        self.grid_columnconfigure(0, weight=1)
        
        row = 0
        
        # Filter Group Label and Value
        filter_group_label = tk.Label(self, text="Filter Group:", anchor='w', bg='#f0f0f0')
        filter_group_label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='ew')
        row += 1
        
        self.filter_win_name_label = tk.Label(self, text=f"{self.filter_config.filter_win_name or 'None'}", 
                                               anchor='w', bg='#f0f0f0')
        self.filter_win_name_label.grid(row=row, column=0, padx=5, pady=(0, 5), sticky='ew')
        row += 1
        
        # Filter Name Label and Value
        filter_name_label = tk.Label(self, text="Filter Name:", anchor='w', bg='#f0f0f0')
        filter_name_label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='ew')
        row += 1
        
        self.filter_name_label = tk.Label(self, text=f"{self.filter_config.filter_name or 'None'}", 
                                          anchor='w', bg='#f0f0f0')
        self.filter_name_label.grid(row=row, column=0, padx=5, pady=(0, 5), sticky='ew')
        row += 1
        
        # Filter Pattern Label and Value
        filter_pattern_label = tk.Label(self, text="Filter Pattern:", anchor='w', bg='#f0f0f0')
        filter_pattern_label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='ew')
        row += 1
        
        self.sub_filters_label = tk.Label(self, text=f"{self.filter_config.sub_filters or 'None'}", 
                                          anchor='w', bg='#f0f0f0', wraplength=400)
        self.sub_filters_label.grid(row=row, column=0, padx=5, pady=(0, 5), sticky='ew')
        row += 1
        
        # Filter Color Label and Value
        filter_color_label = tk.Label(self, text="Filter Color:", anchor='w', bg='#f0f0f0')
        filter_color_label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='ew')
        row += 1
        
        # Color display frame with indicator and hex value
        color_frame = tk.Frame(self, bg='#f0f0f0')
        color_frame.grid(row=row, column=0, padx=5, pady=(0, 5), sticky='ew')
        color_frame.grid_columnconfigure(1, weight=1)
        
        self.selected_color_label = tk.Label(color_frame, text=" ", 
                                             bg=self.filter_config.selected_color or 'white',
                                             width=4, height=1, relief='solid', borderwidth=1)
        self.selected_color_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')
        
        color_value_label = tk.Label(color_frame, text=f"{self.filter_config.selected_color or 'None'}", 
                                     anchor='w', bg='#f0f0f0')
        color_value_label.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
