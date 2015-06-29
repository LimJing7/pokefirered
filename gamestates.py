try:
    import sys
    import random
    import math
    import getopt
    import pygame
    import objects
    import videoplayer
    from utilities import *
    from pygame.locals import *
except ImportError, err:
    print "Could not load module", err
    pygame.quit()
    sys.exit(1)

STATE_NULL = 0
STATE_QUIT = 1
STATE_MAIN = 2
STATE_BATTLE = 3

nextState = STATE_NULL

def set_next_state(newState):
    global nextState
    if nextState != STATE_QUIT:
        nextState = newState
        
def change_state(currState, screen):
    """
    Changes the gamestate if necessary
    
    Returns -1 if the game is to close, otherwise return 0
    """
    global nextState
    if nextState == STATE_NULL:
        return 0
    currState.close()
    if nextState == STATE_MAIN: currState = MainState(screen)
    elif nextState == STATE_BATTLE: currState = BattleState()
    elif nextState == STATE_QUIT:
        nextState = STATE_NULL
        return -1
    
    nextState = STATE_NULL
    return 0
    
class GameState:
    """
    GameState class
    
    Contains current state of the game
    e.g. main map, battle screen, pokemon list, pc etc.
    
    Attributes:
    """
    
    def __init__(self):
        return
        
    def handleEvents(self):
        return
        
    def update(self):
        return
    
    def render(self, screen):
        return
       
    def setNewState(self, newState):
        return
        
    def close(self):
        return
        
class MainState(GameState):
    """
    MainState class
    
    Game state for the main map (walking around)
    """
    def __init__(self, screen):
        self.mapData = [[1,2,3,4,3,2,1],[2,3,4,1,4,3,2],[3,4,1,2,1,4,3],[4,1,2,3,2,1,4],
                        [3,4,1,2,1,4,3],[2,3,4,1,4,3,2],[1,2,3,4,3,2,1]]
        self.viewSize = [5,5]
        self.viewAnchor = [1,1]
        self.myMap = objects.AreaMap(self.mapData, self.viewSize, self.viewAnchor, screen.get_rect().center)
        self.myPlayer = objects.Player([3,3], self.myMap)
        self.mapSprite = pygame.sprite.RenderPlain(self.myMap)
        self.playerSprite = pygame.sprite.RenderPlain(self.myPlayer)
        
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                set_next_state(STATE_QUIT)
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]: self.myPlayer.makeMove('u')
        elif pressed[K_DOWN]: self.myPlayer.makeMove('d')
        elif pressed[K_LEFT]: self.myPlayer.makeMove('l')
        elif pressed[K_RIGHT]: self.myPlayer.makeMove('r')
            
    def update(self):
        self.mapSprite.update()
        self.playerSprite.update()
    
    def render(self, screen):
        print 'hello'
        #screen.blit(background, self.myMap.rect, self.myMap.rect)
        self.mapSprite.draw(screen)
        self.playerSprite.draw(screen)
        
    def close(self):
        return
        
class BattleState(GameState):
    def __init__(self):
        return
        
class IntroState(GameState):
    """
    IntroState class
    
    Game state for showing introduction and choosing to continue or start new game
    """
    
    def __init__(self, screen, video):
        self.movie = pygame.movie.Movie(video)
        videoplayer.play_vid(video)
        nextState = STATE_MAIN