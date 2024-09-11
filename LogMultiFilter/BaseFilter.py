from BaseFilterConfig import BaseFilterConfig
from Utils import TagRangeConf


class BaseFilter:

    def __init__(self, filter_win_name, filter_name, main_filter=None, sub_filters=None, tag_configs=None, sub_filter_to_tags=None, sub_filter_to_range_conf=None,
                 filter_config=None, is_default_filter=False):
        self.filter_win_name = filter_win_name
        self.filter_name = filter_name
        self.main_filter = main_filter
        self.sub_filters = sub_filters
        self.tag_configs = tag_configs
        self.sub_filter_to_tags = sub_filter_to_tags
        self.sub_filter_to_range_conf = sub_filter_to_range_conf
        # TODO: this is a small fix for loading - change in the future if needed
        if "all" in self.sub_filter_to_range_conf:
            self.sub_filter_to_range_conf["all"] = {TagRangeConf.SUB_FILTER_TO_END , TagRangeConf.TAG_MARK_INDEXES}
        self.filter_config = filter_config
        self.is_default_filter = is_default_filter
        self.sub_ind = 0

    def to_dict(self):
        sub_filter_to_range_conf = {}
        sub_filter_to_range_conf.update(self.sub_filter_to_range_conf)
        if "all" in sub_filter_to_range_conf:
            sub_filter_to_range_conf["all"] = "{TagRangeConf.SUB_FILTER_TO_END | TagRangeConf.TAG_MARK_INDEXES}"

        return {"filter_win_name": self.filter_win_name,
                "filter_name": self.filter_name,
                "main_filter": self.main_filter if self.main_filter is not None else "",
                "sub_filters": list(self.sub_filters) if isinstance(self.sub_filters, set) else self.sub_filters,
                "tag_configs": self.tag_configs,
                "sub_filter_to_tags": self.sub_filter_to_tags,
                "sub_filter_to_range_conf": sub_filter_to_range_conf,
                "filter_config": self.filter_config.to_dict() if isinstance(self.filter_config, BaseFilterConfig) else self.filter_config,
                "is_default_filter": self.is_default_filter}

    @classmethod
    def from_dict(cls, data):
        return cls(data["filter_win_name"], data["filter_name"], data["main_filter"], data["sub_filters"], data["tag_configs"], data["sub_filter_to_tags"],
                   data["sub_filter_to_range_conf"], data["filter_config"], data["is_default_filter"])

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

    def __repr__(self):
        return f'{self.filter_win_name}-{self.filter_name}'
