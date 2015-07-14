try:
    import sys
    import random
    import math
    import getopt
    import pygame
    import objects
    import gamestateobjects
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
STATE_INTRO = 4
STATE_LOAD = 5
STATE_NEW = 6

nextState = STATE_NULL
nextStateObject = None

def set_next_state(newState, stateObject = None):
    global nextState
    global nextStateObject
    if nextState != STATE_QUIT:
        nextState = newState
        nextStateObject = stateObject
        print("Setting next state to {0}".format(nextState))
    
def change_state(currState):
    """
    Changes the gamestate if necessary
    
    Returns -1 if the game is to close, otherwise return 0
    """
    global nextState
    global nextStateObject
    #print("Next state is {0}".format(nextState))
    if nextState == STATE_NULL:
        return currState
    currState.close()
    
    
    if nextState == STATE_MAIN: currState = MainState(nextStateObject)
    elif nextState == STATE_BATTLE: currState = BattleState(nextStateObject)
    elif nextState == STATE_NEW: currState = NewState(nextStateObject)    
    elif nextState == STATE_QUIT:
        print("quitting")
        currState = None

    nextState = STATE_NULL
    return currState
    
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
        
    def close(self):
        return
        
class MainState(GameState):
    """
    MainState class
    
    Game state for the main map (walking around)
    """
    def __init__(self, mainStateObject):
        #blah
        return
        
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
        #screen.blit(background, self.myMap.rect, self.myMap.rect)
        self.mapSprite.draw(screen)
        self.playerSprite.draw(screen)
        
    def close(self):
        return
        
class BattleState(GameState):
    def __init__(self, battleObject):
        self.background = battleObject.background
        self.enemyCount = battleObject.count
        self.enemy = battleObject.pokemon_list[0]
        self.selfCount = #<sth>
        
    def update(self):
        screen.blit(self.background,,) #todo

class NewState(GameState):
    """
    NewState class
    
    Game state for creation of new game
    """
    def __init__(self, newStateObject):
        self.screen = newStateObject.screen
        print 'new'
    
    def update(self):
        self.mapData = [[1,2,3,4,3,2,1],[2,3,4,1,4,3,2],[3,4,1,2,1,4,3],[4,1,2,3,2,1,4],
                        [3,4,1,2,1,4,3],[2,3,4,1,4,3,2],[1,2,3,4,3,2,1]]
        self.viewSize = [5,5]
        self.viewAnchor = [1,1]
        self.myMap = objects.AreaMap(self.mapData, self.viewSize, self.viewAnchor, self.screen.get_rect().center)
        self.player = objects.Player([3,3], self.myMap)
        self.mapSprite = pygame.sprite.RenderPlain(self.myMap)
        self.playerSprite = pygame.sprite.RenderPlain(self.player)
        mainStateObject = gamestateobjects.mainStateObject(self.screen, self.myMap, self.player)
        set_next_state(STATE_MAIN, mainStateObject)
    
    def close(self):
        return

class IntroState(GameState):
    """
    IntroState class
    
    Game state for showing introduction and choosing to continue or start new game
    """
    
    def __init__(self, screen, video):
        self.cont=True
        self.movie = pygame.movie.Movie(video)
        videoplayer.play_vid(video)
        set_next_state(STATE_NEW)
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                set_next_state(STATE_QUIT)
        pressed = pygame.key.get_pressed()
        if pressed[K_UP] or pressed[K_DOWN]: self.cont = not self.cont
        elif pressed[K_RETURN]:
            if self.cont:
                set_next_state(STATE_LOAD)
            else:
                newStateObject = gamestateobjects.NewStateObject(screen)
                set_next_state(STATE_NEW, newStateObject)
    
    def update(self):
        return
    
    def render(self, screen):
        return
        
    def close(self):
        return