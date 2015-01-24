try:
    import sys
    import random
    import math
    import getopt
    import pygame
    import objects
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

    mapData = [[1,2,3,4,3,2,1],[2,3,4,1,4,3,2],[3,4,1,2,1,4,3],[4,1,2,3,2,1,4],
               [3,4,1,2,1,4,3],[2,3,4,1,4,3,2],[1,2,3,4,3,2,1]]
    viewSize = [5,5]
    viewAnchor = [1,1]
    myMap = objects.AreaMap(mapData, viewSize, viewAnchor, screen.get_rect().center)
    myPlayer = objects.Player([3,3], myMap)
    mapSprite = pygame.sprite.RenderPlain(myMap)
    playerSprite = pygame.sprite.RenderPlain(myPlayer)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]: myPlayer.makeMove('u')
        elif pressed[K_DOWN]: myPlayer.makeMove('d')
        elif pressed[K_LEFT]: myPlayer.makeMove('l')
        elif pressed[K_RIGHT]: myPlayer.makeMove('r')
        screen.blit(background, myMap.rect, myMap.rect)
        screen.blit(background, myPlayer.rect, myPlayer.rect)
        mapSprite.update()
        mapSprite.draw(screen)
        playerSprite.update()
        playerSprite.draw(screen)
        #myPlayer.debugPlayer()
        #myMap.debugMap()
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
