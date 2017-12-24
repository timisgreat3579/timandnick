# Game 1 Reaction Time Game, A letter shows up and you have to click the key
# on the keyboard

import pygame
import time
import random
from gridModule import menu

pygame.init()

right = 0
wrong = 0
tries = 0
totalTime = 0
last = ''

startfont = pygame.font.SysFont("monospace", 60)
startfont1 = pygame.font.SysFont("monospace", 85)
myfont = pygame.font.SysFont("monospace", 150)
displayFont = pygame.font.SysFont("monospace", 30)

w_width = 1000
w_height = 600


class leaderboard(object):
    def __init__(self, game, type, win , width, height, x, y):
        #game is to allow us to determine what game leaderboard we need to get
        #type is either freind or global
        self.win = win
        self.width = width
        self.height = height
        self.cols = 2
        self.rows = 5
        self.x = x
        self.y = y
        self.text = []
        pass

    def setup(self):
        self.grid = menu(self.win, self.width, self.height, self.cols, self.rows, self.showGrid, self.x, self.y)

    def draw(self):
        self.grid.draw((255, 255, 255))

    def font(self, font, size):
        self.grid.font(font, size)

    def update(self):
        self.text = []
        self.display(self.win, self.width, self.height, self.cols, self.rows, self.showGrid, self.x, self.y)
        pass

    def getFriends(self):
        pass

    def getGlobal(self):
        pass


class button(object):
    def __init__(self, text, textSize, width, height, color):
        self.text = text
        self.width = width
        self.height = height
        self.original = color
        self.color = self.original
        self.x = 0
        self.y = 0
        self.isHover = True
        self.fontSize = textSize
        self.textColor = (255,255,255)

    def draw(self, surface, x, y):
        self.x = x
        self.y = y
        font = pygame.font.SysFont("monospace", self.fontSize)
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color, (self.x+2, self.y+2, self.width-4, self.height-4))
        text = font.render(self.text, 1, self.textColor)
        surface.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def hover(self, surface):
        if not self.isHover:
            self.color = (round(self.color[0]*(3/4)), round(self.color[1]*(3/4)), round(self.color[2]*(3/4)))
        self.draw(surface, self.x, self.y)
        self.isHover = True

    def isMouseOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        else:
            return False

    def update(self, surface):
        self.isHover = False
        self.color = self.original
        self.draw(surface, self.x, self.y)

    def textColor(self, color):
        self.textColor = color


def update():
    global time1, totalTime
    pygame.draw.rect(win, (0,0,0), (0,0,w_width,100))
    totalTime = time.time() - time1
    label = displayFont.render('Time: ' + str(round(totalTime,2)),1,(255,255,255))
    win.blit(label,(10,10))
    label = displayFont.render('Remaining: ' + str(26 - tries),1,(255,255,255))
    win.blit(label, (w_width - 20 - label.get_width(),10))
    label = displayFont.render('Correct: ' + str(right),1,(0,255,0))
    win.blit(label, (w_width-38-label.get_width(),40))
    label = displayFont.render('Incorrect: ' + str(wrong),1,(255,0,0))
    win.blit(label, (w_width - 37 - label.get_width(),70))
    label = displayFont.render('+' + str(2.5*wrong) + 's', 1, (255,0,0))
    win.blit(label, (220, 10))
    pygame.display.update()

def showLetter():
    global last
    letter = generateKey()
    while letter == last:
        letter = generateKey()
    last = letter
    label = myfont.render(letter, 1, (255,255,255))
    win.blit(label, (random.randrange(100,w_width - 100 - label.get_width()), random.randrange(100,w_height-label.get_height())))
    pygame.display.update()
    return letter
    
def correct():
    global right
    right += 1

def incorrect():
    global wrong
    wrong += 1

def generateKey():
    r = random.randrange(0,26)
    return chr(65 + r)

def startCount():
    win.fill((0,0,0))
    label = myfont.render('3',1,(255,255,255))
    win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)
    win.fill((0,0,0))
    label = myfont.render('2',1,(255,255,255))
    win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)
    win.fill((0,0,0))
    label = myfont.render('1',1,(255,255,255))
    win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)


def endScreen():
    global totalTime
    totalTime += 2.5 * wrong
    if tries == 26:
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    pygame.quit()


def showInfoScreen():
    global win
    pass


def start():
    global win

    win = pygame.display.set_mode((w_width, w_height))
    pygame.display.set_caption('Quick Type')
    title = startfont1.render('Quick Type',1,(255,255,255))

    startBtn = button('Start Game', 30, 250, 50, (40,40,40))
    infoBtn = button('Learn to Play', 30, 250, 50, (40,40,40))
    btns = [startBtn, infoBtn]
    run = True
    while run:
        pygame.time.delay(100)
        win.fill((0,0,0))
        win.blit(title, (w_width / 2 - title.get_width() / 2, 10))
        startBtn.draw(win, 175, w_height - 80)
        infoBtn.draw(win, w_width - 425, w_height - 80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.isMouseOver(pos):
                        btn.hover(win)
                    else:
                        btn.update(win)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if startBtn.isMouseOver(pos):
                    run = False
                elif infoBtn.isMouseOver(pos):
                    showInfoScreen()
        pygame.display.update()

    win.fill((0,0,0))
    pygame.display.update()
    main()


def main():
    global time1, tries, right, wrong, totalTime, win

    play = True
    time1 = 0
    while play:
        label = startfont.render('Press Any Key to Begin...', 1, (255,255,255))
        win.blit(label, (w_width/2 - label.get_width()/2,w_height/2-label.get_height()/2))
        pygame.display.update()
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                startCount()
                update()
                totalTime = 0
                tries = 0
                right = 0
                wrong = 0
                time1 = time.time()
                while tries < 26:
                    tries += 1
                    win.fill((0,0,0))
                    correctKey = showLetter()
                    gameLoop = True
                    while gameLoop:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameLoop = False
                                tries = 100
                                play = False
                            if event.type == pygame.KEYDOWN:
                                pressed = pygame.key.get_pressed()
                                for i in range(len(pressed)):
                                    if pressed[i] == 1:
                                        usrPressed = pygame.key.name(i)

                                if usrPressed.lower() == correctKey.lower():
                                    correct()
                                else:
                                    incorrect()
                                gameLoop = False
                        update()
                endScreen()
    pygame.quit()


start()
