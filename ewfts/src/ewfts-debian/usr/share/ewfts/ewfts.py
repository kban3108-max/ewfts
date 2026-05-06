import os
import subprocess
import sys
import time
import shutil

scr = os.path.abspath(__file__)
cur_dir = os.getcwd()

if len(sys.argv) == 1:
    print("EWFTS v1.0\n    for more info run 'man ewfts'")
    sys.exit(0)
if len(sys.argv) > 1:
    target = sys.argv[1:]
selected = None
n = 1
files = []
for i in range(len(target)):
    if os.path.isfile(target[i]) or os.path.isdir(target[i]):
        files.append(target[i])
for i, val in enumerate(files):
    if os.path.isfile(files[i]):
        print(f"{n}. {val} (File)")
        n += 1
    elif os.path.isdir(files[i]):
        print(f"{n}. {val} (Folder)")
        n += 1

choice = input("Select file (type 'exit' to cancel): ")
if choice == "exit":
    print("Exiting...")
    sys.exit(0)
try:
    choice = int(choice)
except (ValueError, TypeError):
    print("not int!")
    sys.exit(1)
if 1 <= choice <= len(files):
    selected = files[choice - 1]
else:
    print("Out of range.")
    sys.exit(1)

process = subprocess.Popen(target)
process.wait()

print("Finished. Cleaning up in 5 seconds... (CTRL+C to cancel)")
try:
    time.sleep(5)
except KeyboardInterrupt:
    print("Cleanup cancelled. File retained.")
    sys.exit(0)

for _ in range(5):
    try:
        if os.path.isfile(selected):
            os.remove(selected)
        elif os.path.isdir(selected):
            shutil.rmtree(selected)
        print("Deleted successfully.")
        break
    except PermissionError:
        time.sleep(0.5)
else:
    print("Failed to delete: File is still locked.")
    sys.exit(1)
