## v0.0.5 (2021-10-30)

- sync compares content hash on top of file existence
  - New dependency on dropbox python sdk
  - Ref https://www.dropbox.com/developers/reference/content-hash
  - Ref https://github.com/dropbox/dropbox-sdk-python/blob/fc72aaa95fa474171c3b4a42ee08f06841e65108/dropbox/base.py#L1473


## v0.0.4 (2021-09-06)

- faster sync by doing ls on directory and caching list of files instead of ls one file at a time


## v0.0.3 (2021-07-28)

- rename package to dbxcli-extras


## v0.0.2 (2021-07-27)

- factor out the sync command and make it a subcommand in preparation to add recursive get
- add getr function for recursive get from https://gist.github.com/debuti/5887c126811eeae1bf9451e73a7b8fd8
- bugfix, sync: use ls instead of revs to determine if file exists


## v0.0.1 (2021-07-23)

- first release: dbxcli sync command
