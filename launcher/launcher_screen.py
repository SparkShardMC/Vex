from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton
from installer import install_game

class LauncherScreen(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.windows_button = DirectButton(
            text="Install for Windows",
            scale=0.08,
            pos=(-0.35,0,0),
            frameColor=(0,0.8,0,1),
            command=self.install_windows
        )

        self.mac_button = DirectButton(
            text="Install for Mac",
            scale=0.08,
            pos=(0.35,0,0),
            frameColor=(0,0.8,0,1),
            command=self.install_mac
        )

    def install_windows(self):
        install_game("windows")

    def install_mac(self):
        install_game("mac")
