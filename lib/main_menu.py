import pygame
from pygame.locals import *
from menu import Menu
from scene import Scene
import qgl

class MainMenu(Scene):
    
    def __init__(self, world):
        Scene.__init__(self, world)

        items = [
                 ("Start new game", self.on_new_game),
                 ("Credits", self.on_credits),
                 ("Quit", self.on_quit),
                 ]

        self.menu = Menu(self, items)


    def update(self):
        self.menu.update()


    def update_event(self, event):
        self.menu.update_event(event)


    # Handlers 

    def on_new_game(self):
        print "Ha seleccionado 'new game'"

    def on_credits(self):
        print "Ha seleccionado 'credits'"

    def on_quit(self):
        print "Ha seleccionado 'quit'"
