from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode, TransparencyAttrib
import random
import os

class MainMenu(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # ---- Background ----
        from panda3d.core import CardMaker
        cm = CardMaker("bg")
        cm.setFrame(-5, 5, -5, 5)
        self.bg = self.render2d.attachNewNode(cm.generate())
        self.bg.setColor(0,0,0,1)
        self.bg.setTransparency(TransparencyAttrib.MAlpha)

        # ---- Spark Particles ----
        self.particles = []
        for _ in range(50):
            pt = self.loader.loadModel("models/misc/sphere")
            pt.reparentTo(self.render2d)
            pt.setScale(random.uniform(0.01,0.03))
            pt.setPos(random.uniform(-1,1),0,random.uniform(-1,1))
            pt.setColor(1,1,1,random.uniform(0.5,1))
            self.particles.append(pt)
        taskMgr.add(self.move_particles, "MoveParticles")

        # ---- VEX Logo ----
        self.create_vex_logo()

        # ---- Main Buttons ----
        self.play_button = DirectButton(
            text="PLAY",
            scale=0.08,
            pos=(0,0,-0.4),
            frameColor=(0.2,0.2,0.2,1)
        )
        self.settings_button = DirectButton(
            text="SETTINGS",
            scale=0.06,
            pos=(0,0,-0.55),
            frameColor=(0.2,0.2,0.2,1)
        )

    # ---- Particle Motion ----
    def move_particles(self, task):
        for pt in self.particles:
            x, y, z = pt.getPos()
            z -= 0.002
            if z < -1:
                z = 1
                x = random.uniform(-1,1)
            pt.setPos(x,y,z)
        return task.cont

    # ---- VEX Logo ----
    def create_vex_logo(self):
        # Soldier placeholder
        soldier_model = "assets/models/soldier.bam"
        if os.path.exists(soldier_model):
            soldier = self.loader.loadModel(soldier_model)
        else:
            soldier = self.loader.loadModel("models/misc/rgbCube")
        soldier.reparentTo(self.render2d)
        soldier.setScale(0.2,0.2,0.4)
        soldier.setPos(0,0,0.2)
        soldier.setColor(0.8,0.8,0.8,1)

        # Shield placeholder
        shield_model = "assets/models/shield.bam"
        if os.path.exists(shield_model):
            shield = self.loader.loadModel(shield_model)
        else:
            shield = self.loader.loadModel("models/misc/sphere")
        shield.reparentTo(self.render2d)
        shield.setScale(0.15)
        shield.setPos(0.25,0,0.25)
        shield.setColor(0.7,0.7,0.7,1)

        # VEX Text
        font_path = "assets/fonts/vex_inferno.ttf"
        if os.path.exists(font_path):
            vex_font = self.loader.loadFont(font_path)
        else:
            vex_font = None

        vex_text = TextNode("vex_text")
        vex_text.setText("VEX")
        if vex_font:
            vex_text.setFont(vex_font)
        vex_text.setAlign(TextNode.ACenter)
        vex_text_node = self.aspect2d.attachNewNode(vex_text)
        vex_text_node.setScale(0.2)
        vex_text_node.setPos(0,0,0.5)
        vex_text_node.setColor(1,0.2,0.2,1)
