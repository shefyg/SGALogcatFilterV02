from LogcatFilterConsts import LOG_ID_BG_UPLOAD_SERVICE


class BgUpServiceSpecificFilter():
    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_BG_UPLOAD_SERVICE
        self.sub_line_patterns = ['BgUploadService', '[SGA]<#bgUpPlug>[BatchInfoAndState]', '[SGA]<#bgUpPlug>']

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
        elif '[SGA]<#bgUpPlug>[BIAS]' in line:
            if ' Progress for batchInfo ' in line:
                filtered_event_line = f'>>> {line.split(">>>")[1]}'
        elif 'BgUploadService[SGA]<#bgUpPlug>[BUS][upBF][BIAS]' in line:
            if '30.5 - filename:' in line:
                filtered_event_line = f'  -> About to upload {line.split("filename:")[1]}'
            elif '230 -  Uploading file:' in line:
                filtered_event_line = f'  -> Uploading file: {line.split("Uploading file:")[1]}'
            elif 'BgUploadService[SGA]<#bgUpPlug>[BgUploadService][uploadPreProcessedFileToFB]' in line:
                filtered_event_line = f'  -> uploadPreProcessedFileToFB : {line.split("[uploadPreProcessedFileToFB]")[1]}'
        elif '[SGA]<#bgUpPlug>[BUS][upBF][BIAS]' in line:
            filtered_event_line = f'  -> uploadBathesFiles : {line.split("[SGA]<#bgUpPlug>[BUS][upBF][BIAS]")[1]}'
        elif '[SGA]<#bgUpPlug>[BatchInfoAndState][toString]' in line:
            filtered_event_line = f'  -> {line}'
        elif '[SGA]<#bgUpPlug>[BatchFileRecord][getBatchInfoJsonStr]' in line:
            filtered_event_line = f'  -> {line.split("[getBatchInfoJsonStr]")[1]}'
        elif '[SGA]<#bgUpPlug>[BIAS][upFileFromObj]' in line:
            filtered_event_line = f'  ->[upFileFromObj]: {line.split("[upFileFromObj]")[1]}'

        return filtered_event_line
