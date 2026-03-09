from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, OnscreenText
import platform, os, sys
import subprocess

class VexLauncher(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.title = OnscreenText(text="VEX Launcher", pos=(0,0.7),
                                  scale=0.15, fg=(1,0.2,0.1,1))

        self.win_button = DirectButton(text="Install / Update Windows",
                                       scale=0.08, pos=(-0.5,0,0),
                                       frameColor=(0.2,0.2,0.2,1),
                                       command=self.install_windows)

        self.mac_button = DirectButton(text="Install / Update Mac",
                                       scale=0.08, pos=(0.5,0,0),
                                       frameColor=(0.2,0.2,0.2,1),
                                       command=self.install_mac)

    def run_packager(self):
        script_path = os.path.join(os.path.dirname(__file__), "repo_checker.py")
        print("Checking for updates...")
        subprocess.run([sys.executable, script_path], check=True)

    def launch_installer(self, os_type):
        import yaml
        with open(os.path.join(os.path.dirname(__file__), "../config/electron_config.yml"), "r") as f:
            cfg = yaml.safe_load(f)
        if os_type=="windows":
            build_dir = cfg["windows"]["build_dir"]
            output_name = cfg["windows"]["output_name"]
        else:
            build_dir = cfg["mac"]["build_dir"]
            output_name = cfg["mac"]["output_name"]

        installer_path = os.path.join(build_dir, output_name)

        if os.path.exists(installer_path):
            if platform.system().lower().startswith("win"):
                os.startfile(installer_path)
            elif platform.system().lower().startswith("darwin"):
                subprocess.run(["open", installer_path])
            print(f"Launched installer: {installer_path}")
        else:
            print("Installer not found!")

    def install_windows(self):
        self.run_packager()
        self.launch_installer("windows")

    def install_mac(self):
        self.run_packager()
        self.launch_installer("mac")

app = VexLauncher()
app.run()
