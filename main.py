from config import PARSER_MODE

from instructions import usual_mode
from instructions import full_mode
from instructions import unusual_mode
from instructions import repeat_mode
from instructions import debug_mode


if __name__ == "__main__":
    # PARSER_MODE: Literal["usual", "full", "repeat", "debug", "unusual"]
    match PARSER_MODE:
        case "usual":
            usual_mode()
        case "full":
            full_mode()
        case "repeat":
            repeat_mode()
        case "debug":
            debug_mode()
        case "unusual":
            unusual_mode()
