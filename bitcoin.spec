Name:    bitcoin
Version: 0.15.1
Release: 2%{?dist}
Summary: Peer to Peer Cryptographic Currency
Group:   Applications/System
License: MIT
URL:     https://bitcoin.org/
Source0: https://github.com/bitcoin/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: libevent-devel
BuildRequires: boost-devel
%if 0%{?!enable_wallet:1}
BuildRequires: libdb4-devel
BuildRequires: libdb4-cxx-devel
%else
%define walletargs --disable-wallet
%endif
%if 0%{?enable_gui}
BuildRequires: qt5-qttools-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: protobuf-devel
BuildRequires: qrencode-devel
%define guiargs --with-gui=qt5 --with-qrencode
%else
%define guiargs --with-gui=no
%endif

%description
Bitcoin is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of bitcoins is carried out collectively by the network.

%prep
%autosetup -n %{name}-%{version}

%build
./autogen.sh
%configure --disable-bench %{?walletargs} %{?guiargs}
%make_build

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_bindir}/test_bitcoin

%check
make check

%files
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/bips.md doc/files.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_mandir}/man1/bitcoin*.1.gz
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%changelog
* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-2
- Remove test_bitcoin executable from bindir.

* Tue Nov 14 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-1
- Initial build.
