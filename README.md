![EWFTS logo](logo.jpg)
# EWFTS - Ephemeral Wrapper For Temporary Scripts

EWFTS is a simple Python tool that processes a command, detects file references in the current directory, lets the user choose one interactively, then executes the reconstructed command via the system shell.

After execution, it deletes the selected file after a short cancellation window.

For more details, see the man page: [Here](ewfts/src/ewfts-arch/ewfts.1)

# Examples

ewfts "cat file.txt > newfile.txt"

- You get a list of files structured like this:
    1. file.txt
    2. newfile.txt
- it scans the current directory for files found in the input command
- user selects which file to act on
- runs the reconstructed shell command
- then deletes the selected file (with a 5 second cancellation window)

# Behaviour

- if your command is not in a string (for example: `ewfts cat hi.txt > newhi.txt`), then the shell intercepts operators (e.g. `>`, `*`, `$`) and executes them before EWFTS runs
- to fix this, wrap your command in a string (for example: `ewfts "cat hi.txt > newhi.txt"`), so EWFTS receives the full input correctly

# License

[License](LICENSE)
