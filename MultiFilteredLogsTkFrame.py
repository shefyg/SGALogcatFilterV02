import tkinter as tk

TEXT_WIDGET_HEIGHT = 10
LOG_ID_UPLOAD_STATE = 'App Upload State'
LOG_ID_PRE_PROCESS = 'PreProcess status'
LOG_ID_KEEP_TRACK = 'Keep track of Bg Upload'
LOG_ID_APP_CALL_PLUGIN = 'Calls to BgUpPlugin'
LOG_ID_BG_UPLOAD_SERVICE = 'From Bg Upload Service'

class MultiFilteredLogsTkFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # List to store the added text widgets
        self.text_widgets_frms = []
        self.id_to_text_widget = {}


        # Create widgets and layout for your custom frame
        label = tk.Label(self, text="Filtered Logs")
        label.pack()

        # Create a button to add text widgets
        # self.add_button = tk.Button(self, text="Add Text Widget", command=self.add_text_widget)
        # self.add_button.pack()

        self.all_text_widgets_frm = tk.Frame(self)
        self.all_text_widgets_frm.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)


    def add_text_widget(self, id):
        # Create a new frame for the text widget and scrollbar
        text_frame = tk.Frame(self.all_text_widgets_frm)
        text_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        label = tk.Label(text_frame, text=f"{id}")
        label.pack()

        # getting height of text widget
        tmp_height = TEXT_WIDGET_HEIGHT
        if id == LOG_ID_KEEP_TRACK:
            tmp_height = 30
        elif id == LOG_ID_APP_CALL_PLUGIN:
            tmp_height = 4


        # Create a new text widget
        new_text_widget = tk.Text(text_frame, height=tmp_height, width=20)
        new_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar for the text widget
        scrollbar = tk.Scrollbar(text_frame, command=new_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the text widget to use the scrollbar
        new_text_widget.config(yscrollcommand=scrollbar.set)

        # Add the new text widget to the list
        self.text_widgets_frms.append(text_frame)

    def add_line(self, filtered_log_id, line):
        if filtered_log_id not in self.id_to_text_widget:
            self.add_text_widget(filtered_log_id)
            self.id_to_text_widget[filtered_log_id] = self.text_widgets_frms[-1]

        text_widget = self.id_to_text_widget[filtered_log_id].winfo_children()[1]

        # Append the new line and the custom line passed as an argument
        updated_content = line + "\n"  # Include a newline to separate lines

        # Insert the updated content at the end
        text_widget.insert("end-1c", updated_content)

        # Scroll to the bottom
        text_widget.see("end")