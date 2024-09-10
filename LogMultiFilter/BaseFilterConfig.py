class BaseFilterConfig:

    def __init__(self, info=None):
        self.filter_win_name = None
        self.filter_name = None
        self.sub_filters = None
        self.selected_color = None
        if info:
            self.filter_win_name = info['filter_win_name']
            self.filter_name = info['filter_name']
            self.sub_filters = info['sub_filters']
            self.selected_color = info['selected_color']

    def to_dict(self):
        return {"filter_win_name": self.filter_win_name, "filter_name": self.filter_name, "sub_filters": self.sub_filters, "selected_color": self.selected_color}

    @classmethod
    def from_dict(cls, data):
        return cls(info=data)
