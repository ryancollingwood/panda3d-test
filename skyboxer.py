import direct.directbase.DirectStart
from pandac.PandaModules import *

class SkySphereWriter:
  def __init__(self, name):
    self.texture = loader.loadCubeMap(f"skybox/{name}/{name}_#.png")
    self.sphere = loader.loadModel("skybox/InvertedSphere.egg")
    self.sphere.setTexGen(TextureStage.getDefault(), 
      TexGenAttrib.MWorldPosition)
    self.sphere.setTexProjector(TextureStage.getDefault(), 
      render, self.sphere)
    self.sphere.setTexture(self.texture)
    self.sphere.setLightOff()
    self.sphere.setScale(1500)
    self.sphere.writeBamFile(f"skybox_{name}.bam")
    self.sphere.reparentTo(render)

SSW = SkySphereWriter("purp")
run()