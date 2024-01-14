from LogcatFilterConsts import LOG_ID_SHELF_COVERAGE


class ShelfCoverageSpecificFilter():

    def __init__(self, log_id=None, sub_line_patterns=[]):
        # Using specific params for this class
        self.log_id = LOG_ID_SHELF_COVERAGE
        self.sub_line_patterns = ['ImageUploadShelfCoverage:', '[#ShelfCoverage]']
        self.sub_line_ignore_patterns = None

    def check_filter_match(self, line):
        handle_with_filter = False

        # handle ignore case
        if self.sub_line_ignore_patterns is not None:
            for sub_line_pattern in self.sub_line_ignore_patterns:
                if sub_line_pattern.lower() in line.lower():
                    return False

        # handle with filter
        for sub_line_pattern in self.sub_line_patterns:
            if sub_line_pattern in line:
                handle_with_filter = True
                break
        if handle_with_filter:
            return True

        return False

    def filter_line(self, line):
        filtered_event_line = None

        processed_line = line
        for sep in self.sub_line_patterns:
            if sep in processed_line:
                processed_line = processed_line.split(sep)[1]

        filtered_event_line = f'  -> shelfCoverage check: {processed_line}'

        return filtered_event_line

