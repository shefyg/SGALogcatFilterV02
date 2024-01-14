
# Constants for LogcatFilte
DEFAULT_LOG = None

LOG_ID_UPLOAD_STATE = 'App Upload State'
LOG_ID_PRE_PROCESS = 'PreProcess status'
LOG_ID_KEEP_TRACK = 'Keep track of Bg Upload'
LOG_ID_APP_CALL_PLUGIN = 'Calls to BgUpPlugin'
LOG_ID_BG_UP_MNG = 'BgUpMng Log'
LOG_ID_BG_UPLOAD_SERVICE = 'From Bg Upload Service'
LOG_ID_EXCEPT_AND_ERRS = 'Exceptions and Errors'
LOG_ID_REALOGRAM = 'Realogram'
LOG_ID_WORKFLOW = 'WorkFlow'
LOG_ID_GOOGLE_DRIVE_FILE = 'Google Drive File:'
LOG_ID_SHELF_COVERAGE = 'Shelf Coverage'

# size constants for ui
TEXT_WIDGET_HEIGHT = 75

# Text colors for console output
    # ANSI escape codes for text colors
    # ANSI escape codes for text and background colors
RED_TEXT = "\033[91m"
GREEN_TEXT = "\033[92m"
WHITE_TEXT = "\033[97m"  # White text color
BLACK_TEXT = "\033[30m"
RESET_COLOR = "\033[39m"  # Reset text color to default
RESET_BG = "\033[49m"  # Reset background color to default

# ANSI escape codes for bold text
BOLD = "\033[1m"
RESET_BOLD = "\033[0m"  # Reset bold text to normal

# Background colors
WHITE_BG = "\033[107m"
YELLOW_BG = "\033[103m"
RED_BG = "\033[41m"  # Red background
RESET_ALL = "\033[0m"  # Reset all formatting