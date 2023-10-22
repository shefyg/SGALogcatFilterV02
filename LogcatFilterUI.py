import threading
import tkinter as tk

from MultiFilteredLogsTkFrame import MultiFilteredLogsTkFrame

DEFAULT_TEXT_WIDGET_WIDTH = 160

class LogcatFilterUI():

    def __init__(self, logcat_filter_func):

        self.logcat_filter_func = logcat_filter_func

        # Tk Root & widgets ------------------------

        # Create a root window
        self.root = tk.Tk()
        self.root.title("LogCat Filtering Dashboard")
        self.root.geometry("1920x1280")

        # Create a Text widget to display text
        self.text_widget = tk.Text(self.root, width=DEFAULT_TEXT_WIDGET_WIDTH)
        self.text_widget.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Create a vertical scrollbar and associate it with the Text widget
        scrollbar = tk.Scrollbar(self.root, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        self.text_widget.config(yscrollcommand=scrollbar.set)

        # Multi Filtered Log Frame
        self.multi_filtered_logs_frame = MultiFilteredLogsTkFrame(self.root)
        self.multi_filtered_logs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def start_gui_and_filtering(self):
        # Create a thread for the GUI
        self.filter_thread = threading.Thread(target=self.logcat_filter_func)
        self.filter_thread.daemon = True
        self.filter_thread.start()

        self.root.mainloop()

    def add_line(self, filtered_log_id, line):
        if filtered_log_id != None:
            self.text_widget.insert(tk.END, line)
            self.multi_filtered_logs_frame.add_line(filtered_log_id, line)
        else: # Add to the main log
            self.text_widget.insert(tk.END, line)
            self.text_widget.see("end")