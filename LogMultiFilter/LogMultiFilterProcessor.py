from BaseFilter import BaseFilter


class LogMultiFilterProcessor:

    def __init__(self, handle_proc_line):
        self.filters = None
        self.handle_proc_line = handle_proc_line
        self.setup_filters()

    # todo: for now setting up filters here
    def setup_filters(self):
        self.filters = {}
        filter_name = 'Errors or Exceptions'
        log_filter = BaseFilter(filter_name, sub_filters=['error', 'ERROR', 'exception', 'Exception'])
        self.filters[filter_name] = log_filter


    def process_log_file(self, file_path):
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
        print(f'{ind}: {line}')
        filter_to_line_msgs = {}
        for log_filter in self.filters.values():
            filter_match, msg = log_filter.filter_line_match(main_ind=ind, line=line)
            if filter_match:
                if log_filter not in filter_to_line_msgs:
                    filter_to_line_msgs[log_filter] = []
                filter_to_line_msgs[log_filter].append(msg)
        self.handle_proc_line(ind, line, filter_to_line_msgs)
