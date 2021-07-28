## dbxcli-extras

A CLI that wraps [dbxcli](https://github.com/dropbox/dbxcli/) to solve some long-standing issues:

- Missing sync command: https://github.com/dropbox/dbxcli/issues/53
- Missing recursive get command: https://github.com/dropbox/dbxcli/issues/60


## Install

First install [dbxcli](https://github.com/dropbox/dbxcli/)

Then install this package:

```
pip3 install git+https://github.com/shadiakiki1986/dbxcli-extras.git@v0.0.3
```

## Usage

```
dbxcli_extras sync [--verbosity={0,1,2}] <localdir> <dbxdir>
dbxcli_extras getr [--verbosity={0,1,2}] [--verify] <dbxdir> <localdir>
```

For examples, see [this jupyter notebook](https://gist.github.com/shadiakiki1986/7c478d451a4221d464d7bcfd5fc6a914)


## License

WTFPL. Check [LICENSE](LICENSE)


## Dev notes

```
pip3 install pew
pew new dbxcli_extras
pip3 install -e .
```
