import utility
import pygame
import actor
import random
import aitools
import animation
import copy

from actor import *

def loadData():
    Bokko.bulletSound = utility.loadSound("baakeHit")
    Bokko.MasterAnimationList.buildAnimation("Idle", ["bokko"])

class Bokko(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):
        
        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_BAAKE
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")        
        
        self.rect = self.image.get_rect()
        
        self.boundStyle = BOUND_STYLE_REFLECT
        self.bounds = [32,32,(SCREEN_WIDTH - 32),(SCREEN_HEIGHT - 32)]
                
        self.canCollide = True
        self.hitrect = pygame.Rect(0,0,108,88)
        
        self.position = vector.vector2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = vector.vector2d(5.0,0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = 5.0
        self.changeDirection = 0
        self.arc = -1
        self.moving = 0

        """    BOSS FIGHT        """
        self.leaveScreen = False

        aitools.spawnOnScreen(self)
    
    
    def actorUpdate(self):
        if not self.leaveScreen:
            self.processAI()
        else:
            self.boundStyle = BOUND_STYLE_KILL

        if not self.active:
            self.active = True
        
        
        
    def processAI(self):
        if not self.changeDirection:
            self.changeDirection = 2 * FRAMES_PER_SECOND
            self.moving = 12
            arcDirection = int(random.random() * 2) - 1

            if arcDirection:
                self.arc = 0.7
            else:
                self.arc = -0.7

            aitools.cardinalDirection(self)

        if self.moving:
            self.speed = 5
            self.moving -= 1
        else:
            self.speed = 7
            self.velocity += self.velocity.getPerpendicular().makeNormal() * self.arc
            self.velocity = self.velocity.makeNormal() * self.speed
                    
            self.changeDirection -= 1
    
    
    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_BULLET:
            utility.playSound(Bokko.bulletSound,BAAKE_CHANNEL)

        elif self.objectCollidedWith.actorType == ACTOR_PLAYER:
                if self.objectCollidedWith.position.x < self.position.x - 64:
                    self.objectCollidedWith.position = vector.vector2d((self.position.x - 94),
                                                                         self.objectCollidedWith.position.y)
                    if self.objectCollidedWith.velocity:
                        self.objectCollidedWith.velocity *= [-1.0, 1.0]
                           
                elif self.objectCollidedWith.position.x > self.position.x + 64:
                    self.objectCollidedWith.position = vector.vector2d((self.position.x + 94),
                                                                         self.objectCollidedWith.position.y)
                    if self.objectCollidedWith.velocity:
                        self.objectCollidedWith.velocity *= [-1.0, 1.0]
                        
                if self.objectCollidedWith.position.y < self.position.y - 32:
                    self.objectCollidedWith.position = vector.vector2d(self.objectCollidedWith.position.x,
                                                                         self.position.y - 76)
                    if self.objectCollidedWith.velocity:
                        self.objectCollidedWith.velocity *= [1.0, -1.0]
                        
                elif self.objectCollidedWith.position.y > self.position.y + 32:
                    self.objectCollidedWith.position = vector.vector2d(self.objectCollidedWith.position.x,
                                                                         self.position.y + 108)
                    if self.objectCollidedWith.velocity:
                        self.objectCollidedWith.velocity *= [1.0, -1.0]