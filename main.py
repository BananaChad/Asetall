import subprocess

print("Welcome to Asetall!")
print(
    "For this program to run properly you have to choose what Operating System you're using"
)
operatingsystem = input(
    "Enter Your operating system here:\n Ubuntu/Debian/Windows:"
).lower()

if operatingsystem == "windows":
    subprocess.run(["py", "./operatingsystems/windows.py"])
elif operatingsystem == "ubuntu" or "debian":
    subprocess.run(["python3", "./operatingsystems/linux/ubuntudebian.py"])
elif operatingsystem == "fedora":
    subprocess.run(["python3", "./operatingsystems/linux/fedora.py"])
elif operatingsystem == "arch":
    subprocess.run(["python3", "./operatingsystems/linux/arch.py"])
elif operatingsystem == "suse":
    subprocess.run(["python3", "./operatingsystems/linux/suse.py"])
