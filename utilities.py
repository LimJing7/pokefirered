try:
    import sys
    import os
    import random
    import math
    import getopt
    import pygame
    from pygame.locals import *
except ImportError, err:
    print "Could not load module", err
    pygame.quit()
    sys.exit(1)

TILE_WIDTH = 40
TILE_HEIGHT = 40
BG_COLOR = (0, 0, 0)

def load_png(name, colorkey = False):
    
    """ Load an image and return a converted image object
        Receives: Name of image
        Returns: Image object, rect of image """
    
    fullname = os.path.join("resources", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        if colorkey:
            image.set_colorkey(image.get_at((0,0)), RLEACCEL)
    except pygame.error, message:
        print "Cannot load image:", fullname
        pygame.quit()
        sys.exit(2)
    return image, image.get_rect()

def load_sound(name):
    
    """ Load a sound and return a sound object
        Receives: Name of sound
        Returns: Sound object """
    
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join("resources", name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Cannot load sound:", fullname
        pygame.quit()
        sys.exit(3)