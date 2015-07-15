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
screenSize = []

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
    
    def render(self):
        return
        
    def close(self):
        return
        
class MainState(GameState):
    """
    MainState class
    
    Game state for the main map (walking around)
    """
    def __init__(self, mainStateObject):
        self.screen = mainStateObject.screen
        self.player = mainStateObject.player
        self.map = mainStateObject.map
        self.mapSprite = pygame.sprite.RenderPlain(self.map)
        self.playerSprite = pygame.sprite.RenderPlain(self.player)
        
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                set_next_state(STATE_QUIT)
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]: self.player.makeMove('u')
        elif pressed[K_DOWN]: self.player.makeMove('d')
        elif pressed[K_LEFT]: self.player.makeMove('l')
        elif pressed[K_RIGHT]: self.player.makeMove('r')
            
    def update(self):
        self.mapSprite.update()
        self.playerSprite.update()
    
    def render(self):
        #screen.blit(background, self.myMap.rect, self.myMap.rect)
        self.mapSprite.draw(self.screen)
        self.playerSprite.draw(self.screen)
        
    def close(self):
        return
        
class BattleState(GameState):
    def __init__(self, battleObject):
        self.background = battleObject.background
        self.enemyCount = battleObject.count
        self.enemy = battleObject.pokemon_list
        self.screen = battleObject.screen
        #self.selfCount = #<sth>
        
    def update(self):
        self.screen.blit(self.background,self.screen.get_rect()) #todo

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
        mainStateObject = gamestateobjects.MainStateObject(self.screen, self.myMap, self.player)
        set_next_state(STATE_MAIN, mainStateObject)
    
    def close(self):
        return

class IntroState(GameState):
    """
    IntroState class
    
    Game state for showing introduction and choosing to continue or start new game
    """
    
    def __init__(self, screen, video):
        global screenSize
        self.cont=True
        self.movie = pygame.movie.Movie(video)
        self.screen = screen
        screenSize = [self.screen.get_rect()[2], self.screen.get_rect()[3]]
        videoplayer.play_vid(video)
        self.screen.fill((48, 64, 84))
        if pygame.font:
            font = pygame.font.Font(None, 36)
            self.newButton = objects.Button(screenSize[0]*0.2,screenSize[1]*0.8-10,screenSize[0]*0.6,screenSize[1]*0.2, 'New', False)
            self.loadButton = objects.Button(screenSize[0]*0.2,10 ,screenSize[0]*0.6,screenSize[1]*0.8-30, 'Load', True)
            self.newButtonSprite = pygame.sprite.RenderPlain(self.newButton)
            self.loadButtonSprite = pygame.sprite.RenderPlain(self.loadButton)
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                set_next_state(STATE_QUIT)
        pressed = pygame.key.get_pressed()
        if pressed[K_UP] or pressed[K_DOWN]:
            self.cont = not self.cont
            self.newButton.flip_select()
            self.loadButton.flip_select()
        elif pressed[K_RETURN]:
            if self.cont:
                set_next_state(STATE_LOAD)
            else:
                newStateObject = gamestateobjects.NewStateObject(self.screen)
                print newStateObject
                set_next_state(STATE_NEW, newStateObject)
    
    def update(self):
        self.newButtonSprite.update()
        self.loadButtonSprite.update()
    
    def render(self):
        self.newButtonSprite.draw(self.screen)
        self.loadButtonSprite.draw(self.screen)
        # return
        
    def close(self):
        return