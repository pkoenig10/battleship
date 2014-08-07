HOST = "127.0.0.1"
PORT = 2885

RECV_SIZE  = 1024
END_COMMAND = "\0"

ROWS = 10
COLS = 14

AIRCRAFT_CARRIER_SIZE = 5
BATTLESHIP_SIZE = 4
DESTROYER_SIZE = 3
SUBMARINE_SIZE = 3
PATROL_BOAT_SIZE = 2

AIRCRAFT_CARRIER_MISSILES = 2
BATTLESHIP_MISSILES = 1
DESTROYER_MISSILES = 2
SUBMARINE_MISSILES = 2
PATROL_BOAT_MISSILES = 0

BACKGROUND_COLOR = "grey30"
PADX = 10
PADY = 10
PEG_PADDING = 2
RECON_PADDING = 6

COORDINATE_SIZE = 25
COORDINATE_OUTLINE = 2
BOARD_COLOR = "cyan"
BOARD_OUTLINE_COLOR = "deep sky blue"
BOARD_TEXT_COLOR = "black"

LOG_COLOR = "grey50"
LOG_TEXT_COLOR = "white"
LOG_WIDTH = 30
LOG_HEIGHT = 10

INFO_TEXT_COLOR = "white"
INFO_KEY_COLOR = "gold"
INFO_KEY_TEXT_COLOR = "black"
INFO_KEY_PADX = (0,10)
INFO_PATTERN_SIZE = 9
INFO_PATTERN_OUTLINE = 2
INFO_PATTERN_ARROW_WIDTH = 3
INFO_PATTERN_ARROW_SHAPE = (7,8,3)
INFO_PATTERN_PADY = (0,10)
INFO_COL_MINSIZE = 50
INFO_SPACE_MINSIZE = 20

PATTERN_ROWS = 3
PATTERN_COLS = 3
PATTERN_MARK = "X"
AIRCRAFT_CARRIER_PATTERN_1 = "X-X-X-X-X"
AIRCRAFT_CARRIER_PATTERN_2 = "-X-XXX-X-"
BATTLESHIP_PATTERN = "XXXXXXXXX"
DESTROYER_PATTERN_1 = "---XXX---"
DESTROYER_PATTERN_2 = "-X--X--X-"
ANTI_AIRCRAFT_GUN_PATTERN = "----X----"
SUBMARINE_SCAN_PATTERN = "XXXXXXXXX"
RECON_ONE_SCAN_PATTERN_1 = "X-X---X-X"
RECON_ONE_SCAN_PATTERN_2 = "-X-X-X-X-"
RECON_TWO_SCAN_PATTERN_1 = "X-X---X-X"
RECON_TWO_SCAN_PATTERN_2 = "-X-X-X-X-"

STATUS_EMPTY = 0
STATUS_SUBMARINE_SCAN = 1
STATUS_RECON_SCAN = 2
STATUS_MISS = 3
STATUS_HIT = 4
STATUS_AIRCRAFT_CARRIER = 5
STATUS_BATTLESHIP = 6
STATUS_DESTROYER = 7
STATUS_SUBMARINE = 8
STATUS_PATROL_BOAT = 9
STATUS_RECON_ONE = 10
STATUS_RECON_TWO = 11

COLOR_MISS = "white"
COLOR_HIT = "red"
COLOR_SUBMARINE_SCAN = "blue"
COLOR_RECON_SCAN = "royal blue"
COLOR_AIRCRAFT_CARRIER = "grey"
COLOR_BATTLESHIP = "grey"
COLOR_DESTROYER = "grey"
COLOR_SUBMARINE = "grey35"
COLOR_PATROL_BOAT = "grey"
COLOR_RECON_ONE = "red4"
COLOR_RECON_TWO = "blue4"

COMMAND_MESSAGE = "MESSAGE"
COMMAND_CLEAR = "CLEAR"
COMMAND_CANCEL = "CANCEL"
COMMAND_KEY = "KEY"
COMMAND_SHIP = "SHIP"
COMMAND_RECON_SHIP_BOARD = "RECON_SHIP_BOARD"
COMMAND_RECON_BOARD = "RECON_BOARD"
COMMAND_PEG_SHIP_BOARD = "PEG_SHIP_BOARD"
COMMAND_PEG_BOARD = "PEG_BOARD"

KEY_COMMAND_NONE = "NONE"
KEY_COMMAND_MOVE = "MOVE"
KEY_COMMAND_PATTERN = "PATTERN"
KEY_COMMAND_COORDINATE = "COORDINATE"
KEY_COMMAND_COORDINATE_COL = "COORDINATE_COL"
KEY_COMMAND_SHIP = "SHIP"
KEY_COMMAND_SHIP_COL = "SHIP_COL"
KEY_COMMAND_ENTER = "ENTER"

MOVE_MISSILE = "MISSILE"
AIRCRAFT_CARRIER_MISSILE = "AIRCRAFT_CARRIER_MISSILE"
BATTLESHIP_MISSILE = "BATTLESHIP_MISSILE"
DESTROYER_MISSILE = "DESTROYER_MISSILE"
SUBMARINE_MISSILE = "SUBMARINE_MISSILE"
ANTI_AIRCRAFT_GUN = "ANTIAIRCRAFT_GUN"
SUBMARINE_SCAN = "SUBMARINE_SCAN"
RECON_1_FLY = "RECON_1_FLY"
RECON_2_FLY = "RECON_2_FLY"
RECON_1_SCAN = "RECON_1_SCAN"
RECON_2_SCAN = "RECON_2_SCAN"

KEY_F1 = "F1"
KEY_F2 = "F2"
KEY_F3 = "F3"
KEY_F4 = "F4"
KEY_F5 = "F5"
KEY_F6 = "F6"
KEY_F7 = "F7"
KEY_F8 = "F8"
KEY_F9 = "F9"
KEY_F10 = "F10"
KEY_ENTER = "Return"
KEY_NUM_ENTER = "KP_Enter"
KEY_BACKSPACE = "BackSpace"
KEY_DELETE = "Delete"
KEY_ESCAPE = "Escape"

CANCEL = "Cancel"
CLEAR = "Clear"

