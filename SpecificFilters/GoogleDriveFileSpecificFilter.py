from LogcatFilterConsts import LOG_ID_GOOGLE_DRIVE_FILE


class GoogleDriveFileSpecificFilter():

    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_GOOGLE_DRIVE_FILE
        self.sub_line_patterns = ['GoogleDriveFile:', 'HandleScanFinishedWithNode:']
        # self.sub_line_ignore_patterns = ['E CameraDeviceClient: notifyError:']
        self.sub_line_ignore_patterns = None

    def check_filter_match(self, line):
        handle_with_filter = False

        # handle ignore case
        if self.sub_line_ignore_patterns is not None:
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

