#!/bin/sh

printf "Install EWFTS? [y/N]: "
read answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    make || exit 1
    mkdir -p "$HOME/.local/bin"
    mkdir -p "$HOME/.local/share/man/man1"
    cp ewfts "$HOME/.local/bin/ewfts"
    [ -f ewfts.1 ] && cp ewfts.1 "$HOME/.local/share/man/man1/ewfts.1"
    echo "Installed."
    echo "Make sure ~/.local/bin is in path (and make sure ~/.local/share/man is in MANPATH to use the manpage)"
else
    echo "Cancelled."
fi
