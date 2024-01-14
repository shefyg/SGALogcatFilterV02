from LogcatFilterConsts import LOG_ID_APP_CALL_PLUGIN


class BgUpPluginCallsSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_APP_CALL_PLUGIN
        self.sub_line_patterns = ['BgUpPlugin']

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
        if '200 - calling the plugin UploadBatchesToFB' in line:
            filtered_event_line = '    -> Unity called plugin func UploadBatchesToFB'
        elif '120 - calling StartKeepTrackOfBatches' in line:
            filtered_event_line = '    -> Unity called plugin func StartKeepTrackOfBatches'




        return filtered_event_line
