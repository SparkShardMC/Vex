from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.DirectGui import DirectButton, OnscreenText
from direct.task import Task
from direct.particles.ParticleEffect import ParticleEffect
import math, random

class VexMainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Camera
        self.camera.setPos(0, -16, 4)
        self.camera.lookAt(0, 0, 1.5)
        self.time = 0

        # Setup scene
        self.setup_lighting()
        self.create_fog()
        self.create_background()
        self.create_logo()
        self.create_soldier()
        self.create_buttons()
        self.create_sparks_particles()

        # Tasks
        taskMgr.add(self.animate_camera, "animate_camera")
        taskMgr.add(self.animate_soldier, "animate_soldier")
        taskMgr.add(self.animate_logo, "animate_logo")

    # ---------- Lighting ----------
    def setup_lighting(self):
        ambient = AmbientLight("ambient")
        ambient.setColor((0.3,0.3,0.3,1))
        ambient_np = render.attachNewNode(ambient)
        render.setLight(ambient_np)

        directional = DirectionalLight("sun")
        directional.setColor((1,1,1,1))
        sun_np = render.attachNewNode(directional)
        sun_np.setHpr(-45,-45,0)
        render.setLight(sun_np)

    # ---------- Fog ----------
    def create_fog(self):
        fog = Fog("sceneFog")
        fog.setColor(0,0,0,1)
        fog.setExpDensity(0.03)
        render.setFog(fog)

    # ---------- Background ----------
    def create_background(self):
        cm = CardMaker("bg")
        cm.setFrame(-30,30,-20,20)
        self.bg = render.attachNewNode(cm.generate())
        self.bg.setPos(0,40,0)
        self.bg.setColor(0.02,0.02,0.05,1)

    # ---------- Logo ----------
    def create_logo(self):
        font = loader.loadFont("assets/fonts/vex_inferno.ttf")
        self.logo = OnscreenText(text="VEX",
                                 font=font,
                                 scale=0.3,
                                 pos=(0,0.75),
                                 fg=(1,0.2,0.1,1),
                                 align=TextNode.ACenter)

    # ---------- Soldier Logo ----------
    def create_soldier(self):
        self.soldier = render.attachNewNode("soldier")

        # Body
        body = loader.loadModel("models/misc/rgbCube")
        body.reparentTo(self.soldier)
        body.setScale(0.7,0.4,1.2)
        body.setPos(0,0,1.2)

        # Head
        head = loader.loadModel("models/misc/sphere")
        head.reparentTo(self.soldier)
        head.setScale(0.4)
        head.setPos(0,0,2.3)

        # Legs
        self.left_leg = loader.loadModel("models/misc/rgbCube")
        self.left_leg.reparentTo(self.soldier)
        self.left_leg.setScale(0.25,0.25,1)
        self.left_leg.setPos(-0.25,0,0.5)

        self.right_leg = loader.loadModel("models/misc/rgbCube")
        self.right_leg.reparentTo(self.soldier)
        self.right_leg.setScale(0.25,0.25,1)
        self.right_leg.setPos(0.25,0,0.5)

        # Arms
        self.left_arm = loader.loadModel("models/misc/rgbCube")
        self.left_arm.reparentTo(self.soldier)
        self.left_arm.setScale(0.2,0.2,0.9)
        self.left_arm.setPos(-0.8,0,1.6)

        shield = loader.loadModel("models/misc/sphere")
        shield.reparentTo(self.left_arm)
        shield.setScale(0.6,0.15,0.6)
        shield.setPos(-0.5,0,0)
        shield.setColor(0.1,0.8,1,1)  # glowing shield

        self.right_arm = loader.loadModel("models/misc/rgbCube")
        self.right_arm.reparentTo(self.soldier)
        self.right_arm.setScale(0.2,0.2,0.9)
        self.right_arm.setPos(0.8,0,1.6)

        sword = loader.loadModel("models/misc/rgbCube")
        sword.reparentTo(self.right_arm)
        sword.setScale(0.1,0.1,1.4)
        sword.setPos(0,0,1)
        sword.setColor(1,0.6,0.1,1)  # glowing sword

    # ---------- Buttons ----------
    def create_buttons(self):
        self.play_button = DirectButton(text="PLAY", scale=0.08, pos=(0,0,-0.35),
                                        frameColor=(0.15,0.15,0.15,1),
                                        command=self.play_game)
        self.settings_button = DirectButton(text="SETTINGS", scale=0.06, pos=(0,0,-0.5),
                                            frameColor=(0.15,0.15,0.15,1),
                                            command=self.settings)

    # ---------- Particle Sparks ----------
    def create_sparks_particles(self):
        self.sparks = []
        for i in range(100):
            spark = loader.loadModel("models/misc/sphere")
            spark.reparentTo(render)
            spark.setScale(0.03)
            spark.setColor(1,random.uniform(0.4,0.8),0.1,1)
            spark.setPos(random.uniform(-4,4), random.uniform(-3,4), random.uniform(0,4))
            self.sparks.append(spark)

    # ---------- Animations ----------
    def animate_camera(self, task):
        self.time += globalClock.getDt()
        x = math.sin(self.time*0.2)*3
        y = -16 + math.cos(self.time*0.2)*2
        z = 4 + math.sin(self.time*0.1)*0.3
        self.camera.setPos(x,y,z)
        self.camera.lookAt(0,0,1.5)
        return Task.cont

    def animate_soldier(self, task):
        t = globalClock.getFrameTime()*3
        leg = math.sin(t)*30
        arm = math.sin(t)*-30
        self.left_leg.setP(leg)
        self.right_leg.setP(-leg)
        self.left_arm.setP(arm)
        self.right_arm.setP(-arm)

        # Update sparks
        for spark in self.sparks:
            spark.setZ(spark.getZ()-0.03)
            if spark.getZ()<0: spark.setZ(random.uniform(3,6))
        return Task.cont

    def animate_logo(self, task):
        scale = 0.3 + math.sin(globalClock.getFrameTime()*2)*0.03
        self.logo.setScale(scale)
        return Task.cont

    # ---------- Button Actions ----------
    def play_game(self):
        print("Launching Game...")

    def settings(self):
        print("Opening Settings...")


app = VexMainMenu()
app.run()
