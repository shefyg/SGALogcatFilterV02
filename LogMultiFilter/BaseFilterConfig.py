class BaseFilterConfig:

    def __init__(self):
        self.filter_name = None
        self.sub_filters = None
        self.selected_color = None
        self.sub_filters_to_color = None

    # def expand_with_filter(self, log_filter: 'BaseFilterConfig'):
    #     if self.filter_name != log_filter.filter_name:
    #         # Example error handling
    #         raise ValueError(f"Filter names do not match: {self.filter_name} vs {log_filter.filter_name}")
    #
    #     # for filter combined - make sure cna address different sub filters colors
    #     if self.sub_filters_to_color is None:
    #         self.sub_filters_to_color = {}
    #         for sub_filter in self.sub_filters:
    #             self.sub_filters_to_color[sub_filter] = self.selected_color
    #
    #     # handling the new sub filters
    #     self.sub_filters.extend(log_filter.sub_filters)
    #     for sub_filter in log_filter.sub_filters:
    #         self.sub_filters_to_color[sub_filter] = log_filter.selected_color






