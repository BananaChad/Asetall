# works, original from AsepriteTool, Modified by @BananaChad
import os
import subprocess
import sys
import zipfile
from configparser import ConfigParser

import requests

first = True
command = "req"
InstallMode = "Auto"
config = ConfigParser()

try:
    config.read("config.ini")
    update = config["Settings"]["update"]
    skia_link = config["Settings"]["skia_link_linux"]
    aseprite_path = config["Settings"]["aseprite_path_linux"]
    aseprite_link = config["Settings"]["aseprite_link"]

except Exception as e:
    print("Config File Is Corrupted or does not Exist!" + e)

home_dir = os.path.expanduser(aseprite_path)

if update == "True":
    print(
        "please wait, installing skia to "
        + aseprite_path
        + "deps/skia (update == True)"
    )
    r_skia = requests.get(skia_link)
    open("skia.zip", "wb").write(r_skia.content)

    config.set("Settings", "update", "False")

    with open("./config.ini", "w") as configfile:
        config.write(configfile)


def change_install_mode(mode):
    global InstallMode
    InstallMode = mode
    print("Success! Install-Mode is now: " + InstallMode)


def Install():
    with open("Install.sh", "w") as f:

        f.write("cd " + aseprite_path + "\n")
        f.write("git clone --recursive " + aseprite_link)

    subprocess.call(["bash", "Install.sh"])

    os.remove("Install.sh")
    skia_path = "skia.zip"
    skia_dir = os.path.join(home_dir, "deps/skia")
    # Construct the skia directory path relative to the home directory
    try:
        # Open the ZIP file
        with zipfile.ZipFile(skia_path, "r") as zip_ref:
            # Extract all files to skia_dir
            zip_ref.extractall(path=skia_dir)
            print("Extracted skia.zip to", skia_dir)
    except (zipfile.BadZipFile, OSError) as e:
        print("Error extracting skia.zip:", e)
    print(
        "Prompting for sudo permissions in order to install packages and update packages \n (sudo apt-get all packages, sudo apt update)"
    )
    BuildAseprite()

    print(
        "Done! Finished Compiling Aseprite! It can be found by going to"
        + aseprite_path
        + "aseprite/build/bin/aseprite"
    )
    os.remove("cmd.sh")


def BuildAseprite():
    with open("cmd.sh", "w") as f:
        f.write(
            "sudo apt-get install -y g++ clang libc++-dev libc++abi-dev cmake ninja-build libx11-dev libxcursor-dev libxi-dev libgl1-mesa-dev libfontconfig1-dev"
            + "\n"
        )
        f.write("sudo apt update" + "\n")
        f.write("cd " + aseprite_path + "aseprite" + "\n")
        f.write("mkdir build" + "\n")
        f.write("cd " + aseprite_path + "aseprite/build" + "\n")
        f.write("export CC=clang" + "\n")
        f.write("export CXX=clang++" + "\n")
        f.write(
            "cmake \\"
            + "\n"
            + "  -DCMAKE_BUILD_TYPE=RelWithDebInfo \\"
            + "\n"
            + "  -DCMAKE_CXX_FLAGS:STRING=-stdlib=libc++ \\"
            + "\n"
            + "  -DCMAKE_EXE_LINKER_FLAGS:STRING=-stdlib=libc++ \\"
            + "\n"
            + "  -DLAF_BACKEND=skia \\"
            + "\n"
            + "  -DSKIA_DIR="
            + aseprite_path
            + "deps/skia \\"
            + "\n"
            + "  -DSKIA_LIBRARY_DIR="
            + aseprite_path
            + "deps/skia/out/Release-x64 \\"
            + "\n"
            + "  -DSKIA_LIBRARY="
            + aseprite_path
            + "deps/skia/out/Release-x64/libskia.a \\"
            + "\n"
            + "  -G Ninja \\"
            + "\n"
            + "  .."
            + "\n"
        )
        f.write("ninja aseprite")

    subprocess.call(["bash", "cmd.sh"])


def Update():
    with open("cmd.sh", "w") as f:
        f.write("cd " + aseprite_path + "aseprite" + "\n")
        f.write("git pull" + "\n")
        f.write("git submodule update --init --recursive")
    print(
        "Prompting for sudo permissions in order to install packages and update packages \n (sudo apt-get all packages, sudo apt update and sudo apt upgrade"
    )
    BuildAseprite()
    print(
        "Done! Finished Compiling Aseprite! It can be found by searching for aseprite in the start menu"
    )
    os.remove("cmd.sh")


while 1:
    if first is False:
        command = input("Please Enter a Command: ").lower()

    if command == "help":
        print("List of available commands:")
        print("help - Shows a List of all available commands")
        print("start - Starts the install/update process")
        print("exit - Exits the program")
        print("req - Shows all requirements")
        print("InstallMode Auto/Update/Install - Changes the Installation-Mode")
        print("InstallMode - Shows the current InstallMode")
        print("dir - Shows where aseprite is installing to")
    elif command == "dir":
        print("Installing to: " + aseprite_path + "aseprite")
    elif command == "installmode":
        print("Current InstallMode is:" + InstallMode)

    elif command == "installmode auto":
        change_install_mode("Auto")

    elif command == "installmode install":
        change_install_mode("Install")

    elif command == "installmode update":
        change_install_mode("Update")

    elif command == "exit":
        sys.exit()

    elif command == "start":

        if InstallMode == "Auto":
            if os.path.isdir(home_dir + "aseprite") and os.path.isdir(
                    home_dir + "deps/skia"
            ):
                print("Update Mode detected. (currently bugged)")
                Update()
            else:
                print("Install mode detected. (currently bugged)")
                Install()
        elif InstallMode == "Install":
            Install()
        elif InstallMode == "Update":
            Update()
    elif command == "req":
        print("Requirements: ")
        print("")
        print(
            "The packages required will be auto installed when running install or update :)\n for more info go to https://github.com/aseprite/aseprite/blob/main/INSTALL.md#linux-dependencies"
        )
        print("for a list of commands, type help")
        first = False
