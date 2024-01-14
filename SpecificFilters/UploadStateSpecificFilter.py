from LogcatFilterConsts import LOG_ID_UPLOAD_STATE


class UploadStateSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_UPLOAD_STATE
        self.sub_line_patterns = ['CreateStatusFileForState']


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
        status = line.split('US_')[1].split('.status')[0]
        filtered_event_line = f'Status file:{status}'
        return filtered_event_line
