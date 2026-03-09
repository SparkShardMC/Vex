import yaml

def check_for_updates():

    with open("config/version.yaml") as file:
        local = yaml.safe_load(file)["version"]

    print("Current version:", local)

    return False
