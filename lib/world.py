from euclid import *
import time

gravity = Vector2(0,-9.81/10) # m/s**2

            
class Collision:
    def __init__(self, ball, other, where):
        self.ball = ball
        self.other = other
        self.where = where
    def __repr__(self):
        return "<coll of %s with %s>"%(self.ball, self.other)
    
class GameObject:
    def set_world(self, world):
        self.world = world
      
    def __repr__(self):
        return "<o @ %s>"%(str(self.segment))
        
class Ball(GameObject):
    def __init__(self, position, velocity=None):
        self.position = position
        if velocity is None: velocity=Vector2(0,0)
        self.velocity = velocity
        
    def loop(self, delta):
        start = self.position
        movement = self.velocity*delta
        
        collision = True
        last = None
        while collision:
            collision = self.world.collide(self, movement, last)

            if not collision:
                q = (start + movement)
                self.position = Point2( q.x, q.y )
            else:
                movement = collision.other.reflect( 
                                (start+movement)-collision.where
                         )
                self.velocity = collision.other.reflect( self.velocity )
                start = collision.where
                last = collision.other

        self.velocity += gravity*delta
                
    def __repr__(self):
        return "<ball: p=%s v=%s>"%(str(self.position), self.velocity)
          
class Segment(GameObject):
    def __init__(self, x1, y1, x2, y2, bounce=1):
        self.segment =LineSegment2(Point2(x1, y1), Point2(x2, y2))
        self.bounce = bounce
        
    def collide(self, who, movement):
        if movement.magnitude()<0.0000002: return None

        pos = who.position
        dest = pos+movement
        segment = LineSegment2( Point2(pos.x, pos.y), Point2(dest.x, dest.y) )
        where = segment.intersect( self.segment )
        if where:
            c = Collision( who, self, where )
            return c
            
    def reflect(self, what):
        return what.reflect( Vector2(-self.segment.v.y, self.segment.v.x).normalize())*self.bounce
        
    
            
            
class Floor(Segment):
    def __init__(self, x1, y1, x2, y2):
        self.segment =Line2(Point2(x1, y1), Point2(x2, y2))
            
    def reflect(self, what):
        return Vector2(0,0)

class Goal(GameObject):
    def __init__(self, x, y,radius):
        self.segment =Circle(Point2(x, y), radius)
            
    def collide(self, who, movement):
        if movement.magnitude()<0.0000002: return None

        pos = who.position
        dest = pos+movement
        segment = LineSegment2( Point2(pos.x, pos.y), Point2(dest.x, dest.y) )
        try:
            where = segment.intersect( self.segment )
        except:
            where = None
        if where:
            c = Collision( who, self, where.p1 )
            return c

    def reflect(self, what):
        return what
                    
class World:
    def __init__(self):
        self.balls = []
        self.active = []
        self.passive = []
        
        self.events = []
        
    def add_event(self, evt):
        self.events.append( evt )
        
    def get_events(self):
        for i in range(len(self.events)):
            yield self.events.pop()
                
    def add_ball(self,ball):
        ball.set_world(self)
        self.balls.append( ball )

    def add_passive(self, what):
        what.set_world( self )
        self.passive.append( what )
        
        
    def loop(self, delta):
        for o in self.balls: o.loop(delta)
        for o in self.active: o.loop(delta)
        
    def collide(self, who, movement, last=None):
        colls = []
        for l in [self.active, self.passive]:
            for o in l:
                if not o == last:
                    c = o.collide(who, movement)
                    if c:
                        colls.append( c )
        if colls:
            mindist = -1
            for c in colls:
                try:
                    dist = who.position.distance(c.where)
                except:
                    self.add_event( c )
                    return c
                if mindist == -1 or mindist > dist:
                    mindist = dist
                    winner = c
            self.add_event( winner )
            return winner
        return None
        
    
if __name__ == "__main__":
    w = World()
    
    w.add_passive( Floor(0,0,2,0) )

    
    w.add_ball( ball = Ball(Point2(1, 10) ) )
    w.add_passive( Segment(0,3,2,3, bounce=2) )

    w.add_ball( ball = Ball(Point2(5, 10) ) )
    w.add_passive( Segment(4,4,6,3) )

    w.add_passive( Goal(1,30, 3.) )
    dt = 1
    print "Start..."
    while True:
        time.sleep(dt)
        w.loop(dt)
        print ">>", w.balls
        for e in w.get_events():
            print "evt:", e
         