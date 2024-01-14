from LogcatFilterConsts import LOG_ID_REALOGRAM


class RealogramSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_REALOGRAM
        self.sub_line_patterns = ['SessionSet: PrintRealogramFlagsReport:  >>>']

    def check_filter_match(self, line):
        handle_with_filter = False

        for sub_line_pattern in self.sub_line_patterns:
            if sub_line_pattern in line:
                handle_with_filter = True
                break
        if handle_with_filter:
            return True

        return False

    def filter_line(self, line):
        filtered_event_line = None
        return line
