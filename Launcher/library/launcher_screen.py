import pygame,os,pygame.gfxdraw,sys,os.path
from random import randint,randrange
from .loading_screen import buffer,session_var,user_login
from .leaderboard import Leaderboard
from .server_data import get_players,get_table_data


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((1280,720),pygame.NOFRAME)

buffer(screen,0,0,'AUTHENTICATING...',200).draw(screen)
pygame.display.flip()

DGREY = (60,60,60)
SGREY = (70,70,70)
DDGREY = (40,40,40)
RED = (163, 27, 27)
GREEN = (6, 114, 15)
WHITE = (255,255,255)
DWHITE = (200,200,200)
DDWHITE = (150,150,150)


class random_stars(object):
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = randint(1,10)
        self.opacity = randint(1,size) * 30 + randint(0,15)
        self.surf = pygame.Surface((size,size))
        self.surf.set_alpha(self.opacity)
        self.surf.fill(WHITE)
        
    def draw(self,surface):
        self.opacity += self.speed
        if self.opacity > 255:
            self.speed = randrange(-1,-10,-1)
        elif self.opacity < 0:
            self.speed = randint(1,10)
        surface.blit(self.surf,(self.x,self.y))
        self.surf.set_alpha(self.opacity)

def star_gaze(w,h,size):
    if h < 0:
        return []
    else:
        if w > 0:
            return [random_stars(randint(w-100,w),randint(h-100,h),randint(2,8))] + star_gaze(w-100,h,size)
        else:
            w = screen.get_width()
            return star_gaze(w,h-100,size) + [random_stars(randint(0,w),randint(h-100,h),randint(2,size))]

class surface_object():
    def __init__(self,w,h,x,y,color,alpha=255):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.surface = pygame.Surface((self.w,self.h))
        self.surface = self.surface.convert()
        self.surface.fill(self.color)
        self.surface.set_alpha(alpha)
    def set_color(self,color):
        self.surface.fill(color)

    def on_mouse_hover(self):
        return pygame.Rect(self.x,self.y,self.w,self.h).collidepoint(pygame.mouse.get_pos())

    def get_width(self):
        return self.w

    def get_height(self):
        return self.h

    def get_rect(self):
        return self.surface.get_rect(center=(self.x,self.y))

class popup_window_friend():
    def __init__(self):
        self.main_surface = surface_object(250,320,0,0,DGREY)
        self.top_bar = surface_object(self.main_surface.w,self.main_surface.h/6,self.main_surface.x,self.main_surface.y,DDGREY)
        self.brand_text = draw_text('',30,True,WHITE)
        self.current_window = None
        self.game_buttons = button_grouper(self.top_bar,['FRIENDS','REQUESTS'],button
                                           ,frames=[display_buttons('friends',1,self.main_surface.w,self.main_surface.h - self.main_surface.h/6,0,self.main_surface.h/6),None]
                                           ,pos=(0,round(self.top_bar.h-self.top_bar.h/2)),sizes=(0,self.top_bar.h/2),centerx = True)

        
    def draw(self,surface):
        self.main_surface.surface.blit(self.top_bar.surface,(self.top_bar.x,self.top_bar.y))
        surface.blit(self.main_surface.surface,(self.main_surface.x,self.main_surface.y))
        if self.current_window is not None:
            self.current_window.draw(surface)
        self.game_buttons.draw(surface)
        pygame.draw.rect(surface,WHITE,pygame.Rect(self.main_surface.x,self.main_surface.y,self.main_surface.w,self.main_surface.h),2)
    def check_drag(self):
        if pygame.Rect(self.main_surface.x,self.main_surface.y,self.main_surface.w,self.main_surface.h/6).collidepoint(pygame.mouse.get_pos()):
            self.main_surface.x,self.main_surface.y = pygame.mouse.get_pos()[0]+self.main_surface.x,pygame.mouse.get_pos()[1] +self.main_surface.y

class display_buttons():
    def __init__(self,index,types,w,h,x,y):
        self.type = types
        self.scroll_y = 0
        self.index = index
        self.scroll_bar_size = 0
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.background = surface_object(self.w,self.h,self.x,self.y,DGREY)
        self.scroll_bar_frame = surface_object(self.w/20,self.h/1.3,self.w - (self.w/20*2),(self.h - self.h/1.3)/2,SGREY)
        self.scroll_bar = surface_object(self.scroll_bar_frame.w,self.scroll_bar_size,self.w - (self.w/20*2),self.scroll_bar_frame.y + self.scroll_bar_size,WHITE)
        self.update_buttons()
    def draw(self,surface):
        if self.scroll_y < self.scroll_bar.y+(self.scroll_bar.h/2):
            self.scroll_y = self.scroll_bar.y+(self.scroll_bar.h/2)
        elif self.scroll_y > self.scroll_bar.y+self.scroll_bar_frame.h-self.scroll_bar_size + (self.scroll_bar.h/2):
            self.scroll_y = self.scroll_bar.y+self.scroll_bar_frame.h-self.scroll_bar_size + (self.scroll_bar.h/2)
        self.background.surface.blit(surface_object(1000,1000,self.x,self.y,DGREY).surface,(self.x,self.y))
        for i,x in enumerate(self.player_buttons):
            x.x,x.y=10,((i)*110+10)#-self.scroll_y
            x.draw(self.background.surface)
        self.background.surface.blit(self.scroll_bar_frame.surface,(self.scroll_bar_frame.x,(self.background.h - self.scroll_bar_frame.h)/2))
        surface.blit(self.background.surface,(self.x,self.y))
        surface.blit(self.scroll_bar.surface,(self.scroll_bar.x,self.scroll_bar.y))
    def update_buttons(self):
        self.player_buttons = []
        for i,x in enumerate(get_table_data('friends')):
            self.player_buttons.append(button(self.background.surface,x,center='LEFT',bold=True,font_size=40,color = DGREY
                                              ,startpos=(self.x+10,self.y+((i)*110+10)),size=(self.w/2.2,100)))

class launcher():
    def __init__(self,screen):
        self.screen = screen
        self.w = self.screen.get_width()
        self.h = self.screen.get_height()
        self.frame_selected = None
        self.game_screen = None
        self.leaderb_menu = None
        self.fr_menu = None
        self.top_bar = surface_object(self.w,self.h/8,0,0,DDGREY)
        self.enlarge = False
        self.friends_open = False
        self.brand_text = draw_text('TRNT v1.0',30,True,WHITE)

        self.user_text = draw_text('Welcome, ' + user.upper() +'!',17,False,WHITE)
        
        self.home_menu = main_frame(self.screen)
        self.library_menu = library_screen(self.screen)
        self.stats_menu = stats_screen(self.screen)
        self.profile_menu = profile_screen(self.screen)
        self.community_menu = community_screen(self.screen)
        self.main_buttons = button_grouper(self.top_bar,['HOME','LIBRARY','PROFILE','COMMUNITY','GLOBAL STATS']
                                           ,button,frames=[self.home_menu,self.library_menu,self.profile_menu,self.community_menu,self.stats_menu],pos=(0,self.top_bar.h/2),sizes=(0,self.top_bar.h/2),centerx = True)
        
        self.close_button = button(self.screen,'x',startpos=(self.top_bar.w-self.top_bar.w/25,0),size=(self.top_bar.w/25,self.top_bar.h/4),text_color=DDWHITE,color=DDGREY,font_size=15,bold = True)
        self.enlarge_button = button(self.screen,'□',startpos=(self.top_bar.w-self.top_bar.w/25-self.top_bar.w/25,0),size=(self.top_bar.w/25,self.top_bar.h/4),text_color=DDWHITE,color=DDGREY,font_size=15,bold = False)
        self.minimize_button = button(self.screen,'-',startpos=(self.top_bar.w-self.top_bar.w/25-self.top_bar.w/25-self.top_bar.w/25,0),size=(self.top_bar.w/25,self.top_bar.h/4),text_color=DDWHITE,color=DDGREY,font_size=16,bold = True)

        self.friends_button = button(self.screen,'FRIENDS',startpos=(self.top_bar.w-(self.top_bar.w/25*4),0),size=(self.top_bar.w/25,self.top_bar.h/4),text_color=DDWHITE,color=DDGREY,font_size=10,bold = True)

        ##FRIENDS WINDOW
        self.friends_window = popup_window_friend()
    def draw(self,surface):
        if self.frame_selected is not None:
            self.frame_selected.draw(surface)
            if isinstance(self.frame_selected,library_screen) and self.game_screen is not None:
                self.game_screen.draw(surface)                   
            if isinstance(self.leaderb_menu,Leaderboard) and self.leaderb_menu is not None and isinstance(self.frame_selected,stats_screen):
                self.leaderb_menu.draw()
            if isinstance(self.frame_selected,profile_screen) and self.fr_menu is not None:
                self.fr_menu.draw(surface)
            
        surface.blit(self.top_bar.surface,(self.top_bar.x,self.top_bar.y))
        self.main_buttons.draw(surface)
        surface.blit(self.brand_text.surface,(10,0))
        surface.blit(self.user_text.surface,(self.top_bar.w - self.user_text.width-(self.top_bar.w/25*5),0))
        self.close_button.draw(surface)
        self.enlarge_button.draw(surface)
        self.minimize_button.draw(surface)
        self.friends_button.draw(surface)
        if self.friends_open:
            self.friends_window.draw(surface)
    def check_buttons(self):
        self.frame_selected = self.main_buttons.check_event(self.frame_selected)
        self.game_screen = self.library_menu.game_buttons.check_event(self.game_screen)
        self.leaderb_menu = self.stats_menu.select_scores.check_event(self.leaderb_menu)
        self.fr_menu = self.profile_menu.select_scores.check_event(self.fr_menu)
        self.friends_window.current_window = self.friends_window.game_buttons.check_event(self.friends_window.current_window)
        if isinstance(self.frame_selected,community_screen):
            if self.community_menu.refresh_button.on_mouse_click():
                buffer(self.community_menu.players_box,self.community_menu.players_box.x
                       ,self.community_menu.players_box.y + self.community_menu.display_screen.y,'WAITING').draw(surf = self.screen)
                self.community_menu.update_buttons()
        if isinstance(self.frame_selected,stats_screen):
            if self.stats_menu.refresh_button.on_mouse_click():
                buffer(self.stats_menu.leader_board_display,self.stats_menu.leader_board_display.x,self.stats_menu.leader_board_display.y + self.stats_menu.display_screen.y,'WAITING').draw(surf = self.screen)
                for i in self.stats_menu.select_scores.frames:
                    i.update()
        if isinstance(self.frame_selected,library_screen) and self.game_screen is not None:
            game_directory = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
            game_directory = os.path.abspath(os.path.join(leader_dir, '..'))
            game_directory = os.path.join('Games/'+self.game_screen.name)
            sys.path.append(game_directory)
            if self.game_screen.name == 'quicktype' and self.game_screen.play_button.on_mouse_click():
                
            elif self.game_screen.name == 'integerrecall' and self.game_screen.play_button.on_mouse_click():

            elif self.game_screen.name == 'golfgame' and self.game_screen.play_button.on_mouse_click():
                
        if self.minimize_button.on_mouse_click():
            pygame.display.iconify()
        if self.close_button.on_mouse_click():
            pygame.quit()
            raise SystemExit
        if self.friends_button.on_mouse_click():
            if self.friends_open:
                self.friends_open = False
            else:
                self.friends_open = True
        if self.enlarge_button.on_mouse_click():
            if self.enlarge:
                screen = pygame.display.set_mode((1280,720),pygame.NOFRAME)
                self.enlarge = False
            else:
                screen = pygame.display.set_mode((1920,1080),pygame.NOFRAME)
                self.enlarge = True
       
    def check_scroll(self):
     if isinstance(self.frame_selected,library_screen):
        for x in self.library_menu.game_buttons.frames:
            if x is not None:
                if x.scroll_bar.on_mouse_hover():
                    x.scroll_y = pygame.mouse.get_pos()[1]
                    
class main_frame():
    def __init__(self,parent):
        self.parent = parent
        self.w = self.parent.get_width()
        self.h = self.parent.get_height()/8*7
        self.x = self.parent.get_width()/8
        self.y = self.parent.get_height()/8
        self.scroll_y = 0

        self.display_screen = surface_object(self.w,self.h,0,self.y,DGREY)

        self.scroll_bar_frame = surface_object(self.w/70,self.h/1.3,self.x*7.5,(self.h - self.h/1.3)/2,SGREY)

        self.scroll_bar = surface_object(self.scroll_bar_frame.w,50,self.scroll_bar_frame.x+self.display_screen.x+self.scroll_bar_frame.w+2,163,WHITE)
        
    def draw(self,surface):
        surface.blit(self.display_screen.surface,(self.display_screen.x,self.display_screen.y))
        
class library_screen(main_frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.side_bar = surface_object(self.display_screen.w/6,self.display_screen.h,0,0,DGREY)
        self.game_buttons = button_grouper(self.side_bar,['QUICKTYPE','INTEGER RECALL','GOLF GAME'],button
                                           ,frames=[game_frame(self.parent,'quicktype','quicktype'),game_frame(self.parent,'integerrecall','integerrecall'),game_frame(self.parent,'golfgame','golfgame')],pos=(0,self.display_screen.y),sizes=(self.side_bar.w,0),centery = True)
        self.stars  = star_gaze(self.display_screen.w,self.display_screen.h,7)
    def draw(self,surface):
        #self.scroll_bar_frame.surface.blit(self.scroll_bar.surface,(self.scroll_bar_frame.x,self.scroll_bar.y))
        #self.display_screen.surface.blit(self.scroll_bar_frame.surface,(self.scroll_bar_frame.x,(self.display_screen.h - self.scroll_bar_frame.h)/2))
        self.display_screen.surface.blit(self.side_bar.surface,(0,0))
        surface.blit(self.display_screen.surface,(0,self.display_screen.y))
        for x in self.stars:
            x.draw(surface)
        self.game_buttons.draw(surface)
        
class draw_text():
    def __init__(self,text,font_size,bold,color):
        self.text = text
        self.font_size = font_size
        self.bold = bold
        self.color = color
        self.font = pygame.font.SysFont('tahoma',self.font_size,self.bold)
        self.surface = self.font.render(self.text,True,self.color)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()     
  
class game_frame(main_frame):
    def __init__(self,parent,name,to_run):
        super().__init__(parent)
        self.move_val = 0
        self.name = name
        self.display_screen = surface_object(self.w-self.w/6,self.h,self.w/6,self.y,DGREY)
        self.display_screen.surface.set_alpha(220)
        self.bg_picture = surface_object(self.display_screen.w/1.2,400,(self.display_screen.w - self.display_screen.w/1.2)/2,100,DDGREY)
        self.bg_leader = surface_object(self.display_screen.w/1.2,400,(self.display_screen.w-self.display_screen.w/1.2)/2,650-(self.scroll_y-163),DDGREY)
        self.bg_title = surface_object(self.display_screen.w/1.2,50,(self.display_screen.w-self.display_screen.w/1.2)/2,10-self.move_val,DDGREY)
        self.game_text = draw_text(name.upper(),40,True,WHITE)

        self.led_bg = surface_object(self.display_screen.w/1.2,50,(self.display_screen.w-self.display_screen.w/1.2)/2,600-self.move_val,DDGREY)
        self.led_text = draw_text('LEADERBOARDS',35,True,WHITE)
        
        self.scroll_bar_frame = surface_object(self.w/70,self.h/1.3,self.x*6.3,(self.h - self.h/1.3)/2,SGREY)
        self.play_button = button(self.display_screen,'PLAY',text_color=WHITE,bold=True,font_size=60,startpos = ((self.display_screen.w+self.display_screen.w/15)/2,570-(self.scroll_y-163)),size=(self.display_screen.w/3,80),color=GREEN)
        self.image = pygame.image.load('materials/'+name+'.png')
        self.image = pygame.transform.scale(self.image,(int(self.bg_picture.w),int(self.bg_picture.h+190)))

        self.quicktype_scores = Leaderboard(user,name,'friends',parent,self.bg_leader.w,self.bg_leader.h
                                                   ,self.bg_leader.x,self.bg_leader.y,True)
    def draw(self,surface):
        if self.scroll_y < 163+(self.scroll_bar.h/2):
            self.scroll_y = 163+(self.scroll_bar.h/2)
        elif self.scroll_y > 596+(self.scroll_bar.h/2):
            self.scroll_y = 596+(self.scroll_bar.h/2)
        self.display_screen.surface.blit(surface_object(1000,1000,0,0,DGREY).surface,(0,0))
        self.bg_picture.surface.blit(self.image,(0,0))
        self.display_screen.surface.blit(self.bg_picture.surface,(self.bg_picture.x,90-(self.scroll_y-163)))
        self.display_screen.surface.blit(self.bg_title.surface,((self.display_screen.w-self.display_screen.w/1.2)/2,30-(self.scroll_y-163)))
        self.display_screen.surface.blit(self.game_text.surface,((self.display_screen.w-self.game_text.width)/2,30-(self.scroll_y-163)))
        self.display_screen.surface.blit(self.bg_leader.surface,((self.display_screen.w-self.bg_leader.w)/2,650-(self.scroll_y-163)))

        self.display_screen.surface.blit(self.led_bg.surface,((self.display_screen.w-self.display_screen.w/1.2)/2,590-(self.scroll_y-163)))
        self.display_screen.surface.blit(self.led_text.surface,((self.display_screen.w-self.led_text.width)/2,590-(self.scroll_y-163)))
        
        self.display_screen.surface.blit(self.scroll_bar_frame.surface,(self.scroll_bar_frame.x,(self.display_screen.h - self.scroll_bar_frame.h)/2))
        self.play_button.y=self.play_button.surface.y = 590-(self.scroll_y-163)
        self.play_button.draw(self.display_screen.surface,custom=True)
        surface.blit(self.display_screen.surface,(self.display_screen.x,self.display_screen.y))
        self.quicktype_scores.x,self.quicktype_scores.y = (self.display_screen.w-self.bg_leader.w)/2+self.display_screen.x,650-(self.scroll_y-163)+self.display_screen.y
        self.quicktype_scores.draw()
        
        self.scroll_bar.y = self.scroll_y-(self.scroll_bar.h/2)
        surface.blit(self.scroll_bar.surface,(self.scroll_bar.x,self.scroll_bar.y))
        
class profile_screen(main_frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.select_bar = surface_object(self.display_screen.w/1.5,self.display_screen.h/14,round((self.display_screen.w - self.display_screen.w/1.5 )/2),10,DGREY)
        self.select_scores = button_grouper(self.select_bar,['PROFILE','FRIENDS','REQUESTS'],button
                                            ,frames=[None,friends_screen(parent),None],pos=(0,self.display_screen.y+self.select_bar.y)
                                            ,sizes=(0,self.select_bar.h),centerx = True,style=1)
        self.refresh_button = button(self.display_screen,'REFRESH',startpos = ((self.display_screen.w-200)/2,self.display_screen.h+27),size=(200,50))
    def draw(self,surface):
        self.display_screen.surface.blit(self.select_bar.surface,(self.select_bar.x,self.select_bar.y))
        surface.blit(self.display_screen.surface,(0,self.display_screen.y))
        self.select_scores.draw(surface)
        self.refresh_button.draw(surface)
        
class scroll_b():
    def __init__(self,parent):
        self.parent = parent
        self.scroll = surface_object(self.parent.w,0,self.parent.x,0,WHITE)

    def check_scroll(self):
        mx,my = pygame.mouse.get_pos()
       # if

    def on_mouse_hover(self):
        return pygame.Rect(self.scroll.x,self.scroll.y,self.scroll.w,self.scroll.h).collidepoint(pygame.mouse.get_pos())

class friends_screen(main_frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.player_buttons = []
        self.players_box = surface_object(self.w/2,self.h/1.2,(self.display_screen.w-self.w/2)/2,self.display_screen.h/7,DDGREY)
        
    def draw(self,surface):
        print(self.player_buttons)
        self.players_box.surface.blit(surface_object(1000,1000,0,0,DDGREY).surface,(0,0))
        self.update_buttons()
        for i,x in enumerate(self.player_buttons):
            x.x,x.y=10,((i)*110+10)
            x.draw(self.players_box.surface)
        self.players_box.surface.blit(self.scroll_bar_frame.surface,(self.players_box.w/4*3.8,(self.players_box.h-self.scroll_bar_frame.h)/2))
        self.display_screen.surface.blit(self.players_box.surface,(self.players_box.x,self.players_box.y))
        surface.blit(self.display_screen.surface,(self.display_screen.x,self.display_screen.y))
        
    def update_buttons(self):
        self.player_buttons = []
        for i,x in enumerate(get_table_data('friends')):
            self.player_buttons.append(button(self.players_box.surface,x,center='LEFT',bold=True,font_size=40,color = DGREY,startpos=(self.search_bg.x+10,self.display_screen.h/3.5+((i)*110+10)),size=(self.w/2.2,100)))
            
class community_screen(main_frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.search_text = []
        self.player_buttons = []
        self.clicked_player = None
        self.search_bg = surface_object(self.w/2,50,(self.display_screen.w-self.w/2)/2,self.display_screen.h/20,DDGREY)
        self.text = draw_text('SEARCH:',30,True,WHITE)
        self.players_box = surface_object(self.w/2,self.h/1.2,(self.display_screen.w-self.w/2)/2,self.display_screen.h/7,DDGREY)
        self.refresh_button = button(self.display_screen,'FIND',startpos = (self.search_bg.x + self.search_bg.w-105,self.display_screen.h/5),size=(100,40),color=DGREY)
    def draw(self,surface):
        
        self.c_text = draw_text(''.join(self.search_text),30,False,WHITE)
        self.players_box.surface.blit(surface_object(1000,1000,0,0,DDGREY).surface,(0,0))
        for i,x in enumerate(self.player_buttons):
            x.x,x.y=10,((i)*110+10)
            x.draw(self.players_box.surface)
        self.players_box.surface.blit(self.scroll_bar_frame.surface,(self.players_box.w/4*3.8,(self.players_box.h-self.scroll_bar_frame.h)/2))
        self.display_screen.surface.blit(self.players_box.surface,(self.players_box.x,self.players_box.y))
        self.display_screen.surface.blit(self.search_bg.surface,(self.search_bg.x,self.search_bg.y))
        surface.blit(self.display_screen.surface,(self.display_screen.x,self.display_screen.y))
        surface.blit(self.text.surface,(self.search_bg.x+10,self.display_screen.h/5))
        surface.blit(self.c_text.surface,(self.search_bg.x+150,self.display_screen.h/5))
        self.refresh_button.draw(surface)
    def update_buttons(self):
        self.player_buttons = []
        for i,x in enumerate(get_players(''.join(self.search_text))):
            self.player_buttons.append(button(self.players_box.surface,x,center='LEFT',bold=True,font_size=40,color = DGREY,startpos=(self.search_bg.x+10,self.display_screen.h/3.5+((i)*110+10)),size=(self.w/2.2,100)))
            
class stats_screen(main_frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.select_bar = surface_object(self.display_screen.w/1.5,self.display_screen.h/14,round((self.display_screen.w - self.display_screen.w/1.5 )/2),10,DGREY)
        self.leader_board_display = surface_object(self.display_screen.w/1.3,self.display_screen.h/1.3,round((self.display_screen.w - self.display_screen.w/1.3 )/2),(self.display_screen.h-self.display_screen.h/1.3)/2,DDGREY)
        self.scroll_bar_frame = surface_object(self.w/70,self.h/1.55,self.x*7.5,(self.h - self.h/1.55)/2,SGREY)
        self.refresh_button = button(self.display_screen,'REFRESH',startpos = ((self.display_screen.w-200)/2,self.display_screen.h+27),size=(200,50))
        quicktype_scores = Leaderboard(user,'quicktype','global',parent,self.leader_board_display.w,self.leader_board_display.h
                                                   ,self.leader_board_display.x,self.h/3.9,True)

        integer_scores = Leaderboard(user,'integerrecall','global',parent,self.leader_board_display.w,self.leader_board_display.h
                                                   ,self.leader_board_display.x,self.h/3.9,True)

        golf_scores = Leaderboard(user,'golf','global',parent,self.leader_board_display.w,self.leader_board_display.h
                                                   ,self.leader_board_display.x,self.h/3.9,True)
        self.select_scores = button_grouper(self.select_bar,['QUICKTYPE','INTEGER RECALL','GOLF GAME'],button,frames=[quicktype_scores,integer_scores,golf_scores],pos=(0,self.display_screen.y+self.select_bar.y),sizes=(0,self.select_bar.h),centerx = True,style=1)
    def draw(self,surface):
        self.display_screen.surface.blit(self.select_bar.surface,(self.select_bar.x,self.select_bar.y))
        #self.leader_board_display.surface.blit(self.scroll_bar_frame.surface,(self.leader_board_display.w/4*3.8,(self.leader_board_display.h-self.scroll_bar_frame.h)/2))
        self.display_screen.surface.blit(self.leader_board_display.surface,(self.leader_board_display.x,self.leader_board_display.y))
        surface.blit(self.display_screen.surface,(0,self.display_screen.y))
        self.select_scores.draw(surface)
        self.refresh_button.draw(surface)
        
class button():
    def __init__(self,parent,text = None,startpos=(0,0),size=(None,None),text_color=DDWHITE, color = None, style= 0 ,parent_frame = None,font_size=20,bold = False,center='CENTER'):
        self.text = text
        self.parent = parent
        self.startpos = startpos
        if color is None:
            self.color = DDGREY
        else:
            self.color =  color
        self.bold = bold
        self.center = center
        self.font_size = font_size
        self.style = style
        self.parent_frame = parent_frame
        if self.parent_frame is not None: self.parent_frame = parent_frame
        self.w = size[0]
        self.h = size[1]
        self.x = startpos[0]
        self.y = startpos[1]
        self.text_color = text_color
        self.style = style
        self.surface = surface_object(self.w,self.h,self.x,self.y,self.color)
        self.selected = False
    def draw(self,target,custom=False):
        self.font = pygame.font.SysFont('tahoma',self.font_size,self.bold)
        if self.on_mouse_hover():
            self.text_surface = self.font.render(self.text,True,DWHITE)
            self.surface.set_color(SGREY)
        else:
            self.text_surface = self.font.render(self.text,True,self.text_color)
            self.surface.set_color(self.color)
        if self.selected:
            self.text_surface = self.font.render(self.text,True,WHITE)
            self.surface.set_color(DGREY)
        if self.center == 'CENTER':
            self.center = (self.surface.w-self.text_surface.get_width())/2
        elif self.center == 'RIGHT':
            self.center = self.surface.w-self.text_surface.get_width()
        elif self.center == 'LEFT':
            self.center = self.surface.w/20
            
        self.surface.surface.blit(self.text_surface,(self.center,(self.surface.h-self.text_surface.get_height())/2))
        if custom:
            target.blit(self.surface.surface,(self.x-self.parent.x,self.y-self.parent.y))
        else:
            target.blit(self.surface.surface,(self.x,self.y))
        if self.style ==1 and self.selected:
            pygame.draw.rect(target,WHITE,pygame.Rect(self.surface.x,self.surface.y,self.surface.w,self.surface.h),2)
    def on_mouse_hover(self):
        return pygame.Rect(self.surface.x,self.surface.y,self.surface.w,self.surface.h).collidepoint(pygame.mouse.get_pos())
    def on_mouse_click(self):
        return self.on_mouse_hover()
    
class button_grouper():
    def __init__(self,parent,texts,button_type,sizes=(0,0),pos=(0,0),centerx = False,centery = False,frames=[None,None,None,None],offset=(0,0),style=0,gap=10):
        self.parent = parent
        self.pos = pos
        self.texts = texts
        self.button_type = button_type
        self.centerx = centerx
        self.centery = centery
        self.amount = len(texts)
        self.button_list = []
        self.frames = frames
        for num,text in enumerate(texts):
            x,y=self.pos
            w,h=sizes
            if centerx:
                x = round(((self.parent.w-gap*(self.amount-1))/self.amount+gap) * (num) +self.parent.x + self.pos[0])
                w = round(((self.parent.w-gap*(self.amount-1))/self.amount))
            elif centery:
                y = round(((self.parent.h-gap*(self.amount-1))/self.amount+gap) * (num) + self.parent.y + self.pos[1])
                h = round(((self.parent.h-gap*(self.amount-1))/self.amount))
            else:
                x,y=self.pos
            self.button_list.append(self.button_type(self.parent,text,size=(int(w),int(h)),startpos=(x,y),parent_frame=frames[num],style=style))
                
    def draw(self,surface):
        for x in self.button_list:
            x.draw(surface)

    def check_event(self,p_frame):
        for z in self.button_list:
            if z.on_mouse_click():
                for c in self.button_list:
                    c.selected = False
                z.selected = True
                return z.parent_frame
        return p_frame

session = session_var
user = user_login
launch = launcher(screen)

while True:
    screen.fill((0,0,0))
    launch.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            launch.check_buttons()
        elif event.type == pygame.KEYDOWN:
            if isinstance(launch.frame_selected,community_screen):
                if event.key == pygame.K_BACKSPACE:
                    if len(launch.community_menu.search_text) > 0:
                        del launch.community_menu.search_text[-1]
                elif len(launch.community_menu.search_text) < 25:
                    launch.community_menu.search_text.append(chr(event.key))
        if pygame.mouse.get_pressed()[0]:
            launch.check_scroll()
    pygame.display.update()

