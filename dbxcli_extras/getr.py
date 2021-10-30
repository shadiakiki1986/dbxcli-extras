# From https://gist.github.com/debuti/5887c126811eeae1bf9451e73a7b8fd8

import os
import subprocess
import re
import hashlib
from .dropbox_api import DropboxAPI


def md5(f):
  BLOCKSIZE=65536
  hasher = hashlib.md5()
  with open(f, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
      hasher.update(buf)
      buf = afile.read(BLOCKSIZE)
  return(hasher.hexdigest())


class DbxcliGetr:
  def __init__(self, verify, verbosity):
    self.verify = verify
    self.verbosity = verbosity
    self.dbxapi = DropboxAPI(verbosity)

  def _get(self, remote):
    dlcmd = ["dbxcli", "get", remote]
    if self.verbosity>=2: print(dlcmd)
    dlproc = subprocess.run(dlcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if self.verbosity>=1:
      try: 
        count, order = re.compile('/(\S+)\s(\S+)').match(dlproc.stderr.decode('utf-8')).group(1, 2)
        print("Downloaded " + remote +" "+ count + " " + order)
      except Exception:
        print("Downloaded " + remote)


  def getr(self, remote, local):
    localcwd = os.getcwd()
    os.chdir(local)
    #print("cwd: " + os.getcwd())
    for obj_isdir, _, obj_name in self.dbxapi.ls_dir(remote):
      if obj_isdir:
        os.mkdir(obj_name)
        if self.verbosity>=1: print("Created " + remote+'/'+obj_name)
        self.getr(remote+'/'+obj_name, obj_name)
      else:
        if self.verify:
          myhash=None
          while True:
            self._get(remote+'/'+obj_name)
            chash = md5(obj_name)
            if myhash == chash:
              break
            else:
              myhash=chash
        else:
          self._get(remote+'/'+obj_name)

    os.chdir(localcwd)
