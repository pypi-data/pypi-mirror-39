from ezgame import Ezgame
from point2d import Point2D
import math

ANGLE = 45
NEXT_SIZE = 0.9

class Tree:
    def __init__(self, p, size, level=1, leaf=False):
        self.p = p
        self.size  = size
        self.level = level
        self.right = None
        self.left  = None
        self.leaf  = False


    def create_children(self, levels=1, angle=ANGLE):
        right_point   = Point2D()
        right_point.r = self.size*NEXT_SIZE
        right_point.a = self.p.a - angle
        right_point   = right_point + self.p
        self.right    = Tree(right_point, self.size*NEXT_SIZE, levels)

        left_point   = Point2D()
        left_point.r = self.size*NEXT_SIZE
        left_point.a = self.p.a + angle
        left_point   = left_point + self.p
        self.left    = Tree(left_point, self.size*NEXT_SIZE, levels)


        if levels <= 0:
            self.right.leaf = True
            self.left.leaf  = True
        else:
            self.right.create_children(levels-1, angle)
            self.left.create_children(levels-1, angle)

#############

APPW = 1200
APPH = 800

LEVELS = 9
FPS = 32

class Application:
    def __init__(self):
        self.ez = Ezgame(APPW, APPH)
        self.ez.origin = Point2D(APPW/2.0, APPH*0.90)
        self.ez.fps = FPS
        self.ez.init(self.loop)

        self.size = 1
        p = Point2D(0, 0)
        p.a = math.radians(90)
        self.tree = Tree(p, self.size, LEVELS)
        self.angle = math.radians(1)

    def drawNode(self, node):
        if node.level == 1:
            self.drawChildren(node, "chartreuse2")
        elif node.level == 2:
                self.drawChildren(node, "chartreuse3")
        elif node.level == 3:
                self.drawChildren(node, "chartreuse4")
        else:
                self.drawChildren(node, "burlywood4")

    def drawChildren(self, node, color):
        self.ez.line(node.p, node.right.p, color, node.level)
        self.ez.line(node.p, node.left.p, color, node.level)

        if not node.right.leaf:
            self.drawNode(node.right)
            self.drawNode(node.left)
        return


    def loop(self):
        self.tree.create_children(LEVELS, self.angle)
        self.drawNode(self.tree)

        if self.angle <= math.radians(35):
            self.angle += math.radians(0.1)
        if self.tree.size <= 100:
            self.tree.size += 0.5

    def run(self):
        self.ez.run()


def run_example():
    app = Application()
    app.run()