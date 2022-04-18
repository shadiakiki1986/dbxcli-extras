## dbxcli-extras

[dbxcli](https://github.com/dropbox/dbxcli/) utilities:

- sync (local to remote): https://github.com/dropbox/dbxcli/issues/53
- recursive get: https://github.com/dropbox/dbxcli/issues/60

Related:
- https://github.com/dropbox/dbxcli/
- https://rclone.org/


## Install

First, install [dbxcli](https://github.com/dropbox/dbxcli/)

Then install this package:

```
pip3 install --user git+https://github.com/shadiakiki1986/dbxcli-extras.git@v0.0.8
```

## Usage

```
# syncronize a local directory with a remote directory in dropbox
dbxcli_extras sync [--verbosity={0,1,2}] [--start-from=<path>] <localdir> <dbxdir>

# recursive get
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

# Test that sync should check hash
mkdir d1
date > d1/f1
python3 -m dbxcli_extras.cli sync d1 d1
date > d1/f1
python3 -m dbxcli_extras.cli sync d1 d1

dbxcli rm d1
```
