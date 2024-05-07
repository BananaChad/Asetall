# works, original from AsepriteTool
import os
import shutil
import subprocess
import sys
import zipfile
from configparser import ConfigParser
import elevate
import requests
from requests_html import HTML

first = True
command = "req"
InstallMode = "Auto"

config = ConfigParser()

try:
    # Uncomment on release!!
    elevate.elevate()
    config.read("config.ini")
    vs_url = str(config["Windows"]["vs_link"])
    update = config["Windows"]["update"]
    skia_link = config["Windows"]["skia_link_windows"]
    ninja_url = config["Windows"]["ninja_link"]
    n_p = config["Windows"]["ninja_path_windows"]
    p_path = config["Windows"]["p_path_windows"]
    aseprite_path = config["Windows"]["aseprite_path_windows"]
    aseprite_link = config["Windows"]["aseprite_link"]

except Exception as e:
    print("Config File Is Corrupted or does not Exist!", e)

home_dir = os.path.expanduser(aseprite_path)

if update == "True": #TODO: fix this abomination of code (really broken imo)
    if os.path.isdir("Git"):
        shutil.rmtree("Git")
    git_r = requests.get("https://github.com/git-for-windows/git/releases/")
    git_r = HTML(html=str(git_r.content))
    git_url = git_r.links
    versions = []
    links = []
    for i in git_url:
        if "MinGit" in i and "64" in i and not "busybox" in i:
            versions.append(i.split("MinGit-")[1].split("-")[0].replace(".", ""))
            links.append(i)

    git_url = links[max(versions)]

    cmake_r = requests.get("https://cmake.org/download/")
    cmake_r = HTML(html=str(cmake_r.content))
    cmake_url = cmake_r.links
    for i in cmake_url:
        if "windows" in i and "msi" in i and "x86_64" in i:
            cmake_url = i
            break
    git_url = "https://github.com" + git_url
    r_vs = requests.get(vs_url)
    r_git = requests.get(git_url)
    r_cmake = requests.get(cmake_url)
    r_skia = requests.get(skia_link)
    r_ninja = requests.get(ninja_url)
    os.mkdir("Git")
    open("Git.zip", "wb").write(r_git.content)
    open("vs.exe", "wb").write(r_vs.content)
    open("cmake.msi", "wb").write(r_cmake.content)
    open("skia.zip", "wb").write(r_skia.content)
    open("ninja.zip", "wb").write(r_ninja.content)
    with zipfile.ZipFile("Git.zip", "r") as zf:
        zf.extractall("Git")
    os.remove("Git.zip")
    os.system("cmake.msi")
    os.remove("cmake.msi")
    os.system("vs.exe")
    os.remove("vs.exe")
    config.set("Settings", "update", "False")
    with open("config.ini", "w") as configfile:
        config.write(configfile)

# if update == "True":  TODO: decide which one to use
#     print("it seems this is your first time running Asetall, please install these tools: \n The latest version of CMake (ADD TO PATH FOR ALL USERS), \n The ninja build system \n Visual studio 2022 (Aseprite doesn't support MinGW)\n The Desktop development with C++ item + Windows 10.0.18362.0 SDK from the Visual Studio installer \n for a visual guide go to this youtube video:")    
#     print(
#         "please wait, installing skia to "
#         + aseprite_path
#         + "deps/skia (update == True)"
#     )
#     r_skia = requests.get(skia_link)
#     open("skia.zip", "wb").write(r_skia.content)

#     config.set("Windows", "update", "False")
#     with open("config.ini", "w") as configfile:
#         config.write(configfile)


def change_install_mode(mode):
    InstallMode = mode
    print("Success! Install-Mode is now: " + InstallMode)


def Install():
    with open("Install.bat", "w") as f:
        f.write("SET PATH=%PATH%;" + os.getcwd() + "/Git/cmd" + "\n")
        f.write("cd " + home_dir + "\n")
        f.write("git clone --recursive " + aseprite_link)

    subprocess.call(["Install.bat"])

    os.remove("Install.bat")

    skia_path = "skia.zip"
    # ninja_path = "ninja.zip"

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

        # with zipfile.ZipFile(ninja_path, "r") as zf:
        #     zf.extractall(n_p)

    except Exception as e:
        print("exception occured: " + e)

    if os.path.isdir(p_path + "Microsoft Visual Studio/2022/Community/Common7/Tools"):
        BuildAseprite(
            'call "'
            + p_path
            + 'Microsoft Visual Studio/2022/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    elif os.path.isdir(
        p_path[:-1] + " (x86)" + "/Microsoft Visual Studio/2019/Community/Common7/Tools"
    ):
        BuildAseprite(
            'call "'
            + p_path[:-1]
            + " (x86)"
            + '/Microsoft Visual Studio/2019/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    else:
        print(
            "No Visual Studio installation found. Please refer to https://github.com/TheLiteCrafter/AsepriteTool" #TODO: Rewrite this
        )

    os.system(
        'shortcut /a:c /f:"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Aseprite.lnk" /t:"'
        + home_dir
        + 'aseprite/build/bin/aseprite.exe"'
    )

    print(
        "Done! Finished Compiling Aseprite! It can be found by searching for aseprite in the start menu"
    )
    os.remove("cmd.bat")


def BuildAseprite(arg0):
    with open("cmd.bat", "w") as f:
        f.write(arg0 + "\n")
        f.write("cd " + aseprite_path + "aseprite" + "\n")
        f.write("mkdir build" + "\n")
        f.write("cd " + aseprite_path + "aseprite/build" + "\n")
        f.write(
            "cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLAF_BACKEND=skia -DSKIA_DIR="
            + aseprite_path
            + "deps/skia"
            + " -DSKIA_LIBRARY_DIR="
            + aseprite_path
            + "deps/skia/out/Release-x64"
            + " -DSKIA_LIBRARY="
            + aseprite_path
            + "deps/skia/out/Release-x64/skia.lib"
            + " -G Ninja .."
            + "\n"
        )
        f.write("ninja aseprite")

    subprocess.call(["cmd.bat"])


def Update():
    with open("cmd.bat", "w") as f:
        f.write("SET PATH=%PATH%;" + os.getcwd() + "/Git/cmd" + "\n")
        f.write("cd " + aseprite_path + "aseprite" + "\n")
        f.write("git pull" + "\n")
        f.write("git submodule update --init --recursive")

    if os.path.isdir(p_path + "Microsoft Visual Studio/2022/Community/Common7/Tools"):
        BuildAseprite(
            'call "'
            + p_path
            + 'Microsoft Visual Studio/2022/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    elif os.path.isdir(
        p_path[:-1] + " (x86)" + "/Microsoft Visual Studio/2019/Community/Common7/Tools"
    ):
        BuildAseprite(
            'call "'
            + p_path[:-1]
            + " (x86)"
            + '/Microsoft Visual Studio/2019/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    else:
        print(
            "No Visual Studio installation found. Please refer to https://github.com/TheLiteCrafter/AsepriteTool"
        )

    os.system(
        'shortcut /a:c /f:"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Aseprite.lnk" /t:"'
        + aseprite_path
        + 'aseprite/build/bin/aseprite.exe"'
    )

    print(
        "Done! Finished Compiling Aseprite! It can be found by searching for aseprite in the start menu"
    )
    os.remove("cmd.bat")


while 1:
    if first is False:
        command = input("Please Enter a Command: ")
        command = str(command).lower()

    if command == "help":
        print("List of available commands:")
        print("help - Shows a List of all available commands")
        print("start - Starts the install/update process")
        print("exit - Exits the program")
        print("req - Shows all requirements")
        print("InstallMode Auto/Update/Install - Changes the Installation-Mode")

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

            if os.path.isdir(aseprite_path + "aseprite") and os.path.isdir(
                aseprite_path + "deps"
            ):
                print("Update Mode detected.")

                Update()

            else:
                print("Install mode detected.")

                Install()

        elif InstallMode == "Install":
            Install()

        elif InstallMode == "Update":
            Update()

    elif command == "req":

        print("Requirements: ")
        print("")
        print("")
        first = False
