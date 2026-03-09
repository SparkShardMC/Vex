import platform

def get_os():

    system = platform.system()

    if system == "Windows":
        return "windows"

    if system == "Darwin":
        return "mac"

    return "unknown"
