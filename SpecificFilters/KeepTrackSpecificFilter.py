from LogcatFilterConsts import LOG_ID_KEEP_TRACK


class KeepTrackSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_KEEP_TRACK
        self.sub_line_patterns = ['StartKeepingTrackOnBgUpload','KeepTrackOnBgUploadStatusCoroutine:',
                                  'UpdatePlayerPrefsAndUIByBgUploadInfo:']

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

        if '150 - starting keep track coroutine' in line:
            filtered_event_line = '    -> StartKeepingTrackOnBgUpload'
        elif '50.4 - [bgUploadInfoFile]  info file' in line:
            parts = line.split('50.4 - [bgUploadInfoFile]  info file ')
            parts = parts[1].split(': ')
            filtered_event_line = f'    -> info file({parts[0]}): {parts[1]}'
        elif '165 - changed scan info paths :' in line:
            filtered_event_line = '    -> changed scan info files:'
        elif '170 found changed scan info : ' in line:
            filename = line.split('170 found changed scan info : ')[1]
            filtered_event_line = f'            --->  {filename}'
        elif '[SGA][UpSess][PPandUI]: 10.0 info ts:' in line:
            progress = line.split(', progress: ')[1]
            parts = line.split('[SGA][UpSess][PPandUI]: 10.0 info ts: ')
            ts = parts[1].split(', ')[0]
            filtered_event_line = f'    -> for timestamp: {ts} progress: {progress}'
        elif '70.17 - [bgUploadInfoFile] info file changed >>>' in line:
            filtered_event_line = f'    -> info file changed >>> ' \
                                  f'{line.split("70.17 - [bgUploadInfoFile] info file changed >>> ")[1]}'
        elif '[bgUploadInfoFile] file changed >>>' in line:
            filtered_event_line = f'    -> info file changed >>> ' \
                                  f'{line.split("[bgUploadInfoFile] file changed >>>")[1]}'
        elif 'Keep Track Coroutine >>>' in line:
            filtered_event_line = f'    -> Keep Track Coroutine >>> ' \
                                  f'{line.split("Keep Track Coroutine >>>")[1]}'
        return filtered_event_line
