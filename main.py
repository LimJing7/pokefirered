try:
    import sys
    import random
    import math
    import getopt
    import pygame
    import objects
    import gamestates
    from pygame.locals import *
    from utilities import *
except ImportError, err:
    print "Could not load module", err
    pygame.quit()
    sys.exit(1)
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Cats")
    
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(BG_COLOR)
    
    currentState = gamestates.MainState(screen)

    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)
        currentState.handleEvents()
        currentState.update()
        if gamestates.change_state(currentState) == -1:
            return
        currentState.render(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
