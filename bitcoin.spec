Name:    bitcoin
Version: 0.15.1
Release: 1%{?dist}
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
BuildRequires: libdb4-devel
BuildRequires: libdb4-cxx-devel

%description
Bitcoin is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of bitcoins is carried out collectively by the network.

%prep
%autosetup -n %{name}-%{version}

%build
./autogen.sh
%configure --disable-bench
%make_build

%install
%make_install

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
* Tue Nov 14 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-1
- Initial build.
- new version
