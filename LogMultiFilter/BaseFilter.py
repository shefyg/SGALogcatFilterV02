class BaseFilter:

    def __init__(self,filter_name, main_filter=None, sub_filters=None, tag_configs=None, sub_filter_to_tags=None, sub_filter_to_range_conf=None):
        self.filter_name = filter_name
        self.main_filter = main_filter
        self.sub_filters = sub_filters
        self.tag_configs = tag_configs
        self.sub_filter_to_tags = sub_filter_to_tags
        self.sub_filter_to_range_conf = sub_filter_to_range_conf
        self.sub_ind = 0

    def filter_line_match(self, main_ind, line):
        # if no main filter filtering by sub filters
        if not self.main_filter or self.main_filter in line:
            return self.sub_filter_line(main_ind, line)
        elif self.main_filter not in line:
            return False, None

    def sub_filter_line(self, main_ind, line):
        if not self.sub_filters:
            return True, self.get_filter_msg(main_ind, line)

        for sub_filter in self.sub_filters:
            if sub_filter in line:
                return True, self.get_filter_msg(main_ind, line, sub_filter)

        return False, None

    def get_filter_msg(self, main_ind, line, sub_filter=None):
        self.sub_ind += 1
        # Basic Filter, just return line
        # change implementation for specific message on children
        return f'{main_ind}-{self.sub_ind}: {line}'

