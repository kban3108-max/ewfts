Name:           ewfts
Version:        2.0
Release:        1%{?dist}
Summary:        Ephemeral Wrapper for Temporary Scripts
Packager:       kban3108-max <https://github.com/kban3108-max>

License:        MIT
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       python3

%description
Ephemeral Wrapper for Temporary Scripts.

%prep
%setup -q

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/ewfts
mkdir -p %{buildroot}/usr/share/man/man1

install -m 755 ewfts %{buildroot}/usr/bin/ewfts
install -m 644 ewfts.py %{buildroot}/usr/share/ewfts/ewfts.py
install -m 644 ewfts.1 %{buildroot}/usr/share/man/man1/ewfts.1

%post
if command -v mandb >/dev/null 2>&1; then
    mandb >/dev/null 2>&1 || true
elif command -v makewhatis >/dev/null 2>&1; then
    makewhatis /usr/share/man >/dev/null 2>&1 || true
fi

%files
/usr/bin/ewfts
/usr/share/ewfts/ewfts.py
/usr/share/man/man1/ewfts.1
