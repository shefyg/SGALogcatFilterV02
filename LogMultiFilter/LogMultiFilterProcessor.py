import os
import threading
import json

from BaseFilter import BaseFilter
from BaseFilterConfig import BaseFilterConfig
from NotificationsMngPack.NotifMng import NotifMng
from NotificationsMngPack.NotifMngClient import NotifMngClient
from Utils import TagRangeConf, LMFNotifType, get_contrast_color, LMFNotifInfoKey


class LogMultiFilterProcessor(NotifMngClient):

    def __init__(self):

        self.log_start_process_line = ''
        self.log_stop_process_line = ''

        self._handling_processed_line_clients = set()

        self.filters = None
        # self.handle_proc_line = handle_proc_line
        self.setup_filters()
        self.last_processed_file_path = None
        
        # Stop flag and progress tracking
        self.stop_processing = False
        self.current_line = 0
        self.total_lines = 0
        
        NotifMng.register_client(LMFNotifType.FILTER_CREATED, self)
        NotifMng.register_client(LMFNotifType.CLEAR_FILTERS, self)
        # self.load_filters()

    def register_processed_line_client(self, client):
        self._handling_processed_line_clients.add(client)


    # todo: for now setting up filters here
    def setup_filters(self):
        self.filters = {}
        filter_name = 'Errors or Exceptions'
        log_filter = BaseFilter(filter_win_name=filter_name, filter_name=filter_name, sub_filters=['ERROR:', 'Exception:', 'FAIL:', 'FAILED', 'Failed', 'AttributeError:'],
                                tag_configs={"bold": {"font": ("TkDefaultFont", 10, "bold")},
                                             "danger": {"foreground": "red"},
                                             "indexes_filter_tag": {"font": ("TkDefaultFont", 10, "bold"), "foreground": "white", "background": "red"}},
                                # sub_filter_to_tags={"error": ["bold", "danger"], "ERROR": ["bold", "danger"], "exception": ["bold", "danger"], "Exception": ["bold", "danger"]},
                                sub_filter_to_tags={"ERROR:": ["bold", "danger"], "Exception:": ["bold", "danger"], "FAIL:": ["bold", "danger"], "AttributeError:":
                                    ["bold", "danger"]},
                                sub_filter_to_range_conf={"all": "TagRangeConf.SUB_FILTER_TO_END | TagRangeConf.TAG_MARK_INDEXES"}, is_default_filter=True)
        self.filters[filter_name] = log_filter

        filter_name = 'INFO'
        log_filter = BaseFilter(filter_win_name=filter_name, filter_name=filter_name, sub_filters=['INFO:'],
                                tag_configs={"bold": {"font": ("TkDefaultFont", 10, "bold")},
                                             "info": {"foreground": "green"},
                                             "indexes_filter_tag": {"font": ("TkDefaultFont", 10, "bold"), "foreground": "white", "background": "green"}},
                                # sub_filter_to_tags={"error": ["bold", "danger"], "ERROR": ["bold", "danger"], "exception": ["bold", "danger"], "Exception": ["bold", "danger"]},
                                sub_filter_to_tags={"INFO:": ["bold", "info"]},
                                sub_filter_to_range_conf={"all": "TagRangeConf.SUB_FILTER_TO_END | TagRangeConf.TAG_MARK_INDEXES"}, is_default_filter=True)
        self.filters[filter_name] = log_filter

    def HandleNotif(self, notif_type, filter_config: BaseFilterConfig) -> None:

        if (notif_type == LMFNotifType.FILTER_CREATED):
            fg = get_contrast_color(filter_config.selected_color)
            log_filter = BaseFilter(filter_win_name=filter_config.filter_win_name, filter_name=filter_config.filter_name, sub_filters=[f'{filter_config.sub_filters}'],
                                    tag_configs={f"bold_{filter_config.filter_name}": {"font": ("TkDefaultFont", 10, "bold")},
                                                 f"filter_color_{filter_config.filter_name}": {"foreground": f'{filter_config.selected_color}'},
                                                 f"indexes_filter_tag": {"font": ("TkDefaultFont", 10, "bold"), "foreground": f"{fg}",
                                                                         "background": f'{filter_config.selected_color}'}},
                                    sub_filter_to_tags={f'{filter_config.sub_filters}': [f"bold_{filter_config.filter_name}", f"filter_color_{filter_config.filter_name}"]},
                                    sub_filter_to_range_conf={"all": "TagRangeConf.SUB_FILTER_TO_END | TagRangeConf.TAG_MARK_INDEXES"},
                                    filter_config=filter_config)
            self.filters[filter_config.filter_name] = log_filter

            # reprocess log file - after delay
            # Call `my_function` after a 5-second delay
            delay = 0.45  # seconds
            # timer = threading.Timer(delay, self.process_log_file)
            # timer.start()
            # self.save_filters()
        elif notif_type == LMFNotifType.CLEAR_FILTERS and self.filters:
            # removing all filters except default
            default_filters = {k: v for k, v in self.filters.items() if v.is_default_filter}
            self.filters = default_filters
            # removing filters file
            if os.path.isfile('filters.json'):
                os.remove('filters.json')

    def process_log_file(self, file_path=None):
        # Reset stop flag when starting new processing
        self.stop_processing = False
        self.current_line = 0
        threading.Thread(target=self.process_log_file_async, args=(file_path,)).start()

    def process_log_file_async(self, file_path=None):
        # todo: need to clear log and remove all other logs - so can be called after adding filter

        if not file_path:
            file_path = self.last_processed_file_path
        else:
            self.last_processed_file_path = file_path

        print(f'on process_log_file')
        try:
            with open(file_path, 'r') as file:
                should_process=False
                is_line_nums = self.log_stop_process_line.isdigit() and self.log_start_process_line.isdigit()
                start_ind = end_ind = -1
                if is_line_nums:
                    start_ind = int(self.log_start_process_line)
                    end_ind = int(self.log_stop_process_line)

                line_ind = 1
                for line in file:
                    # Check stop flag
                    if self.stop_processing:
                        print("Processing stopped by user")
                        break
                    
                    if is_line_nums:
                        if line_ind >= start_ind:
                            should_process = True
                    elif self.log_start_process_line == '' or self.log_start_process_line in line:
                        should_process = True

                    if not should_process:
                        line_ind += 1
                        continue

                    self.current_line = line_ind
                    self.process_line(line_ind, line)
                    line_ind += 1
                    if is_line_nums and line_ind >= end_ind:
                        break
                    elif not is_line_nums and (self.log_stop_process_line != '' and self.log_stop_process_line in line):
                        break

        except FileNotFoundError:
            print(f"The file at {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Reset current line when done
            self.current_line = 0

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

        for client in self._handling_processed_line_clients:
            client.handle_line_from_processor(ind, line, filter_to_line_msgs)

    def save_filters(self):
        # get list of filters that are not default
        filters_to_save = [filter.to_dict() for filter in self.filters.values() if not filter.is_default_filter]
        # save them in file
        with open('filters.json', 'w') as file:
            json.dump(filters_to_save, file, indent=4)

    def load_filters(self):
        file_path = 'filters.json'
        if os.path.isfile(file_path):
            with open('filters.json', 'r') as file:
                filters = json.load(file)
                for log_filter in filters:
                    bf = BaseFilter.from_dict(log_filter)
                    self.filters[log_filter['filter_name']] = bf
                    # adding the widget to the ui
                    notif_info = {LMFNotifInfoKey.FILTER_CONFIG: log_filter['filter_config']}
                    NotifMng.notify(LMFNotifType.FILTER_CREATED_FROM_CONFIG, notif_info,.3)

            print(f'loaded filters: {self.filters}')
        else:
            print(f"The file {file_path} does not exist.")

    def add_custom_filters(self, filters):
        for i, log_filter in enumerate(filters):
            self.filters[log_filter.filter_name] = log_filter
            # adding the widget to the ui
            notif_info = {LMFNotifInfoKey.FILTER_CONFIG: log_filter.filter_config}
            NotifMng.notify(LMFNotifType.FILTER_CREATED_FROM_CONFIG, notif_info, .3+i*0.1)

