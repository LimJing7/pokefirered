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
    
class GameStateObject:
    """
    GameStateObject class
    
    Contains current state of the game for passing between gamestates
    e.g. main map, battle screen, pokemon list, pc etc.
    """
    
    def __init__(self):
        return

class NewStateObject(GameStateObject):
    """
    NewStateObject class
    
    Contains the attributes for creating the new state object
    
    screen: screen for drawing to
    """
    def __init__(self, screen):
        self.screen = screen
    
    def __repr__(self):
        return "NewStateObject"

class MainStateObject(GameStateObject):
    """
    MainStateObject class
    
    Contains current state of the game for passing to other states
    
    screen: screen for drawing to
    map: mapObject
    player: playerObject
    
    #TODO
    location: location on current map 
    """
    
    def __init__(self, screen, map, player):
        self.screen = screen
        self.map = map
        self.player = player
        
    def __repr__(self):
        return "MainStateObject"
        
class BattleStateObject(GameStateObject):
    """
    BattleStateObject class
    
    Contains attributes describing the battle to occur
    
    trainer: boolean describing if it is a trainer battle
    count: number of pokemons
    pokemon_list: number of pokemon in the battle
    background: background to display during battle
    """
    
    def __init__(self, trainer, count, pokemon_list, background):
        self.trainer=trainer
        self.count=count
        self.pokemon_list=pokemon_list
        self.background=background
    
    def __repr__(self):
        return "BattleStateObject"