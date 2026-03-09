from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode, TransparencyAttrib, Point3, NodePath
from panda3d.core import Filename, LPoint3, LVector3
from panda3d.physics import ForceNode, LinearVectorForce
from direct.particles.ParticleEffect import ParticleEffect
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

        # ---- Spark Particle System ----
        self.spark = ParticleEffect()
        self.spark.loadConfig("assets/particles/spark.ptf")
        self.spark.start(parent=self.render2d, renderParent=self.render2d)

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

        # ---- Logo Text Pulse Task ----
        taskMgr.add(self.pulse_text, "PulseTextTask")
        self.pulse_scale = 0.2
        self.pulse_direction = 1

    # ---- Logo ----
    def create_vex_logo(self):
        # Load soldier model
        soldier_model = "assets/models/soldier.bam"
        if os.path.exists(soldier_model):
            soldier = self.loader.loadModel(soldier_model)
        else:
            soldier = self.loader.loadModel("models/misc/rgbCube")
        soldier.reparentTo(self.render2d)
        soldier.setScale(0.3)
        soldier.setPos(-0.1,0,0.1)
        soldier.setColor(0.8,0.8,0.8,1)

        # Load shield model
        shield_model = "assets/models/shield.bam"
        if os.path.exists(shield_model):
            shield = self.loader.loadModel(shield_model)
        else:
            shield = self.loader.loadModel("models/misc/sphere")
        shield.reparentTo(self.render2d)
        shield.setScale(0.2)
        shield.setPos(0.2,0,0.1)
        shield.setColor(0.7,0.7,0.7,1)

        # VEX text
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
        self.vex_node = self.aspect2d.attachNewNode(vex_text)
        self.vex_node.setScale(self.pulse_scale)
        self.vex_node.setPos(0,0,0.5)
        self.vex_node.setColor(1,0.2,0.2,1)

    # ---- Pulse Effect for Text ----
    def pulse_text(self, task):
        self.pulse_scale += 0.001 * self.pulse_direction
        if self.pulse_scale > 0.22 or self.pulse_scale < 0.18:
            self.pulse_direction *= -1
        self.vex_node.setScale(self.pulse_scale)
        return task.cont
