from LogcatFilterConsts import LOG_ID_EXCEPT_AND_ERRS


class ExceptAndErrSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_EXCEPT_AND_ERRS
        self.sub_line_patterns = ['Exception','Error:']
        self.sub_line_ignore_patterns = ['E CameraDeviceClient: notifyError:', 'StorageUtil: Error getting App Check token; using placeholder to']

    def check_filter_match(self, line):
        handle_with_filter = False

        # handle ignore case
        for sub_line_pattern in self.sub_line_ignore_patterns:
            if sub_line_pattern.lower() in line.lower():
                return False

        # handle with filter
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
