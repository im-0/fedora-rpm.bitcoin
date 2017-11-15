%if 0%{?_no_wallet}
%define walletargs --disable-wallet
%define _buildqt 0
%define guiargs --with-gui=no
%else
%if 0%{?_no_gui}
%define _buildqt 0
%define guiargs --with-gui=no
%else
%define _buildqt 1
%define guiargs --with-qrencode --with-gui=qt5
%endif
%endif

Name:    bitcoin
Version: 0.15.1
Release: 8%{?dist}
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
BuildRequires: miniupnpc-devel

%description
Bitcoin is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of bitcoins is carried out collectively by the network.

%if %{_buildqt}
%package qt
Summary:        Peer to Peer Cryptographic Currency
Group:          Applications/System
Obsoletes:      %{name} < %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
BuildRequires: libdb4-devel
BuildRequires: libdb4-cxx-devel
BuildRequires: qt5-qttools-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: protobuf-devel
BuildRequires: qrencode-devel
BuildRequires: desktop-file-utils

%description qt
Bitcoin is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of bitcoins is carried out collectively by the network.

This package contains the Qt based graphical client and node. If you are looking
to run a Bitcoin wallet, this is probably the package you want.
%endif

%package libs
Summary:        Bitcoin shared libraries
Group:          System Environment/Libraries

%description libs
This package provides the bitcoinconsensus shared libraries. These libraries
may be used by third party software to provide consensus verification
functionality.

Unless you know need this package, you probably do not.

%package devel
Summary:        Development files for bitcoin
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and static library for the
bitcoinconsensus shared library. If you are developing or compiling software
that wants to link against that library, then you need this package installed.

Most people do not need this package installed.

%package -n bitcoind
Summary:        The bitcoin daemon
Group:          System Environment/Daemons
Recommends:     bitcoin-cli = %{version}-%{release}

%description -n bitcoind
This package provides a stand-alone bitcoin daemon. For most users, this
package is only needed if they need a full-node without the graphical client.

Some third party wallet software will want this package to provide the actual
bitcoin node they use to connect to the network.

If you use the graphical bitcoin client then you almost certainly do not
need this package.

%package cli
Summary:        Bitcoin utilities
Group:          Applications/System
Supplements:    bitcoind = %{version}-%{release}

%description cli
This package provides several command line utilities for interacting with a
bitcoin daemon.

The bitcoin-cli utility allows you to communicate and control a bitcoin daemon
over RPC. The bitcoin-tx utility is also included, which allows you to create
custom transactions.

This package contains utilities frequently used with the bitcoind package.

%prep
%autosetup -n %{name}-%{version}

%build
./autogen.sh
%configure --disable-bench %{?walletargs} %{?guiargs}
%make_build

%check
make check

%install
make install DESTDIR=%{buildroot}

# no need to generate debuginfo data for the test executables
rm -f %{buildroot}%{_bindir}/test_bitcoin*

%if %{_buildqt}
# qt icons
install -D -p share/pixmaps/bitcoin.ico %{buildroot}%{_datadir}/pixmaps/bitcoin.ico
install -p share/pixmaps/*.png %{buildroot}%{_datadir}/pixmaps/
install -p share/pixmaps/*.xpm %{buildroot}%{_datadir}/pixmaps/
install -p share/pixmaps/*.ico %{buildroot}%{_datadir}/pixmaps/
install -p share/pixmaps/*.bmp %{buildroot}%{_datadir}/pixmaps/

# Desktop File - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/applications
cat <<EOF > bitcoin-qt.desktop
[Desktop Entry]
Version=1.0
Name=Bitcoin Core
Comment=Connect to the Bitcoin P2P Network
Comment[de]=Verbinde mit dem Bitcoin peer-to-peer Netzwerk
Comment[fr]=Bitcoin, monnaie virtuelle cryptographique pair à pair
Comment[tr]=Bitcoin, eşten eşe kriptografik sanal para birimi
Exec=bitcoin-qt %u
Terminal=false
Type=Application
Icon=bitcoin128
MimeType=x-scheme-handler/bitcoin;
Categories=Office;Finance;
StartupWMClass=Bitcoin-qt
EOF
desktop-file-validate bitcoin-qt.desktop

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install bitcoin-qt.desktop
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%if %{_buildqt}
%files qt
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/bips.md doc/files.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_bindir}/bitcoin-qt
%attr(0644,root,root) %{_datadir}/applications/bitcoin-qt.desktop
%attr(0644,root,root) %{_datadir}/pixmaps/*.ico
%attr(0644,root,root) %{_datadir}/pixmaps/*.bmp
%attr(0644,root,root) %{_datadir}/pixmaps/*.png
%attr(0644,root,root) %{_datadir}/pixmaps/*.xpm
%attr(0644,root,root) %{_mandir}/man1/bitcoin-qt.1*
%endif

%files libs
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/shared-libraries.md
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/developer-notes.md doc/shared-libraries.md
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files -n bitcoind
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/REST-interface.md doc/bips.md doc/dnsseed-policy.md doc/files.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_bindir}/bitcoind
%attr(0644,root,root) %{_mandir}/man1/bitcoind.1*

%files cli
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md
%attr(0755,root,root) %{_bindir}/bitcoin-cli
%attr(0755,root,root) %{_bindir}/bitcoin-tx
%attr(0644,root,root) %{_mandir}/man1/bitcoin-cli.1*
%attr(0644,root,root) %{_mandir}/man1/bitcoin-tx.1*

%changelog
* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-8
- Remove bench_bitcoin from the bitcoin-cli package.

* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-7
- bitcoin-daemon -> bitcoind, bitcoin-utils -> bitcoin-cli

* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-6
- Fix the desktop file.

* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-5
- Don't depend on SELinux stuff, rename the .desktop file

* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-4
- Split into subpackages.

* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-3
- Fix test_bitcoin logic, allow building without wallet.

* Wed Nov 15 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-2
- Remove test_bitcoin executable from bindir.

* Tue Nov 14 2017 Evan Klitzke <evan@eklitzke.org> - 0.15.1-1
- Initial build.
