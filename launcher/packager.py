import os, yaml, platform, subprocess, sys

current_os = platform.system().lower()  # 'windows' or 'darwin'

# Load Electron config
with open("../config/electron_config.yml", "r") as f:
    cfg = yaml.safe_load(f)

if current_os.startswith("win"):
    os_cfg = cfg["windows"]
elif current_os.startswith("darwin"):
    os_cfg = cfg["mac"]
else:
    raise Exception("Unsupported OS for packaging")

# Ensure build directory exists
os.makedirs(os_cfg["build_dir"], exist_ok=True)

# Install Electron if needed
if cfg.get("npm_install", True):
    print(f"Installing Electron v{os_cfg['electron_version']}...")
    subprocess.run(["npm", "install", f"electron@{os_cfg['electron_version']}", "--no-save"], check=True)

# Build command
cmd = [
    "npx", "electron-packager", cfg["source_dir"], "Vex",
    "--overwrite",
    f"--out={os_cfg['build_dir']}",
    f"--icon={os_cfg['icon']}"
]

if current_os.startswith("win"):
    cmd.append("--platform=win32")
elif current_os.startswith("darwin"):
    cmd.append("--platform=darwin")

print("Packaging VEX...")
subprocess.run(cmd, check=True)
print(f"Packaged {os_cfg['output_name']} in {os_cfg['build_dir']}")
