# From https://gist.github.com/debuti/5887c126811eeae1bf9451e73a7b8fd8

import os
import subprocess
import re
import hashlib


def md5(f):
  BLOCKSIZE=65536
  hasher = hashlib.md5()
  with open(f, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
      hasher.update(buf)
      buf = afile.read(BLOCKSIZE)
  return(hasher.hexdigest())


def get(remote, verbose):
  dlproc = subprocess.run(["dbxcli", "get", remote], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if verbose:
    try: 
      count, order = re.compile('/(\S+)\s(\S+)').match(dlproc.stderr.decode('utf-8')).group(1, 2)
      print("Downloaded " + remote +" "+ count + " " + order)
    except Exception:
      print("Downloaded " + remote)


def getr(remote, local, verify, verbose):
  localcwd = os.getcwd()
  os.chdir(local)
  #print("cwd: " + os.getcwd())
  regex = re.compile('^(\S+).*/(.+?)\s*$')
  proc = subprocess.run(["dbxcli", "ls", "-l", remote], stdout=subprocess.PIPE)
  lines = proc.stdout.decode('utf-8').splitlines()
  for line in lines[1:]:
    obj_id, obj_name = regex.match(line).group(1, 2)
    if obj_id == "-":
      os.mkdir(obj_name)
      if verbose: print("Created " + remote+'/'+obj_name)
      getr(remote+'/'+obj_name, obj_name, verify, verbose)
    else:
      if verify:
        myhash=None
        while True:
          get(remote+'/'+obj_name, verbose)
          chash = md5(obj_name)
          if myhash == chash:
            break
          else:
            myhash=chash
      else:
        get(remote+'/'+obj_name, verbose)

  os.chdir(localcwd)
