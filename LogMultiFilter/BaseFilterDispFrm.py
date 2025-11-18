import tkinter as tk

from BaseFilterConfig import BaseFilterConfig


class BaseFilterDispFrm(tk.Frame):
    def __init__(self, parent, filter_config: BaseFilterConfig, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.filter_config = filter_config
        
        # Configure frame styling with border and background
        self.config(relief='raised', borderwidth=2, bg='#f0f0f0')
        
        # Configure columns - column 0, 2, 4 for labels, column 1, 3, 5 for values
        # Column 5 for color indicator, column 6 for color value
        self.grid_columnconfigure(1, weight=1)  # Filter Group value
        self.grid_columnconfigure(3, weight=1)   # Filter Name value
        self.grid_columnconfigure(6, weight=1)    # Filter Color value (for pattern row expansion)
        
        row = 0
        
        # Row 1: Filter Group, Filter Name, Filter Color (all in one row)
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
        
        # Filter Color Label and Value
        filter_color_label = tk.Label(self, text="Filter Color:", anchor='w', bg='#f0f0f0',
                                       font=('', 9, 'bold'))
        filter_color_label.grid(row=row, column=4, padx=5, pady=5, sticky='w')
        
        # Color display with indicator and hex value
        self.selected_color_label = tk.Label(self, text=" ", 
                                             bg=self.filter_config.selected_color or 'white',
                                             width=4, height=1, relief='solid', borderwidth=1)
        self.selected_color_label.grid(row=row, column=5, padx=(0, 5), pady=5, sticky='w')
        
        color_value_label = tk.Label(self, text=f"{self.filter_config.selected_color or 'None'}", 
                                     anchor='w', bg='#f0f0f0')
        color_value_label.grid(row=row, column=6, padx=5, pady=5, sticky='ew')
        
        row += 1
        
        # Row 2: Filter Pattern (full width)
        # Configure column 1 to span all columns for full width
        filter_pattern_label = tk.Label(self, text="Filter Pattern:", anchor='w', bg='#f0f0f0',
                                         font=('', 9, 'bold'))
        filter_pattern_label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='w')
        
        self.sub_filters_label = tk.Label(self, text=f"{self.filter_config.sub_filters or 'None'}", 
                                          anchor='w', bg='#f0f0f0', wraplength=400)
        self.sub_filters_label.grid(row=row, column=1, columnspan=6, padx=5, pady=(0, 5), sticky='ew')
