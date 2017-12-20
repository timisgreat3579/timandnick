import pygame,os
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
#if pygame.QUIT in pygame.event.get(): pygame.quit();raise SystemExit;

class load_screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((640,350),pygame.NOFRAME)
        self.draw()
    def draw(self):
        self.screen.fill((0,0,0))
        pygame.display.flip() 

class buffer():
    def __init__(self,surface,default_text=''):
        self.load_text = pygame.font.SysFont('Arial',50,True)
        self.default_text= default_text
        self.load_additive = self.default_text
        self.screen = surface
        self.background = pygame.Surface((surface.get_width(),surface.get_height()))
        self.background.fill((50,50,50))
        self.background.set_alpha(200)
    def draw(self):
        self.load_additive += '.'
        if len(self.load_additive) > 3:
            self.load_additive = self.default_text
        self.text_surface = self.load_text.render(self.load_additive,True,(255,255,255))
        self.screen.blit(self.background,(0,0)) 
        self.screen.blit(self.text_surface,((self.background.get_width() - self.text_surface.get_width())/2
                                               ,(self.background.get_height() - self.text_surface.get_height())/2))
        


if __name__ == '__main__':
    buffer(load_screen().screen,'LOADING').draw()
    pygame.display.flip()
    import getpip
    import pip
    pip.main(['install','boto3'])
    pygame.quit()
    import launcher_screen

