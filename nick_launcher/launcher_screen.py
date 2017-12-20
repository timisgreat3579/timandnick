import pygame,os,pygame.gfxdraw
os.environ['SDL_VIDEO_CENTERED'] = '1'
DGREY = (60,60,60)
SGREY = (70,70,70)
DDGREY = (40,40,40)
RED = (163, 27, 27)
WHITE = (255,255,255)
DWHITE = (200,200,200)
DDWHITE = (150,150,150)
class launcher():
    def __init__(self,screen):
        self.screen = screen
        self.w = self.screen.get_width()
        self.h = self.screen.get_height()
        self.frame_selected = None
        self.top_bar = pygame.Surface((self.w,self.h/8))
        self.top_bar = self.top_bar.convert()
        self.top_bar.set_colorkey(DDGREY)
        self.top_bar.fill(DDGREY)

        self.home_menu = main_frame(self.screen)

        self.library_menu = library_screen(self.screen)
        
        self.main_buttons = [button(self.top_bar,'HOME',parent_frame = self.home_menu),button(self.top_bar,'LIBRARY',parent_frame = self.library_menu),button(self.top_bar,'PROFILE'),button(self.top_bar,'COMMUNITY'),button(self.top_bar,'GLOBAL STATS')]
        for num,bu in enumerate(self.main_buttons):
            bu.x = self.main_buttons[num].rect.x = round(bu.w * (num))
            
    def draw(self,surface):
        if self.frame_selected is not None: self.frame_selected.draw(surface)
        surface.blit(self.top_bar,(0,0))
        for x in self.main_buttons:
            x.draw(surface)
        
    def check_buttons(self,surface,buttons):
        for x in buttons:
            if x.on_mouse_click():
                for z in buttons:
                    z.selected = False
                x.selected = True
                self.frame_selected = x.parent_frame

class main_frame():
    def __init__(self,parent):
        self.parent = parent
        self.w = self.parent.get_width()
        self.h = self.parent.get_height()/8*7
        self.x = self.w/20 * 19
        self.y = self.parent.get_height()/9
        self.scroll_y = 300
        
        self.display_screen = pygame.Surface((self.w,self.h))
        self.display_screen = self.display_screen.convert()
        self.display_screen.set_colorkey(DGREY)
        self.display_screen.fill(DGREY)
        
        
        self.scroll_bar_frame = pygame.Surface((self.w/70,self.h/1.3))
        self.scroll_bar_frame = self.scroll_bar_frame.convert()
        self.scroll_bar_frame.set_colorkey(SGREY)
        self.scroll_bar_frame.fill(SGREY)

        self.scroll_bar = pygame.Surface((self.w/70,self.h/5))
        self.scroll_bar = self.scroll_bar.convert()
        self.scroll_bar.set_colorkey(WHITE)
        self.scroll_bar.fill(WHITE)

        

    def draw(self,surface):
        surface.blit(self.display_screen,(0,self.parent.get_height()/9))
        
class library_screen(main_frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.side_bar = pygame.Surface((self.w/6,self.h))
        self.side_bar = self.side_bar.convert()
        self.side_bar.set_colorkey(WHITE)
        self.side_bar.fill(WHITE)

        self.game_buttons = [button(self.side_bar,'GAME1',size=(1,3),startpos=(0,0)),button(self.side_bar,'GAME2',size=(1,4),startpos=(0,0))
                             ,button(self.side_bar,'GAME3',size=(1,4),startpos=(0,0)),button(self.side_bar,'GAME4',size=(1,4),startpos=(0,0))]

        for num,bu in enumerate(self.game_buttons):
            bu.y = self.game_buttons[num].rect.y = round(bu.h * (num))
            
    def draw(self,surface):
        for x in self.game_buttons:
            x.draw(self.side_bar)
        self.scroll_bar_frame.blit(self.scroll_bar,(self.x,self.scroll_y))
        self.display_screen.blit(self.scroll_bar_frame,(self.x,(self.h - self.scroll_bar_frame.get_rect().h)/2))
        self.display_screen.blit(self.side_bar,(0,0))
        surface.blit(self.display_screen,(0,self.y))

class button():
    def __init__(self,parent,text = None,startpos=(50,0),size=(None,None), color = None, style= 'SQUARE',parent_frame = None):
        self.text = text
        self.parent = parent
        if color is None:
            self.color = self.parent.get_colorkey()
            print(self.color)
        else:
            self.color = color
        self.bold = False
        self.style = style
        self.parent_frame = parent_frame
        if self.parent_frame is not None: self.parent_frame = parent_frame
        if size[0] is None: self.w = round(self.parent.get_width()/5)
        else: self.w = round(self.parent.get_width()/size[0])
        if size [1] is None: self.h = round(self.parent.get_height() / 2.5)
        else: self.h =  round(self.parent.get_height()/size[1])
        self.x = startpos[0]
        self.y = startpos[1] + self.parent.get_height() - self.h
        
        self.surface = pygame.Surface((self.w,self.h))
        self.surface = self.surface.convert()
        self.surface.set_colorkey(self.color)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x ,self.rect.y = self.x,self.y

        self.selected = False
    def draw(self,target):
        self.font = pygame.font.SysFont('freesansbold',30,self.bold)
        if self.on_mouse_hover():
            self.text_surface = self.font.render(self.text,True,DWHITE)
            self.surface.set_colorkey(SGREY)
            self.surface.fill(SGREY)
        else:
            self.text_surface = self.font.render(self.text,True,DDWHITE)
            self.surface.set_colorkey(self.color)
            self.surface.fill(self.color)
        if self.selected:
           self.text_surface = self.font.render(self.text,True,WHITE)
           self.surface.set_colorkey(DDGREY)
           self.surface.fill(DDGREY)
        self.surface.blit(self.text_surface,((self.rect.w-self.text_surface.get_width())/2,(self.rect.h-self.text_surface.get_height())/2))
        target.blit(self.surface,(self.x,self.y))
    def on_mouse_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def on_mouse_click(self):
        return self.on_mouse_hover()

pygame.init()
screen = pygame.display.set_mode((1280,720),pygame.NOFRAME)
launch = launcher(screen)
while True:
    screen.fill(DGREY)
    launch.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            launch.check_buttons(screen,launch.main_buttons)
    
    pygame.display.flip()

