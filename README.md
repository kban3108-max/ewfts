EWFTS - Ephemeral Wrapper For Temporary Scripts

EWFTS is a simple Python tool that runs a command and deletes a specified file after execution, with a short cancellation window.

For more details, see the man page: [Here](src/ewfts-arch/ewfts.1)

Examples

Universal (Python script)

ewfts run -file hi.txt cat

Packaged (installed)

ewfts -file hi.txt cat

In both cases:

- "hi.txt" is automatically moved to the end of the command
- The command is executed ("cat hi.txt")
- A 5-second timer starts
- You can press "Ctrl+C" to cancel deletion
- Otherwise, "hi.txt" is deleted

Use Cases

- Temporary files
- One-time scripts
- Disposable automation

Availability

Ships as:

- .deb
- .deb (Termux)
- .rpm
- .pkg.tar.xz

License

[License](LICENSE)
