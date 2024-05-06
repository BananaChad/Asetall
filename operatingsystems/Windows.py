# ok how will i do this
# Asetall is a auto installer for popular tool aseprite (https://www.github.com/aseprite/aseprite)
# I am NOT affiliated with aseprite and this is not an official tool
# this script expects you to save files like skia to their default paths, if the script cant find it it will prompt you to A: install for you or B: let you specify a new path
import os
import sys
from configparser import ConfigParser
import zipfile
import requests
import subprocess
import shutil
from requests_html import HTML
import elevate
# start by using git clone --recursive https://github.com/aseprite/aseprite.git if it cant find /aseprite
# if it updates ase start by discarding all changes (ADD WARNING!) and git pull and update submodule

first = True
command = "req"
InstallMode = "Auto"

config = ConfigParser()

try:
    # TODO Uncomment on release
    # elevate.elevate()
    config.read("config.ini")
    vs_url = str(config["Settings"]["vs_link"])
    update = config["Settings"]["update"]
    skia_url = config["Settings"]["skia_link"]
    ninja_url = config["Settings"]["ninja_link"]
    n_p = config["Settings"]["ninja_path"]
    p_path = config["Settings"]["p_path"]
    aseprite_path = config["Settings"]["aseprite_path"]
    aseprite_link = config["Settings"]["aseprite_link"]
except Exception as e:
    print("Config File Is Corrupted or does not Exist!" + e)
    
if update == "True":
    if os.path.isdir("Git"):
        shutil.rmtree("Git")
