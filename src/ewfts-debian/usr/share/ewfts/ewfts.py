import os
import subprocess
import sys
import time

scr = os.path.abspath(__file__)
cur_dir = os.getcwd()

if len(sys.argv) == 1:
    print("EWFTS v1.0\n  -file <file> - specify a file\nfor more info run 'man ewfts'")
    sys.exit(0)

if len(sys.argv) > 1:
    target = sys.argv[1:]
    cmd = []
    i = 0
    while i < len(target):
        if target[i] == "-file":
            i += 2
            continue
        cmd.append(target[i])
        i += 1
    target2 = ' '.join(cmd)
    target3 = target[-1]
    if "-file" in target:
        if not target.index("-file") + 1 >= len(target):
            if os.path.isfile(target[target.index("-file") + 1]):
                target3 = target[target.index("-file") + 1]
            else:
                print("EWFTS error: File doesnt exist.")
                sys.exit(1)
        else:
            print("Give argument after file!")
            sys.exit(1)

    if not os.path.isfile(target3):
        print("EWFTS error: last argument must be a file if not using -file.")
        sys.exit(1)
else:
    print("No Argument Given!")
    sys.exit(1)
if not cmd or target3 != cmd[-1]:
    cmd.append(target3)
print(f"Running: {target2}")

process = subprocess.Popen(cmd)
process.wait()

print("Finished. Cleaning up in 5 seconds... (CTRL+C to cancel)")
try:
    time.sleep(5)
except KeyboardInterrupt:
    print("Cleanup cancelled. File retained.")
    sys.exit(0)

for _ in range(5):
    try:
        os.remove(target3)
        print("Deleted successfully.")
        break
    except PermissionError:
        time.sleep(0.5)
else:
    print("Failed to delete: File is still locked.")
    sys.exit(1)
