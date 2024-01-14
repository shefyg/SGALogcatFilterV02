from LogcatFilterConsts import LOG_ID_KEEP_TRACK


class PreProcessSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_KEEP_TRACK
        self.sub_line_patterns = ['PreprocessAndUploadBatches','PreprocessBatchesCoroutine:']

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
        if '[ARP_U_BgUpProcMng_PreProcAndUp-10]' in line:
            filtered_event_line = f'Starting PreProcess for BgUpload'
        elif '230] Reloading batches' in line:
            filtered_event_line = f'    -> Reloading batches'
        elif '310] Starting PreprocessBatchesCoroutine' in line:
            filtered_event_line = f'    -> Starting PreprocessBatchesCoroutine'
        elif '[ARP_U_BgUpProcMng_PreProcCorut #LookAtMe -10]' in line:
            filtered_event_line = f'Starting PreProcess Coroutine for BgUpload'
        elif '50.1.4 - batch.timeStamp ' in line:
            timestamp = line.split('50.1.4 - batch.timeStamp ')[1]
            filtered_event_line = f'    -> on batch.timeStamp {timestamp}'
        elif 'finished processding batch' in line:
            filtered_event_line = f'    -> finished processing batch'
        elif 'About to upload from plugin' in line:
            filtered_event_line = f'    -> preprocessed Batches -> About to upload from plugin'
        elif '1000] - FINISHED' in line:
            filtered_event_line = f'    -> DONE PreProcessing Batches'
        else:
            return None
        return filtered_event_line
