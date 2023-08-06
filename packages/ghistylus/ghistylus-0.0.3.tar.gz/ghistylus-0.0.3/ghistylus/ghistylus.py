class ghistylus(object):
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, color, phrase):
        
        print (color+phrase+'\033[0m')
    
        