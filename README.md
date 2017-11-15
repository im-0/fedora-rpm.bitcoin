A spec file for Bitcoin. The work here is based on the spec file in the Bitcoin
contrib directory. The main difference between this spec and the one in contrib
is that this version is less heavily modified, e.g. it doesn't install SELinux
rules or try to create system directories.

To enable the COPR:

```bash
$ sudo dnf copr enable eklitzke/bitcoin
```

Afterwards you should install at least one of `bitcoin-qt` or `bitcoin-daemon`.
