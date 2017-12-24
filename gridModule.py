# GRID MODULE BY TIM RUSCICA
#This module contains 5 classes (grid, menu, pixelArt, pixel,colorPallet)
#the grid class is the abstract/parent class, the pixelArt and menu class inherit from it.(they are childs)
#The color pallet class inherits from pixel art class as they both use similar methods.
#The pixel art and colorPallet class creates pixel objects to
#populate the grid, therfore they are dependant of pixel.
#------------------------------------------------------
#Class Descriptions are given above each class.
import pygame
pygame.init()

#Main abstract class (parent)
#This class is capable of creating a grid containing different rows and different columns, bases upon those arguments it
#will automatically alter the pixel size. To display the grid simply call ____.drawGrid(). To find the item in the grid
#that was clicked on call ____.clicked().
class grid(object):
    def __init__(self, win, width, height, cols, rows,showGrid=False, startx = 0, starty = 0, bg=(255,255,255)):
        self.font = pygame.font.SysFont('monospace', 15)
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.bg = bg
        self.startx = startx
        self.starty = starty
        self.showGrid = showGrid #If we should show the black outline
        self.grid = None
        self.lineThick = 1
        self.screen = win
        pygame.display.update()
                    
    def getGrid(self):
        return self.grid #Return the grid list

    def draw(self, lineColor=(0,0,0)): #This will draw the lines to create the grid, this is done so by simply creating overlapping boxes
        x = self.startx
        y = self.starty
        
        for i in range(self.cols):
            y = self.starty + self.height
            if i > 0:
                x += (self.width / self.cols)
            for j in range(self.rows):
                y -= self.height / self.rows 
                pygame.draw.rect(self.screen, lineColor,(x, y, self.width / self.cols, self.height/ self.rows), 1)

    def clicked(self, pos): #Return the position in the grid that user clicked on
        try:
            t = pos[0]
            w = pos[1]
            g1 = int((t - self.startx) / self.grid[0][0].w)
            g2 = int((w - self.starty) / self.grid[0][0].h)

            self.selected = self.grid[g1][g2]

            return self.grid[g1][g2]
        
        except IndexError: #If we run into an index error that means that the user did not click on a position in the grid
            return False


#This class creates basic grid menus that can contain text.
#It uses all of the methods from the parent grid class and is a concrete class
#The setText method takes a list of strings and displays them in the grid.
class menu(grid):
    def setText(self, textList): #The textList argument passed must be equal to the number of spots in the grid
        
        self.grid = []
        # Create textObjects in the grid
        for i in range(self.cols):
            self.grid.append([])
            for j in range(self.rows):
                self.grid[i].append(textObject(i, j, self.width, self.height, self.cols, self.rows, self.startx, self.starty, self.font))
        #Set the text for each of those objects
        c = 0
        for spots in self.getGrid():
            for s in spots:
                s.showText(self.screen, textList[c])
                c += 1

    def font(self, font, size):
        self.font = pygame.font.SysFont(font, size)
                 
#This class is responsible for displaying text and these objects are added into the grid.               
#The showText() method will display the text while the show() method will draw a square showing thr grid.
class textObject():
    def __init__(self, i, j, width, height, cols, rows, startx=0, starty=0, font=pygame.font.SysFont('monospace', 15)):
        self.font = font
        self.col = i #The column of the current instance in the grid
        self.row = j #The row of the current instance in the grid
        self.rows = rows #Total amount of rows
        self.cols = cols #Total amount of columns
        self.w = width / cols
        self.h = height / rows
        self.x = self.col * self.w + startx
        self.y = self.row * self.h + starty
        self.text = ''
    
    def showText(self, win, txt): #This will render and draw the text on the screen
        self.text = txt

        text = self.font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + (self.w /2 - text.get_width() / 2), self.y + (self.h/2 - text.get_height() / 2))) #This will make sure the text is center in the screen.

    def show(self, screen, color, st, outline=False): #Draws a square displaying the area in the grid  
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), st)


