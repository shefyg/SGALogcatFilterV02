class BaseFilter:

    def __init__(self,filter_name, main_filter=None, sub_filters=None, tag_configs=None, sub_filter_to_tags=None, sub_filter_to_range_conf=None):
        self.filter_name = filter_name
        self.main_filters = [main_filter] if main_filter is not None else []
        self.sub_filters = sub_filters
        self.tag_configs = tag_configs
        self.sub_filter_to_tags = sub_filter_to_tags
        self.sub_filter_to_range_conf = sub_filter_to_range_conf
        self.sub_ind = 0

    def expand_with_filter(self, log_filter: 'BaseFilter'):
        if self.filter_name != log_filter.filter_name:
            raise ValueError(f"Filter names do not match: {self.filter_name} vs {log_filter.filter_name}")
        self.main_filters.extend(log_filter.main_filters)
        self.sub_filters.extend(log_filter.sub_filters)
        self.tag_configs.update(log_filter.tag_configs)
        self.sub_filter_to_tags.update(log_filter.sub_filter_to_tags)
        self.sub_filter_to_range_conf.update(log_filter.sub_filter_to_range_conf)

    def filter_line_match(self, main_ind, line):
        # check if any main filter in line
        found_main_filter = False
        if self.main_filters:
            for main_filter in self.main_filters:
                if main_filter in line:
                    found_main_filter = True
                    break

        # if no main filter  or found it in line - continue to filtering by sub filters
        if not self.main_filters or found_main_filter:
            return self.sub_filter_line(main_ind, line)
        elif self.main_filters not in line:
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


