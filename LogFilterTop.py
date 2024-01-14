import tkinter as tk
from tkinter import Toplevel
from LogcatFilterConsts import *
from SGAUtils2024.SGAUtils import SGAUtils


class LogFilterTop(Toplevel):

    filters_top_count = 0

    def __init__(self, parent, id="Log Filter"):
        super().__init__(parent)

        self.text_widget = None

        self.instance_id = LogFilterTop.filters_top_count
        LogFilterTop.filters_top_count += 1
        x_pos = (self.instance_id%4) * 640

        self.title(id)
        self.geometry(f"640x1280+{x_pos}+0")
        self.bg_color = SGAUtils.bg_color_from_string(id)
        self.configure(bg=self.bg_color)
        self.add_text_widget(id)

    def add_text_widget(self, id):
        # Create a new frame for the text widget and scrollbar
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH)

        label = tk.Label(self.text_frame, text=f"{id}")
        label.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        # Create a new text widget
        self.text_widget = tk.Text(self.text_frame, height=TEXT_WIDGET_HEIGHT, width=20, bg=self.bg_color)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the text widget
        scrollbar = tk.Scrollbar(self.text_frame, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the text widget to use the scrollbar
        self.text_widget.config(yscrollcommand=scrollbar.set)

    def add_line(self, line):

        # Append the new line and the custom line passed as an argument
        appended_content = line + "\n"  # Include a newline to separate lines

        # Insert the updated content at the end
        self.text_widget.insert("end-1c", appended_content)

        # Scroll to the bottom
        self.text_widget.see("end")
