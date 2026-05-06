import os
import subprocess
import sys
import time
import shutil

scr = os.path.abspath(__file__)
cur_dir = os.getcwd()

if len(sys.argv) == 1:
    print("EWFTS v1.0\n    setup - setup for windows, does nothing on POSIX\n    setup user - makes a shim in ~/.local/bin, does nothing on windows\n    setup system - makes a shim in /usr/local/bin, does nothing on windows\n    run - runs any executable with the EWFTS wrapper\n    -file <file> - specify a file")
    sys.exit(0)

elif sys.argv[1] == 'setup':
    if os.name == 'nt':
        import winreg as r

        k = r.OpenKey(r.HKEY_CURRENT_USER, r"Environment", 0, r.KEY_ALL_ACCESS)
        try:
            p, _ = r.QueryValueEx(k, "Path")
        except FileNotFoundError:
            p = ""
        def norm(path):
            return os.path.normcase(os.path.normpath(path))

        cur_norm = norm(cur_dir)

        paths = p.split(";")
        norm_paths = [norm(x) for x in paths if x]

        if cur_norm not in norm_paths:
            new_path = (p + ";" if p and not p.endswith(";") else p) + cur_dir
            r.SetValueEx(k, "Path", 0, r.REG_EXPAND_SZ, new_path)
            print("Complete! Restart terminal to apply")
            print("Warning: DO NOT MOVE OR DELETE THIS FILE IT IS NOT TEMPORARY!")
    elif os.name == 'posix':
        target = os.path.expanduser("~/.local/bin/ewfts")
        if len(sys.argv) > 2 and sys.argv[2] == 'system':
            try:
                with open("/usr/local/bin/ewfts", "w") as f:
                    f.write(f'#!/bin/sh\n{sys.executable} {scr} "$@"')
                    os.chmod("/usr/local/bin/ewfts", 0o755)
                    print("Complete!")
                    print("Warning: DO NOT MOVE OR DELETE THIS FILE IT IS NOT TEMPORARY!")
            except PermissionError:
                print("EWFTS error: permission denied: run with sudo")
                sys.exit(1)
        elif len(sys.argv) > 2 and sys.argv[2] == 'user':
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w") as f:
                f.write(f'#!/bin/sh\n{sys.executable} {scr} "$@"')
                os.chmod(target, 0o755)
                print("Complete!")
                print("Make sure ~/.local/bin is in your PATH")
                print("Warning: DO NOT MOVE OR DELETE THIS FILE IT IS NOT TEMPORARY!")
        else:
            print("Usage: ewfts setup [user|system]")
            sys.exit(1)
    sys.exit(0)

elif sys.argv[1] == 'run':
    if len(sys.argv) > 2:
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

else:
    print("Command Not Recognized")
    sys.exit(1)
