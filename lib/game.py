import pygame
from pygame.locals import *
from common import *

class Game:
    
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_mode(WINDOW_SIZE, OPENGL | DOUBLEBUF | HWSURFACE)
        self.quit = False


    def change_scene(self, new_scene):
        self.scene = new_scene


    def main_loop(self, fps=30):

        while not self.quit:

            self._update_event()
            dt = self.clock.tick(fps)
            self.scene.update(dt)
            self.scene.render()
            pygame.display.flip()
        

    def _update_event(self):
        
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit = True
            elif e.type == KEYDOWN and e.key == K_q:
                self.quit = True
            elif e.type == KEYDOWN and e.key == K_f:
                self.fullscreen()
            else:
                self.scene.update_event(e)

    def fullscreen(self):
        pygame.display.toggle_fullscreen()
