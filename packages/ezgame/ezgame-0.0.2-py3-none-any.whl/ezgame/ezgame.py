import pygame
from pygame.locals import *
from point2d import Point2D

class Ezgame:
    def __init__(self, width=100, height=100):
        self.width  = width
        self.height = height
        self.size   = (self.width, self.height)
        self.origin = Point2D(self.width/2, self.height/2)
        # self.origin = Point2D(300, self.height-150)

        self.screen = None

        self.backgroundColor = '#FFFFFF'
        self.axisColor = '#D0D0D0'
        self.textColor = '#666666'

        self.loopFunction = None
        self.keepRunning = True

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.keys = {
            K_ESCAPE: self.setQuit
        }

        self.gui = True

    def setSize(self, w, h):
        self.width  = w
        self.height = h
        self.size   = (self.width, self.height)
        self.origin = Point2D(self.width/2, self.height/2)


    def worldToScreen(self, p):
        # transforms world coordinates to screen coordinates
        return Point2D(p.x+self.origin.x, self.origin.y - p.y)

    def screenToWorld(self, p):
        # transforms screen coordinates to world coordinates
        return Point2D(p.x-self.origin.x, self.origin.y - p.y)

    def init(self, loopFunction=None):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 15)
        self.screen = pygame.display.set_mode(self.size)
        # self.screen.fill(Color(self.backgroundColor))
        self.loopFunction = loopFunction

    def line(self, ini, end, color='black', width=1):
        if self.gui:
            pygame.draw.line(
                self.screen,
                Color(color),
                self.worldToScreen(ini).ints(),
                self.worldToScreen(end).ints(),
                width)

    def lines(self, points, color='black', width=1):
        if self.gui:
            transformed = [self.worldToScreen(p).ints() for p in points]
            pygame.draw.lines(
                self.screen,
                Color(color),
                False,
                transformed,
                width)

    def point(self, pos, color='red', size=3):
        if self.gui:
            pygame.draw.circle(
                self.screen, 
                Color(color), 
                self.worldToScreen(pos).ints(),
                size
            )

    def text(self, txt, pos, onScreen=False):
        if self.gui:
            label = self.font.render(txt, 1, Color(self.textColor))
            pos_tuple = self.worldToScreen(pos).ints()
            if onScreen:
                pos_tuple = pos.ints()
            self.screen.blit(label, pos_tuple)

    def getMousePos(self):
        return self.screenToWorld(Point2D(pygame.mouse.get_pos()))

    def drawScreen(self):
        if self.gui:
            self.screen.fill(Color(self.backgroundColor))
            self.drawAxis()


    def drawAxis(self):
        if self.gui:
            pygame.draw.line(
                self.screen,
                Color(self.axisColor),
                (0, int(self.origin.y)),
                (self.width, int(self.origin.y)),
                1)
            pygame.draw.line(
                self.screen,
                Color(self.axisColor),
                (int(self.origin.x), 0),
                (int(self.origin.x), self.height),
                1)

    def setQuit(self):
        self.keepRunning = False
        pygame.display.quit()
        pygame.quit()

    def press(self, key, func):
        self.keys[key] = func

    def run(self):
        while self.keepRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.setQuit()
                elif event.type == KEYDOWN:
                    if event.key in self.keys:
                        self.keys[event.key]()

            if self.gui:
                self.drawScreen()

            if self.loopFunction:
                self.loopFunction()
            pygame.display.flip()

            self.clock.tick(self.fps)



