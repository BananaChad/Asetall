import subprocess

print("Welcome to Asetall!")
print(
    "For this program to run properly you have to choose what Operating System you're using"
)
operatingsystem = input(
    "Enter Your operating system here:\n Ubuntu/Debian/Fedora/Arch/SUSE:"
).lower()

if operatingsystem == "windows":
    subprocess.Popen(["python3", "./operatingsystems/windows.py"])
elif operatingsystem == "ubuntu" or "debian":
    subprocess.Popen(["python3", "./operatingsystems/linux/ubuntudebian.py"])
elif operatingsystem == "fedora":
    subprocess.Popen(["python3", "./operatingsystems/linux/fedora.py"])
elif operatingsystem == "arch":
    subprocess.Popen(["python3", "./operatingsystems/linux/arch.py"])
elif operatingsystem == "suse":
    subprocess.Popen(["python3", "./operatingsystems/linux/suse.py"])
