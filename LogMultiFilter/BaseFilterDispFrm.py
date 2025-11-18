import tkinter as tk

from BaseFilterConfig import BaseFilterConfig


class BaseFilterDispFrm(tk.Frame):
    def __init__(self, parent, filter_config: BaseFilterConfig, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.filter_config = filter_config
        
        # Configure frame styling with border and background
        self.config(relief='raised', borderwidth=2, bg='#f0f0f0')
        
        # Configure columns - column 0, 2 for labels, column 1, 3 for values on row 1
        # Column 1 for full-width values on rows 2 and 3
        self.grid_columnconfigure(1, weight=1)  # Filter Group value
        self.grid_columnconfigure(3, weight=1)   # Filter Name value
        
        row = 0
        
        # Row 1: Filter Group and Filter Name (side by side)
        # Filter Group Label and Value
        filter_group_label = tk.Label(self, text="Filter Group:", anchor='w', bg='#f0f0f0', 
                                      font=('', 9, 'bold'))
        filter_group_label.grid(row=row, column=0, padx=5, pady=5, sticky='w')
        
        self.filter_win_name_label = tk.Label(self, text=f"{self.filter_config.filter_win_name or 'None'}", 
                                               anchor='w', bg='#f0f0f0')
        self.filter_win_name_label.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        
        # Filter Name Label and Value
        filter_name_label = tk.Label(self, text="Filter Name:", anchor='w', bg='#f0f0f0',
                                      font=('', 9, 'bold'))
        filter_name_label.grid(row=row, column=2, padx=5, pady=5, sticky='w')
        
        self.filter_name_label = tk.Label(self, text=f"{self.filter_config.filter_name or 'None'}", 
                                          anchor='w', bg='#f0f0f0')
        self.filter_name_label.grid(row=row, column=3, padx=5, pady=5, sticky='ew')
        
        row += 1
        
        # Row 2: Filter Color (full width)
        filter_color_label = tk.Label(self, text="Filter Color:", anchor='w', bg='#f0f0f0',
                                       font=('', 9, 'bold'))
        filter_color_label.grid(row=row, column=0, padx=5, pady=5, sticky='w')
        
        # Color display frame with indicator and hex value
        color_frame = tk.Frame(self, bg='#f0f0f0')
        color_frame.grid(row=row, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        color_frame.grid_columnconfigure(1, weight=1)
        
        self.selected_color_label = tk.Label(color_frame, text=" ", 
                                             bg=self.filter_config.selected_color or 'white',
                                             width=4, height=1, relief='solid', borderwidth=1)
        self.selected_color_label.grid(row=0, column=0, padx=(0, 5), pady=0, sticky='w')
        
        color_value_label = tk.Label(color_frame, text=f"{self.filter_config.selected_color or 'None'}", 
                                     anchor='w', bg='#f0f0f0')
        color_value_label.grid(row=0, column=1, padx=5, pady=0, sticky='ew')
        
        row += 1
        
        # Row 3: Filter Pattern (full width)
        filter_pattern_label = tk.Label(self, text="Filter Pattern:", anchor='w', bg='#f0f0f0',
                                         font=('', 9, 'bold'))
        filter_pattern_label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='w')
        
        self.sub_filters_label = tk.Label(self, text=f"{self.filter_config.sub_filters or 'None'}", 
                                          anchor='w', bg='#f0f0f0', wraplength=400)
        self.sub_filters_label.grid(row=row, column=1, columnspan=3, padx=5, pady=(0, 5), sticky='ew')
