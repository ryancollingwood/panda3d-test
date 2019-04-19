from panda3d.core import loadPrcFileData
# uncomment the lines below to munipulate the scene
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

from direct.showbase.ShowBase import ShowBase
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import GeoMipTerrain
from panda3d.core import WindowProperties

from follow_cam import FollowCam
from player import Player


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.accept("escape", exit)

        base.setFrameRateMeter(True)

        self.skybox = Skybox(render, "assets/skybox_purp.bam")
        
        self.grass = Terrain(render, self.cam, "assets/height.png", "assets/grass.png", 35)
    
        self.capture_mouse = True

        base.disableMouse()
        props = WindowProperties.getDefault()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        taskMgr.add(self.resetMouse, "reset mouse")

        self.panda = Player(render, self.resetMouse)
        self.panda.actor.setPos(128,128, self.grass.get_elevation(128, 128))
        self.followCam = FollowCam(self.cam, self.panda.actor)

        self.setup_physics()
    
    def resetMouse(self, task):
        if self.capture_mouse:
            cx = int(base.win.getProperties().getXSize() / 2)
            cy = int(base.win.getProperties().getYSize() / 2)
            base.win.movePointer(0, cx, cy)

    def setup_physics(self):
        taskMgr.add(self.checkCollisions, "Check Collisions")

    def checkCollisions(self, task):
        # checking collisions with rendered terrain isn't something I could get to work
        # so after some digging on the panda3d forums using the elevation was proposed
        terrian_height = self.grass.get_elevation(self.panda.actor.getX(), self.panda.actor.getY())
        panda_height = self.panda.actor.getZ()
        
        if terrian_height < panda_height:
            # to-do the panda might need to fall if the drop is large
            self.panda.actor.setZ(terrian_height)
        elif terrian_height > panda_height:
            # to-do the panda should not be able to climb if the increase is large
            self.panda.actor.setZ(terrian_height)

        return task.again

class Terrain():
    def __init__(self, parent, camera, height_map, color_map, size):
        self.terrain = GeoMipTerrain("terrain")
        self.terrain.setHeightfield(height_map)
        self.terrain.setColorMap(color_map)
        self.root = self.terrain.getRoot()
        self.root.setSz(size)
        self.root.reparentTo(parent)
        self.terrain.generate()
        self.terrain.setFocalPoint(camera)

        taskMgr.add(self.updateTerrain, "update Terrian")      

    def get_elevation(self, x, y):
        """
        https://discourse.panda3d.org/t/collision-with-terrain-generated-by-geomipterrain/4579/3
        """
        power = 16
        cumulative_sum = 0
        number = 0
        step = 0.1
        
        for i in range(-power,power):
            for j in range(-power,power):
                cumulative_sum += self.terrain.getElevation(x+i*step, y+j*step)
                number +=1
        return self.root.getSz() * (cumulative_sum/number)
       
       
    def updateTerrain(self, task):
        self.terrain.update()
        self.root = self.terrain.getRoot()
        
        return task.cont


class Skybox():
    def __init__(self, parent, bam_file):
        self.sphere = loader.loadModel(bam_file)
        self.sphere.reparentTo(parent)
 

app = MyApp()
app.run()