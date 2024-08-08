import threading

from BaseFilter import BaseFilter
from BaseFilterConfig import BaseFilterConfig
from NotificationsMngPack.NotifMng import NotifMng
from NotificationsMngPack.NotifMngClient import NotifMngClient
from Utils import TagRangeConf, LMFNotifType, get_contrast_color


class LogMultiFilterProcessor(NotifMngClient):

    def __init__(self, handle_proc_line):
        self.filters = None
        self.handle_proc_line = handle_proc_line
        self.setup_filters()
        self.last_processed_file_path = None
        NotifMng.register_client(LMFNotifType.FILTER_CREATED, self)

    # todo: for now setting up filters here
    def setup_filters(self):
        self.filters = {}
        filter_name = 'Errors or Exceptions'
        log_filter = BaseFilter(filter_name, sub_filters=['ERROR:', 'Exception:'],
                                tag_configs={"bold": {"font": ("TkDefaultFont", 10, "bold")},
                                             "danger": {"foreground": "red"},
                                             "indexes_filter_tag": {"font": ("TkDefaultFont", 10, "bold"), "foreground": "white", "background": "red"}},
                                # sub_filter_to_tags={"error": ["bold", "danger"], "ERROR": ["bold", "danger"], "exception": ["bold", "danger"], "Exception": ["bold", "danger"]},
                                sub_filter_to_tags={"ERROR:": ["bold", "danger"], "Exception:": ["bold", "danger"]},
                                sub_filter_to_range_conf={"all": TagRangeConf.SUB_FILTER_TO_END | TagRangeConf.TAG_MARK_INDEXES})
        self.filters[filter_name] = log_filter

        filter_name = 'INFO'
        log_filter = BaseFilter(filter_name, sub_filters=['INFO:'],
                                tag_configs={"bold": {"font": ("TkDefaultFont", 10, "bold")},
                                             "info": {"foreground": "green"},
                                             "indexes_filter_tag": {"font": ("TkDefaultFont", 10, "bold"), "foreground": "white", "background": "green"}},
                                # sub_filter_to_tags={"error": ["bold", "danger"], "ERROR": ["bold", "danger"], "exception": ["bold", "danger"], "Exception": ["bold", "danger"]},
                                sub_filter_to_tags={"INFO:": ["bold", "info"]},
                                sub_filter_to_range_conf={"all": TagRangeConf.SUB_FILTER_TO_END | TagRangeConf.TAG_MARK_INDEXES})
        self.filters[filter_name] = log_filter

    def HandleNotif(self, notif_type, filter_config:BaseFilterConfig) -> None:

        fg = get_contrast_color(filter_config.selected_color)

        if(notif_type == LMFNotifType.FILTER_CREATED):
            log_filter = BaseFilter(filter_config.filter_name, sub_filters=[f'{filter_config.sub_filters}'],
                                    tag_configs={"bold": {"font": ("TkDefaultFont", 10, "bold")},
                                             "filter_color": {"foreground": f'{filter_config.selected_color}'},
                                             "indexes_filter_tag": {"font": ("TkDefaultFont", 10, "bold"), "foreground": f"{fg}", "background": f'{filter_config.selected_color}'}},
                                    sub_filter_to_tags = {f'{filter_config.sub_filters}': ["bold", "filter_color"]},
                                    sub_filter_to_range_conf = {"all": TagRangeConf.SUB_FILTER_TO_END | TagRangeConf.TAG_MARK_INDEXES})
            self.filters[filter_config.filter_name] = log_filter

            # reprocess log file - after delay
            # Call `my_function` after a 5-second delay
            delay = 0.45  # seconds
            timer = threading.Timer(delay, self.process_log_file)
            timer.start()

    def process_log_file(self, file_path=None):
        # todo: need to clear log and remove all other logs - so can be called after adding filter

        if not file_path:
            file_path = self.last_processed_file_path
        else:
            self.last_processed_file_path = file_path

        print(f'on process_log_file')
        try:
            with open(file_path, 'r') as file:
                line_ind = 1
                for line in file:
                    self.process_line(line_ind, line)
                    line_ind += 1
        except FileNotFoundError:
            print(f"The file at {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def process_line(self, ind, line):
        # todo: filter and add it to ui
        # print(f'{ind}: {line}')
        filter_to_line_msgs = {}
        for log_filter in self.filters.values():
            filter_match, msg = log_filter.filter_line_match(main_ind=ind, line=line)
            if filter_match:
                if log_filter not in filter_to_line_msgs:
                    filter_to_line_msgs[log_filter] = []
                filter_to_line_msgs[log_filter].append(msg)
        self.handle_proc_line(ind, line, filter_to_line_msgs)
