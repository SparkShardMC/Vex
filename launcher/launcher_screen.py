from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, OnscreenText
import platform
import subprocess
import os
import sys

class VexLauncher(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Title
        self.title = OnscreenText(text="VEX Launcher",
                                  pos=(0, 0.7),
                                  scale=0.15,
                                  fg=(1,0.2,0.1,1))

        # Buttons
        self.win_button = DirectButton(text="Install for Windows",
                                       scale=0.08,
                                       pos=(-0.5, 0, 0),
                                       frameColor=(0.2,0.2,0.2,1),
                                       command=self.install_windows)

        self.mac_button = DirectButton(text="Install for Mac",
                                       scale=0.08,
                                       pos=(0.5, 0, 0),
                                       frameColor=(0.2,0.2,0.2,1),
                                       command=self.install_mac)

    def run_packager(self, os_type):
        """
        Calls the packager.py script for the correct OS.
        Returns the path to the generated installer.
        """
        script_path = os.path.join(os.path.dirname(__file__), "packager.py")

        # Run the packager.py script
        print(f"Running packager for {os_type}...")
        subprocess.run([sys.executable, script_path], check=True)

        # Read the output path from config
        import yaml
        with open(os.path.join(os.path.dirname(__file__), "../config/electron_config.yml"), "r") as f:
            config = yaml.safe_load(f)

        if os_type == "windows":
            build_dir = config["windows"]["build_dir"]
            output_name = config["windows"]["output_name"]
        else:
            build_dir = config["mac"]["build_dir"]
            output_name = config["mac"]["output_name"]

        installer_path = os.path.join(build_dir, output_name)
        return installer_path

    def launch_installer(self, installer_path):
        """
        Launches the installer automatically in user's default directory
        """
        if platform.system().lower().startswith("win"):
            # Windows: open the .exe
            print(f"Launching installer: {installer_path}")
            os.startfile(installer_path)
        elif platform.system().lower().startswith("darwin"):
            # Mac: open the .dmg
            print(f"Opening DMG installer: {installer_path}")
            subprocess.run(["open", installer_path])
        else:
            print("Unsupported OS for installer launch.")

    def install_windows(self):
        installer = self.run_packager("windows")
        self.launch_installer(installer)

    def install_mac(self):
        installer = self.run_packager("mac")
        self.launch_installer(installer)

app = VexLauncher()
app.run()
