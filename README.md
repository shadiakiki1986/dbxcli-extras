## dbxcli-sync

dbxcli sync command that solves https://github.com/dropbox/dbxcli/issues/53


## Install

First install [dbxcli](https://github.com/dropbox/dbxcli/)

Then install this package:

```
pip3 install git+ssh://git@github.com/shadiakiki1986/dbxcli-sync.git@v0.0.1
```

## Usage

```
dbxcli_sync [--verbose={0,1,2}] <localdir> <dbxdir>
```

Examples

```
dbxcli_sync --verbosity=0 icloud-roula-20210723/ "/20210723 icloud downloaded/"
 34%|███████████                 | 322/954 [00:58<01:54,  5.54it/s]


dbxcli_sync --verbosity=1 icloud-roula-20210723/ "/20210723 icloud downloaded/"
File already exists: icloud-roula-20210723/2014/07/23/IMG_0001.JPG
File already exists: icloud-roula-20210723/2014/07/23/IMG_0002.JPG


dbxcli_sync --verbosity=2 icloud-roula-20210723/ "/20210723 icloud downloaded/"
Command: dbxcli revs /20210723 icloud downloaded/2014/07/23/IMG_0001.JPG
File already exists: icloud-roula-20210723/2014/07/23/IMG_0001.JPG
Command: dbxcli revs /20210723 icloud downloaded/2014/07/23/IMG_0002.JPG
File already exists: icloud-roula-20210723/2014/07/23/IMG_0002.JPG
```

## License

WTFPL. Check [LICENSE](LICENSE)


## Dev notes

```
pip3 install pew
pew new dbxcli_sync
pip3 install -e .
```
