import json
from enum import Enum
from typing import Optional

from BaseFilter import BaseFilter


class LogRangeType(Enum):
    UNKNOWN = "unknown"
    SUBSTRING = "sub_strs"
    LINE_NUMBER = "line_nums"


class LogRange:

    def __init__(self, range_start, range_end, range_type: LogRangeType = LogRangeType.UNKNOWN):
        self.range_start = range_start
        self.range_end = range_end

        if range_type == LogRangeType.UNKNOWN:
            range_type = LogRangeType.LINE_NUMBER if range_start.isdigit() else LogRangeType.SUBSTRING
        self.range_type = range_type

    def to_dict(self):
        return {'range_start': self.range_start,
                'range_end': self.range_end,
                'range_type': self.range_type.value}

    @classmethod
    def from_dict(cls, data):
        range_type = LogRangeType(data['range_type'])  # Convert string back to enum
        return cls(data['range_start'], data['range_end'], range_type)


class MultiLogFilterConfig:

    # region init, setup and  modify  ----------------------
    def __init__(self, config_name: str, log_range: Optional[LogRange] = None, filters=None):
        self.log_range = log_range
        self.filters = filters if filters is not None else [Optional[BaseFilter]]
        self.config_name = config_name

    def set_range(self, log_range: Optional[LogRange]):
        self.log_range = log_range

    def clear_filters(self):
        self.filters = [Optional[BaseFilter]]

    def add_filter(self, log_filter: BaseFilter):
        self.filters.append(log_filter)

    # endregion

    # region Serialization and Deserialization

    def to_dict(self):
        return {'config_name': self.config_name,
                'log_range': self.log_range.to_dict() if self.log_range else None,
                'filters': [log_filter.to_dict() for log_filter in self.filters if isinstance(log_filter, BaseFilter) and log_filter and not log_filter.is_default_filter]}

    @classmethod
    def from_dict(cls, data):
        # Deserialize log_range
        log_range = LogRange.from_dict(data['log_range']) if data['log_range'] else None

        # Deserialize filters, assuming BaseFilter has a from_dict method
        filters = [BaseFilter.from_dict(filter_data) for filter_data in data.get('filters', [])]

        # Create an instance of MultiLogFilterConfig
        return cls(
            config_name=data['config_name'],
            log_range=log_range,
            filters=filters
        )

        # Save MultiLogFilterConfig object to a JSON file with .multiLogConf extension

    def save_to_file(self, file_path=''):
        filename = f"{self.config_name}.multiLogConf"
        if not file_path:
            file_path = filename
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)  # Save as JSON with indentation
        print(f"Config saved to {file_path}")

        # Load MultiLogFilterConfig from a .multiLogConf file

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    # endregion
