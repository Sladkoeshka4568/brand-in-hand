import subprocess


files = ["main.py", "main_bot.py"]
for file in files:
    subprocess.Popen(args=["start", "python", file], shell=True, stdout=subprocess.PIPE)