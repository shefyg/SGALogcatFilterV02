import re
import subprocess

from LogcatFilterUI import LogcatFilterUI

DEFAULT_LOG = None

LOG_ID_UPLOAD_STATE = 'App Upload State'
LOG_ID_PRE_PROCESS = 'PreProcess status'
LOG_ID_KEEP_TRACK = 'Keep track of Bg Upload'
LOG_ID_APP_CALL_PLUGIN = 'Calls to BgUpPlugin'
LOG_ID_BG_UPLOAD_SERVICE = 'From Bg Upload Service'

class BasicFilter:
    # ANSI escape codes for text colors
    # ANSI escape codes for text and background colors
    RED_TEXT = "\033[91m"
    GREEN_TEXT = "\033[92m"
    WHITE_TEXT = "\033[97m"  # White text color
    BLACK_TEXT = "\033[30m"
    RESET_COLOR = "\033[39m"  # Reset text color to default
    RESET_BG = "\033[49m"  # Reset background color to default

    # ANSI escape codes for bold text
    BOLD = "\033[1m"
    RESET_BOLD = "\033[0m"  # Reset bold text to normal

    # Background colors
    WHITE_BG = "\033[107m"
    YELLOW_BG = "\033[103m"
    RED_BG = "\033[41m"  # Red background
    RESET_ALL = "\033[0m"  # Reset all formatting

    def __init__(self):
        self.ui = LogcatFilterUI(self.start_filtering_logcat)
        self.ui.start_gui_and_filtering()

    def start_filtering_logcat(self):
        self.setup_for_filtering()
        self.got_app_pid = False
        self.get_logcat()

    def setup_for_filtering(self):
        self.filters = [
            r'A>>|BgUpProcMng|bgUp|bgUpPlug|SGA',
            r'Error:',
            r'Exception:',
            r'SomeCustomTag',  # Replace with your custom tag
            r'planogram',  # Replace with your custom tag
        ]
        self.pattern = '|'.join(self.filters)

        self.pids = []

        # self.pattern = r'(A>>|BgUpProcMng|bgUp|bgUpPlug|SGA)' # r'(Error:|Exception:|planogram|)'

        self.pattern_to_color = {
            r'Error:': [self.RED_BG, self.WHITE_TEXT],
            r'Exception:':[self.RED_BG, self.WHITE_TEXT],
            r'CreateStatusFileForState:': [self.YELLOW_BG, self.BLACK_TEXT],
        }

    def get_logcat(self):
        try:
            self.clear_logs()
            subprocess.run(['adb', 'logcat', '-G', '4M'])
            # Run the ADB command to capture logcat and store it in a file
            process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, universal_newlines=True,
                                       encoding='utf-8')

            # Open a file for saving logcat messages
            with open('logcat.txt', 'w', encoding='utf-8') as logcat_file:
                with open('appEvents.txt', 'w', encoding='utf-8') as events_file:
                    for line in process.stdout:
                        # Chaning filter based on information found in the logcat
                        self.in_process_filtesrs_setup(line)

                        # Check if the line matches the pattern
                        self.handle_line(line, logcat_file, events_file)

            print("Logcat messages saved to logcat.txt")
        except subprocess.CalledProcessError as e:
            print("Error:", e)

    def handle_line(self, line, logcat_file, events_file):
        show_line = True #TODO: Fix this
        # # check for pids
        # for pid in self.pids:
        #     parts = line.split()
        #     if len(parts) >= 3 and pid == parts[2]:
        #         show_line = True
        #         break

        pattern_found = re.search(self.pattern, line)

        # general filters
        if show_line and pattern_found:
            # Print and write the line to the filtered logcat file
            # print line colored
            self.format_print_line(line)
            logcat_file.write(line)
            logcat_file.flush()

            # Check if the line is an event and write it to the events file
            # write it anywat to the log
            self.log_events(events_file, line)
            self.ui.add_line(filtered_log_id=DEFAULT_LOG, line=line)

    def log_events(self, events_file, line):
        """
        Process log events and write to the events file.

        :param events_file: The file to write log events to.
        :param line: The log event to process.
        :return: True if the event is filtered, False otherwise.
        :rtype: bool
        """

        log_id = None
        filtered_event_line = ''
        if 'CreateStatusFileForState' in line and 'US_' in line:
            log_id = LOG_ID_UPLOAD_STATE
            filtered_event_line = self.filter_app_upload_status_line(filtered_event_line, line)
        elif 'PreprocessAndUploadBatches: ' in line:
            log_id =  LOG_ID_PRE_PROCESS
            filtered_event_line = self.filter_bgUp_preProcess_line(line)
        elif 'PreprocessBatchesCoroutine: ' in line:
            log_id = LOG_ID_PRE_PROCESS
            filtered_event_line = self.filter_bgUp_preProcessCotourine_line(line)
        elif 'StartKeepingTrackOnBgUpload' in line or 'KeepTrackOnBgUploadStatusCoroutine:' in line or\
                'UpdatePlayerPrefsAndUIByBgUploadInfo:' in line:
            log_id = LOG_ID_KEEP_TRACK
            filtered_event_line = self.filter_bgUp_keepTrack_line(line)
        elif 'BgUpPlugin:' in line:
            log_id = LOG_ID_APP_CALL_PLUGIN
            filtered_event_line = self.filter_bgUp_plugin_line(line)
        elif 'BgUploadService' in line:
            log_id = LOG_ID_BG_UPLOAD_SERVICE
            filtered_event_line = self.filter_bgUp_service_line(line)

        if log_id is None or filtered_event_line == None:
            return False  # Early return if not found filtered

        datetime_from_line = self.get_datetime_from_line(line)
        self.ui.add_line(filtered_log_id=log_id, line=f'{datetime_from_line} {filtered_event_line}')

        events_file.write(filtered_event_line)
        events_file.flush()
        return True  # Return True if filtered

    def filter_bgUp_plugin_line(self, line):
        filtered_event_line = None
        if '200 - calling the plugin UploadBatchesToFB' in line:
            filtered_event_line = '    -> Unity called plugin func UploadBatchesToFB'
        elif '120 - calling StartKeepTrackOfBatches' in line:
            filtered_event_line = '    -> Unity called plugin func StartKeepTrackOfBatches'

        return filtered_event_line

    def get_datetime_from_line(self, line):
        parts = line.split()
        if len(parts) >= 3:
            return parts[0] + ' ' + parts[1]
        return ''

    def filter_bgUp_keepTrack_line(self, line):
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

        return filtered_event_line

    def filter_bgUp_service_line(self, line):
        filtered_event_line = None

        if 'onStartCommand' in line:
            command_key = None
            if '- commandKey ' in line:
                if '- commandKey ' in line:
                    command_key = line.split('- commandKey ')[1]
                elif '- commandKey: ' in line:
                    command_key = line.split('- commandKey: ')[1]
                if command_key == 10:
                    command_key = '10 - COMMAND_UPLOAD_BATCHES_FB'
                elif command_key == 11:
                    command_key = '11 - COMMAND_TRACK_BATCHES'
                filtered_event_line = f'    -> onStartCommand with commandKey: {command_key}'

        return filtered_event_line

    def filter_bgUp_preProcessCotourine_line(self, line):
        if '[ARP_U_BgUpProcMng_PreProcCorut #LookAtMe -10]' in line:
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

    def filter_bgUp_preProcess_line(self, line):
        if '[ARP_U_BgUpProcMng_PreProcAndUp-10]' in line:
            filtered_event_line = f'Starting PreProcess for BgUpload'
        elif '230] Reloading batches' in line:
            filtered_event_line = f'    -> Reloading batches'
        elif '310] Starting PreprocessBatchesCoroutine' in line:
            filtered_event_line = f'    -> Starting PreprocessBatchesCoroutine'
        else:
            return None
        return filtered_event_line

    def filter_app_upload_status_line(self, filtered_event_line, line):
        status = line.split('US_')[1].split('.status')[0]
        filtered_event_line = f'Status file:{status}'
        return filtered_event_line

    def format_print_line(self, line):
        for k,v in self.pattern_to_color.items():
            if re.search(k, line):
                format_params =  ''.join(v)
                line = line.replace(k, format_params + k + self.RESET_ALL)
        print(line, end='')


    def in_process_filtesrs_setup(self, line):
        # look for my process id
        if self.got_app_pid == False and 'com.arpalus.planogramcompliance' in line:
            parts = line.split()
            pid = parts[2]
            # self.filters.append(pid)
            self.pids.append(pid);

            self.got_app_pid = True
            self.pattern_to_color[pid] = [self.GREEN_TEXT]

    def clear_logs(self):
        try:
            subprocess.run(['adb', 'logcat', '-c'], check=True)
            print("Logs cleared successfully.")
        except subprocess.CalledProcessError as e:
            print("Error:", e)

if __name__ == '__main__':
    bf = BasicFilter()
