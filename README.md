## dbxcli-sync

A CLI that wraps [dbxcli](https://github.com/dropbox/dbxcli/) to solve some long-standing issues:

- https://github.com/dropbox/dbxcli/issues/53
- https://github.com/dropbox/dbxcli/issues/60


## Install

First install [dbxcli](https://github.com/dropbox/dbxcli/)

Then install this package:

```
pip3 install git+https://github.com/shadiakiki1986/dbxcli-sync.git@v0.0.2
```

## Usage

```
dbxcli_sync sync [--verbosity={0,1,2}] <localdir> <dbxdir>
dbxcli_sync getr [--verbosity={0,1,2}] [--verify] <dbxdir> <localdir>
```

For examples, see the jupyter notebook at https://gist.github.com/shadiakiki1986/7c478d451a4221d464d7bcfd5fc6a914


## License

WTFPL. Check [LICENSE](LICENSE)


## Dev notes

```
pip3 install pew
pew new dbxcli_sync
pip3 install -e .
```
