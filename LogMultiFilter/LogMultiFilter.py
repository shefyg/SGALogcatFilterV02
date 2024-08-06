from LogMultiFilter.LogMultiFilterUI import LogMultiFilterUI


class LogMultiFilter:

    def __init__(self):

        self.ui = LogMultiFilterUI(open_log_file=self.open_log_file())
        self.ui.start_gui_and_filtering()

    # region functionality for ui

    def open_log_file(self):
        print(f'on open_log_file')

    # endregion

