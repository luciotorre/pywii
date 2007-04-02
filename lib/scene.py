import qgl
from common import *
import pygame #for events
from pygame.event import Event, post

class NotImplementedError(Exception):
    pass

EV_HANDLER_ACTIVE, EV_HANDLER_PASSIVE, EV_PUSH_HANDLER, EV_POP_HANDLER = range(4)

class EventHandler:
    def handle_event(self, event):
        raise NotImplementedError("You must overwrite this method.")        
    def __init__(self):
        self.parent=None
        
    @property
    def lastClick(self):
        if self.parent is None:
            return None
        return self.parent.getLastClick()
        
    def set_parent(self, xparent):
        self.parent=xparent
    def push_handler(self, handler):
        post(Event(USEREVENT, code=EV_PUSH_HANDLER, handler=handler))
    def pop_handler(self):
        post(Event(USEREVENT, code=EV_POP_HANDLER)) 
        
class clickHandler(EventHandler):
    def handle_event(self, event):
        if event.type is MOUSEBUTTONDOWN:
            self.event = event
            self.pop_handler()
            
class twoClicks(EventHandler):
    def run(self):
        raise NotImplementedError("You must overwrite this method.")  
    def __init__(self):
        EventHandler.__init__(self)
        self.click1 = None
        self.click2 = None
    def handle_event(self, event):
        if self.click1 is None:
            self.click1 = clickHandler()
            self.click1.event = self.lastClick
        if event.type is USEREVENT:
            if event.code is EV_HANDLER_ACTIVE:
                if self.click2 is None:
                    self.click2 = clickHandler()
                    self.push_handler(self.click2)
                else:
                    self.pop_handler()
                    self.run()

class doNothingHandler(EventHandler):
    def run(self):
        pass
    def handle_event(self, event):
        if event.type is USEREVENT:
            if event.code is EV_HANDLER_ACTIVE:
                self.pop_handler()
                self.run()


class EventDispatcher(EventHandler): 
    def __init__(self):
        EventHandler.__init__(self)
        self.handlers = []
        self.lastClickEv = None
        self.set_parent(self)
        
    @property
    def lastClick(self):
        return self.lastClickEv
        
    def getLastClick(self):
        return self.lastClickEv
        
    @property
    def handler(self):
        if len(self.handlers)>0:
            return self.handlers[-1]
        return self
        
    def update_event(self, event):
        if event.type is USEREVENT:
            if event.code is EV_PUSH_HANDLER:
                handler=event.handler
                self.update_event( pygame.event.Event(USEREVENT, code=EV_HANDLER_PASSIVE))        
                handler.set_parent(self)        
                self.handlers.append(handler)
                self.update_event( pygame.event.Event(USEREVENT, code=EV_HANDLER_ACTIVE))        
                return
            elif event.code is EV_POP_HANDLER: 
                self.update_event( pygame.event.Event(USEREVENT, code=EV_HANDLER_PASSIVE))        
                self.handlers.pop()
                self.update_event( pygame.event.Event(USEREVENT, code=EV_HANDLER_ACTIVE))        
                return
                
        self.handler.handle_event(event)
        if event.type is MOUSEBUTTONDOWN:
            self.lastClickEv = event
            
                    
        
class Scene (EventDispatcher):
    def __init__(self, game, type=ORTHOGONAL):
        EventDispatcher.__init__(self)
        self.game = game
        self.compiler = qgl.render.Compiler()
        self.renderer = qgl.render.Render()
        self.root_node = qgl.scene.Root()
        
        self.picker = qgl.render.Picker()
        self.group = qgl.scene.Group()
        
        if type == PERSPECTIVE:
            self.viewport = qgl.scene.PerspectiveViewport()
            self.group.translate = ( 0.0, 0.0, -250 )
            self.viewport.screen_dimensions = (0,0) + WINDOW_SIZE
            #self.group.translate = ( 0.0, -15.0, -50 )

            light = qgl.scene.state.Light(position=(0,10,20))
            light.diffuse = ( 1.0, 1.0, 1.0, 0.0 )
            self.group.add(light)
        else:
            self.viewport = qgl.scene.OrthoViewport()
            self.viewport.screen_dimensions = (0,0) + WINDOW_SIZE
        
       
        self.root_node.add(self.viewport)
        self.viewport.add(self.group)
        self.root_node.accept(self.compiler)

    def render(self):
        self.root_node.accept(self.renderer)

    def update(self, dt):
        raise NotImplementedError("You must overwrite this method.")

    def add(self, object):
        self.group.add(object)

    def add_group(self, group):
        self.viewport.add(group)

    def accept(self):
        self.root_node.accept(self.compiler)
