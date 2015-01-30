try:
    import sys
    import random
    import math
    import getopt
    import pygame
    import objects
    from utilities import *
    from pygame.locals import *
except ImportError, err:
    print "Could not load module", err
    pygame.quit()
    sys.exit(1)