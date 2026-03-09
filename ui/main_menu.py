from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib, NodePath, Loader, LVector3
from direct.gui.DirectGui import DirectButton
from panda3d.core import CardMaker, Point3
import random
import os

class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()  # Turn off default camera

        # -----------------------
        # Background
        # -----------------------
        cm = CardMaker("bg")
        cm.setFrame(-5, 5, -5, 5)
        self.bg = self.render2d.attachNewNode(cm.generate())
        self.bg.setColor(0, 0, 0, 1)  # dark black haze
        self.bg.setTransparency(TransparencyAttrib.MAlpha)

        # -----------------------
        # Spark particles
        # -----------------------
        self.particles = []
        for _ in range(50):
            pt = self.loader.loadModel("models/misc/sphere")
            pt.reparentTo(self.render2d)
            pt.setScale(random.uniform(0.01, 0.03))
            pt.setPos(random.uniform(-1,1),0,random.uniform(-1,1))
            pt.setColor(1,1,1,random.uniform(0.5,1))
            self.particles.append(pt)

        taskMgr.add(self.move_particles, "MoveParticles")

        # -----------------------
        # VEX Logo: Soldier + Shield + Text
        # -----------------------
        self.create_vex_logo()

        # -----------------------
        # Main Buttons
        # -----------------------
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

    # -----------------------
    # Particle motion
    # -----------------------
    def move_particles(self, task):
        for pt in self.particles:
            x, y, z = pt.getPos()
            z -= 0.002
            if z < -1:
                z = 1
                x = random.uniform(-1,1)
            pt.setPos(x,y,z)
        return task.cont

    # -----------------------
    # Create VEX Logo
    # -----------------------
    def create_vex_logo(self):
        # Load soldier model (placeholder cube for now)
        soldier = self.loader.loadModel("models/misc/rgbCube")  # replace with actual soldier later
        soldier.reparentTo(self.render2d)
        soldier.setScale(0.2, 0.2, 0.4)
        soldier.setPos(0,0,0.2)
        soldier.setColor(0.8,0.8,0.8,1)

        # Create shield (placeholder sphere)
        shield = self.loader.loadModel("models/misc/sphere")
        shield.reparentTo(self.render2d)
        shield.setScale(0.15)
        shield.setPos(0.25,0,0.25)
        shield.setColor(0.7,0.7,0.7,1)

        # Add VEX text using custom font
        font_path = "assets/vex_inferno.ttf"
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
        vex_text_node.setColor(1,0.2,0.2,1)  # fiery red
