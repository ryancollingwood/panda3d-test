from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor

class Player(DirectObject):
    def __init__(self, parent, resetMouse):
        """
        It's assumed parent is render
        """
        self.resetMouse = resetMouse
        self.actor = Actor("panda", {"walk": "panda-walk"})
        self.actor.reparentTo(parent)
        self.parent = parent

        # don't use -repeat because of slight delay after keydown
        self.actorWalk = False
        self.actorReverse = False
        self.actorLeft = False
        self.actorRight = False

        self.accept("w", self.beginWalk)
        self.accept("w-up", self.endWalk)
        self.accept("s", self.beginReverse)
        self.accept("s-up", self.endReverse)
        self.accept("a", self.beginTurnLeft)
        self.accept("a-up", self.endTurnLeft)
        self.accept("d", self.beginTurnRight)
        self.accept("d-up", self.endTurnRight)
        taskMgr.add(self.updateactor, "update actor")

    def beginWalk(self):
        self.actor.setPlayRate(1.0, "walk")
        self.actor.loop("walk")
        self.actorWalk = True

    def endWalk(self):
        self.actor.stop()
        self.actorWalk = False

    def beginReverse(self):
        self.actor.setPlayRate(-1.0, "walk")
        self.actor.loop("walk")
        self.actorReverse = True

    def endReverse(self):
        self.actor.stop()
        self.actorReverse = False

    def beginTurnLeft(self):
        self.actorLeft = True

    def endTurnLeft(self):
        self.actorLeft = False

    def beginTurnRight(self):
        self.actorRight = True

    def endTurnRight(self):
        self.actorRight = False        

    def updateactor(self, task):
        # in case we need to restore position due to collisions
        start_position = self.actor.getPos()

        if base.mouseWatcherNode.hasMouse():
            self.actor.setH(self.actor, -base.mouseWatcherNode.getMouseX() * 10)

        taskMgr.add(self.resetMouse, "reset mouse")

        if self.actorWalk:
            self.actor.setY(self.actor, -0.2)
        elif self.actorReverse:
            self.actor.setY(self.actor, 0.2)

        if self.actorLeft:
            self.actor.setH(self.actor, 0.8)
        elif self.actorRight:
            self.actor.setH(self.actor, -0.8)

        return task.cont