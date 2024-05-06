import subprocess

print("Welcome to Asetall!")
print(
    "For this program to run properly you have to choose what Operating System you're using"
)
operatingsystem = input(
    "Enter Your operating system here:\n Ubuntu/Debian/Fedora/Arch/SUSE:"
).lower()

if operatingsystem == "windows":
    subprocess.Popen(["python", "./operatingsystems/Windows.py"])
elif operatingsystem == "ubuntu" or "debian":
    subprocess.Popen(["python", "./operatingsystems/ubuntudebian.py"])
elif operatingsystem == "fedora":
    subprocess.Popen(["python", "./operatingsystems/fedora.py"])
elif operatingsystem == "arch":
    subprocess.Popen(["python", "./operatingsystems/arch.py"])
elif operatingsystem == "suse":
    subprocess.Popen(["python", "./operatingsystems/suse.py"])
