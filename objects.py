try:
    import sys
    import random
    import math
    import getopt
    import pygame
    from utilities import *
    from pygame.locals import *
except ImportError, err:
    print "Could not load module", err
    pygame.quit()
    sys.exit(1)
    
    
class AreaMap(pygame.sprite.Sprite):
    # TODO: Animated tiles?? Might not happen.
    # Make it actually read from files.
    
    """ AreaMap Class
        Handles the map displayed on the screen
        Note: coords are always (x,y) format, but array indexing is other way
        Methods:
        Attributes: """
    
    def __init__(self, mapData, viewSize, viewAnchor, screenCenter):

        """ Initialize the map
            Receives: data for the map (2d array), size of visible area in tiles (NOT TUPLE),
                      map coords of tile in top-left corner, center (on screen)
            Returns: Sets appropriate stuff """
        
        pygame.sprite.Sprite.__init__(self)

        self.mapData = mapData # Read from file.
        self.dimensions = (len(mapData[0]), len(mapData))
        self.viewAnchor = [viewAnchor[0], viewAnchor[1]] # CENTER VIEW ON PLAYER
        self.mapState = "stop"
        self.scrolling = 0
        self.viewSize = [viewSize[0], viewSize[1]] # VIEWSIZE MUST BE ODD!!!
        self.waitCount = 0
        self.__loadMapAssets()

        # self.image is slightly smaller than the actual self.imageFull,
        # which has additional rows to place the incoming rows/columns
        # during scrolling animations. All updates done to self.imageFull.
        tempSize = (viewSize[0]*TILE_WIDTH, viewSize[1]*TILE_HEIGHT)
        self.image = pygame.Surface(tempSize).convert()
        self.image.fill(BG_COLOR)

        tempSize = ((viewSize[0]+2)*TILE_WIDTH, (viewSize[1]+2)*TILE_HEIGHT)
        self.imageFull = pygame.Surface(tempSize).convert()
        self.imageFull.fill(BG_COLOR)
        
        self.rect = self.image.get_rect(center = screenCenter)

        # Construct visible portion of map
        for i in range(self.viewSize[1]):
            startCoords = (self.viewAnchor[0], self.viewAnchor[1]+i)
            tileArray = self.getRow(startCoords, self.viewSize[0])
            self.blitRow((1, i+1), tileArray)
        self.image.blit(self.imageFull, (-TILE_WIDTH, -TILE_HEIGHT))

    def __loadMapAssets(self):

        """ Loads the map assets into a list of surfaces
            Receives: none
            Returns: Populates self.mapAssets with tile images """
        
        self.mapAssets = []

        bg = pygame.Surface((TILE_WIDTH, TILE_HEIGHT)).convert()
        bg.fill(BG_COLOR)
        self.mapAssets.append(bg)
        self.mapAssets.append(load_png("red.png")[0])
        self.mapAssets.append(load_png("green.png")[0])
        self.mapAssets.append(load_png("blue.png")[0])
        self.mapAssets.append(load_png("yellow.png")[0])

        for i in range(len(self.mapAssets)):
            self.mapAssets[i] = pygame.transform.scale(self.mapAssets[i],
                                                       (TILE_WIDTH, TILE_HEIGHT))
    
    def getRow(self, start, tiles):

        """ Gets a specified row
            Receives: start coords, total tiles in row
            Returns: list containing tile types in row, -1 if failed
            Careful with -1 indices, which loop around in python"""

        try:
            return self.mapData[start[1]][start[0]:(start[0]+tiles)]
        except IndexError:
            return -1

    def blitRow(self, pos, tileArray):

        """ Blits a specified row onto self.imageFull
            Receives: start position on self.imageFull, tile array
            Returns: Blits the row """

        tileRect = pygame.Rect(pos[0]*TILE_WIDTH, pos[1]*TILE_HEIGHT,
                               TILE_WIDTH, TILE_HEIGHT)
        for tile in tileArray:
            self.imageFull.blit(self.mapAssets[tile], tileRect)
            tileRect.move_ip(TILE_WIDTH, 0)

    def getCol(self, start, tiles):

        """ Gets a specified column
            Receives: start coords, total tiles in col
            Returns: list containing tile types in col """

        try:
            return [self.mapData[i][start[0]]
                    for i in range(start[1], start[1]+tiles)]
        except IndexError:
            return -1

    def blitCol(self, pos, tileArray):

        """ Blits a specified col onto self.imageFull
            Receives: start __tile__ on self.imageFull, tile array
            Returns: Blits the column """

        tileRect = pygame.Rect(pos[0]*TILE_WIDTH, pos[1]*TILE_HEIGHT,
                               TILE_WIDTH, TILE_HEIGHT)
        for tile in tileArray:
            self.imageFull.blit(self.mapAssets[tile], tileRect)
            tileRect.move_ip(0, TILE_HEIGHT)

    def scroll(self, direction, frames = 10.0):

        """ Scrolls the map (direction of player movement)
            Does not scroll if already at max, or is already scrolling
            Receives: u/d/l/r, number of frames the animation takes
            Returns: Sets scrolling flag to [u/d/l/r, frames, 1/frames],
                     returns -1 if cannot move, 0 if currently moving, else 1 """

        if self.mapState != "stop" or frames == 0: return 0
        else:
            tempCoords = [self.viewAnchor[0], self.viewAnchor[1]]
            if direction == 'u':
                tempCoords[1] -= 1
                if tempCoords[1] < 0: return -1 # These are edge tests.
                tileArray = self.getRow(tempCoords, self.viewSize[0])
                self.blitRow((1, 0), tileArray)
                
            elif direction == 'd':
                tempCoords[1] += self.viewSize[1]
                if tempCoords[1] >= self.dimensions[1]: return -1
                tileArray = self.getRow(tempCoords, self.viewSize[0])
                self.blitRow((1, self.viewSize[1]+1), tileArray)
                
            elif direction == 'l':
                tempCoords[0] -= 1
                if tempCoords[0] < 0: return -1
                tileArray = self.getCol(tempCoords, self.viewSize[1])
                self.blitCol((0, 1), tileArray)
                
            elif direction == 'r':
                tempCoords[0] += self.viewSize[0]
                if tempCoords[0] >= self.dimensions[0]: return -1
                tileArray = self.getCol(tempCoords, self.viewSize[1])
                self.blitCol((self.viewSize[0]+1, 1), tileArray)

            # [direction of scroll, frames left in scroll, distance per frame]
            self.scrolling = [direction, frames, 1/frames]
            self.mapState = "scroll"

            return 1

    def isTraversable(self, coords):
        
        """ Checks if the player can stand on a map tile
            Receives: Coords of tile
            Returns: True/False """

        return True
            
    def update(self):

        """ Update the map sprite
            Receives: none
            Returns: Updates the sprite """

        # Scrolling the map
        if self.mapState == "scroll":
            tempImg = self.imageFull.copy()
            self.imageFull.fill(BG_COLOR)
            self.image.fill(BG_COLOR)
                
            self.scrolling[1] -= 1
            if self.scrolling[0] == 'u' or self.scrolling[0] == 'd':
                distance = self.scrolling[2]*TILE_HEIGHT
            else:
                distance = self.scrolling[2]*TILE_WIDTH
            
            if self.scrolling[0] == 'u':
                self.imageFull.blit(tempImg, (0, distance))
                if not self.scrolling[1]: self.viewAnchor[1] -= 1
            elif self.scrolling[0] == 'd':
                self.imageFull.blit(tempImg, (0, -distance))
                if not self.scrolling[1]: self.viewAnchor[1] += 1
            elif self.scrolling[0] == 'l':
                self.imageFull.blit(tempImg, (distance, 0))
                if not self.scrolling[1]: self.viewAnchor[0] -= 1
            elif self.scrolling[0] == 'r':
                self.imageFull.blit(tempImg, (-distance, 0))
                if not self.scrolling[1]: self.viewAnchor[0] += 1

            if not self.scrolling[1]:
                self.scrolling = 0
                self.mapState = "wait"
                self.waitCount = 5

            self.image.blit(self.imageFull, (-TILE_WIDTH, -TILE_HEIGHT))
            
        elif self.mapState == "wait":
            if self.waitCount > 1:
                self.waitCount -= 1
            else:
                self.waitCount = 0
                self.mapState = "stop"

    def debugMap(self):
        """ Such debug
            wow """
        print "dimensions:", self.dimensions
        print "viewAnchor:", self.viewAnchor
        print "mapState:", self.mapState
        print "scrolling:", self.scrolling
        print "waitCount:", self.waitCount
        print "viewSize:", self.viewSize
        print "rect:", self.rect
        print "-----------------------------------"

################################################################################

class Player(pygame.sprite.Sprite):
    # TODO: Player animations.

    """ Player class
        Handles the player sprite, and movement of map.
        Holds a reference to the map it is associated with. """

    def __init__(self, playerCoords, areaMap):

        """ Initializes the player
            Receives: map coordinates of player (NOT TUPLE), reference to associated map
            Returns: Initializes stuff """

        pygame.sprite.Sprite.__init__(self)
                
        self.playerState = "stop"
        self.playerCoords = [playerCoords[0], playerCoords[1]]
        self.areaMap = areaMap
        self.playerMove = 0
        self.mapMove = 0
        self.waitCount = 0

        self.image, self.rect = load_png("player.png", True)
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect.topleft = self.areaMap.rect.topleft
        diffCoords = (self.playerCoords[0]-self.areaMap.viewAnchor[0],
                      self.playerCoords[1]-self.areaMap.viewAnchor[1])
        self.rect.move_ip(diffCoords[0]*TILE_WIDTH, diffCoords[1]*TILE_HEIGHT)

        # Some calculation stuff
        self.tl = (self.areaMap.viewSize[0]/2, self.areaMap.viewSize[1]/2)
        self.br = (self.areaMap.dimensions[0]-self.tl[0]-1,
                   self.areaMap.dimensions[1]-self.tl[1]-1)
                   
        #player's bag
        self.pokeCount = 0
        self.poke = []
        
        

    def makeMove(self, direction, frames = 10.0):

        """ Moves the player, checking if the tile is traversable.
            Does not handle animations.
            Receives: Direction of travel, frames required for travel
            Returns: Sets self.playerMove to [direction, frames, 1/frames]
                     if player moving or self.mapMove = [direction, frames]
                     if only map moving. Returns 0 if playerState not stop,
                     -1 if cannot move, 1 otherwise """

        if frames == 0 or self.playerState != "stop": return 0

        dest = [self.playerCoords[0], self.playerCoords[1]]
        if direction == 'u': dest[1] -= 1
        elif direction == 'd': dest[1] += 1
        elif direction == 'l': dest[0] -= 1
        elif direction == 'r': dest[0] += 1

        if not self.areaMap.isTraversable(dest): return -1
        
        if dest[0] < 0 or dest[0] >= self.areaMap.dimensions[0] \
           or dest[1] < 0 or dest[1] >= self.areaMap.dimensions[1]:
            return -1

        self.playerState = "move"

        stationaryMap = False

        # Divides the map into nine regions: center, corners, sides and tests
        # whether the player or the map should be moving.
        if self.playerCoords[0] < self.tl[0] or self.playerCoords[0] > self.br[0]:
            if self.playerCoords[1] < self.tl[1] or self.playerCoords[1] > self.br[1]:
                # Corners, move player only
                stationaryMap = True
            elif direction == 'l' or direction == 'r':
                # Towards or away from wall, no need to move map
                stationaryMap = True
            elif dest[1] < self.tl[1] or dest[1] > self.br[1]:
                # Moving into a corner
                stationaryMap = True
        elif self.playerCoords[1] < self.tl[1] or self.playerCoords[1] > self.br[1]:
            if direction == 'u' or direction == 'd':
                stationaryMap = True
            elif dest[0] < self.tl[0] or dest[0] > self.br[0]:
                stationaryMap = True
        else:
            # Starts within the inner area
            if dest[0] < self.tl[0] or dest[0] > self.br[0] \
               or dest[1] < self.tl[1] or dest[1] > self.br[1]:
                stationaryMap = True
                
        if stationaryMap:
            self.mapMove = 0
            self.playerMove = [direction, frames, 1/frames] # Need to animate move
        else:
            self.areaMap.scroll(direction, frames)
            self.playerMove = 0
            self.mapMove = [direction, frames] # No need to move, map is scrolling

        return 1
            
    def update(self):

        """ Update the player sprite
            Receives: none
            Returns: updates the sprite """

        # Moving the player
        if self.playerState == "move":
            if self.playerMove:
                # Moving the player
                self.playerMove[1] -= 1
                if self.playerMove[0] == 'u' or self.playerMove[0] == 'd':
                    distance = self.playerMove[2]*TILE_HEIGHT
                else:
                    distance = self.playerMove[2]*TILE_WIDTH
    
                if self.playerMove[0] == 'u':
                    self.rect.move_ip(0, -distance)
                    if not self.playerMove[1]: self.playerCoords[1] -= 1
                elif self.playerMove[0] == 'd':
                    self.rect.move_ip(0, distance)
                    if not self.playerMove[1]: self.playerCoords[1] += 1
                elif self.playerMove[0] == 'l':
                    self.rect.move_ip(-distance, 0)
                    if not self.playerMove[1]: self.playerCoords[0] -= 1
                elif self.playerMove[0] == 'r':
                    self.rect.move_ip(distance, 0)
                    if not self.playerMove[1]: self.playerCoords[0] += 1
    
                if not self.playerMove[1]:
                    self.playerMove = 0
                    self.playerState = "wait"
                    self.waitCount = 5
                       
            elif self.mapMove:
                # Moving the map, player just stays there
                self.mapMove[1] -= 1
                if not self.mapMove[1]:
                    if self.mapMove[0] == 'u': self.playerCoords[1] -= 1
                    elif self.mapMove[0] == 'd': self.playerCoords[1] += 1
                    elif self.mapMove[0] == 'l': self.playerCoords[0] -= 1
                    elif self.mapMove[0] == 'r': self.playerCoords[0] += 1
                    self.mapMove = 0
                    self.playerState = "wait"
                    self.waitCount = 5

        elif self.playerState == "wait":
            # do absolutely nothing for a few frames
            if self.waitCount > 1:
                self.waitCount -= 1
            else:
                self.waitCount = 0
                self.playerState = "stop"
        
    def debugPlayer(self):
        """ So print
            many amaze """
        print "playerState:", self.playerState
        print "playerCoords:", self.playerCoords
        print "playerMove:", self.playerMove
        print "mapMove:", self.mapMove
        print "waitCount:", self.waitCount
        print "rect:", self.rect
        print "-----------------------------------"

class Button(pygame.sprite.Sprite):
    """
    A class to consolidate all the button attributes
    
    x,y: position of top left corner of button
    w,h: width and height of button
    text: text to displayed
    selected: boolean saying the button starts selected or not
    """
    
    def __init__(self, x, y, w, h, text, selected):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.text = text
        self.selected = selected
        self.color_list = [(216, 228, 228), (92, 96, 96)]
        self.text_color_list = [(56, 56, 56),(44, 44, 44)]
        if self.selected:
            self.color = 0
        else:
            self.color = 1
        self.image = pygame.Surface([w,h])
        self.image.fill(self.color_list[self.color])
        self.textSurf = self.font.render(self.text, 1, self.text_color_list[self.color])
        self.image.blit(self.textSurf, (10, 10))
        self.rect = pygame.Rect(x,y,w,h)
        self.waitCount = 0
        
        self.buttonState = 'still'
        
    def flip_select(self):
        if self.buttonState == 'still':
            self.selected = not self.selected
            self.buttonState = 'flip'
    
    def update(self):
        if self.buttonState == 'flip':
            self.color = (self.color+1)%2
            self.image.fill(self.color_list[self.color])
            self.textSurf = self.font.render(self.text, 1, self.text_color_list[self.color])
            self.image.blit(self.textSurf, (10, 10))
            self.buttonState = 'wait'
            self.waitCount = 5
            
        if self.buttonState == 'wait':
            # do absolutely nothing for a few frames
            if self.waitCount > 1:
                self.waitCount -= 1
            else:
                self.waitCount = 0
                self.buttonState = "still"