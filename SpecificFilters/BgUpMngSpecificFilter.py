from LogcatFilterConsts import LOG_ID_BG_UP_MNG


class BgUpMngSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_BG_UP_MNG
        self.sub_line_patterns = ['BgUpProcessMng:']

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
        total_prog_sub = '[ARP_U_BgUpProcMng_upTotalUpProg]'
        if total_prog_sub in line:
            filtered_event_line = f'   total progress ->  {line.split(total_prog_sub)[1]}'
        return filtered_event_line
