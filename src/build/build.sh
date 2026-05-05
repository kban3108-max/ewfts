#!/bin/bash
set -e
mkdir -p ../../packages/{deb,rpm,termux,arch}

if [ "$1" = "rpm" ]; then
    TOPDIR=$(realpath ../ewfts-rpm)
    RPMDIR=$(realpath ../../packages/rpm)
    rpmbuild -ba "$TOPDIR/SPECS/ewfts.spec" \
      --define "_topdir $TOPDIR" \
      --define "_rpmdir $RPMDIR" \
      --define "_rpmfilename %{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm"

elif [ "$1" = "deb" ]; then
    dpkg-deb --build ../ewfts-debian ../../packages/deb/ewfts.deb

elif [ "$1" = "termux" ]; then
    dpkg-deb --build ../ewfts-termux ../../packages/termux/ewfts-termux.deb
elif [ "$1" = "arch" ]; then
    (cd ../ewfts-arch && makepkg -fAc --nodeps && mv *.pkg.tar.* ../../packages/arch/)
else
    echo "Usage: $0 deb|rpm|termux|arch"
    exit 1
fi
