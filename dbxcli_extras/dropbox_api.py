import subprocess
import re
import click
import sys
from pathlib import Path
import os

class DropboxAPI:
  """
  Dropbox python API
  Update 2021-10-30: started using the python sdk and this class will eventually just become a pretty wrapper of it
  """
  def __init__(self, verbosity: int):
    self.verbosity=verbosity

    import json
    with open(os.path.join(Path.home(), ".config/dbxcli/auth.json"), "r") as fh: token=json.load(fh)[""]["personal"]
    import dropbox
    self.dbx = dropbox.Dropbox(token)


  def my_run(self, cx, stdout=subprocess.DEVNULL, nonzero_ok=False):
    if self.verbosity>=2: print(f"Command: {' '.join(cx)}")
    rx = subprocess.run(cx, capture_output=True)
    if rx.returncode==0 or nonzero_ok:
        return rx

    click.secho(f"Got non-zero return code {rx.returncode} from subcommand. Aborting.", fg="red")
    click.secho(f"Full command: {cx}", fg="red")
    click.secho(f"Error: {rx.stderr.decode()}", fg="red")
    sys.exit(1)


  def exists(self, filename_remote):
    l = list(self.ls_dir(filename_remote))
    assert len(l) in [0,1]
    if len(l)==0: return False
    #if self.verbosity>=1: print(f"File already exists in dropbox: {filename_remote}")
    return True


  def put(self, filename_local, filename_remote):
    c2_put = ['dbxcli', 'put', filename_local, filename_remote]
    r2 = self.my_run(c2_put)
    if r2.returncode==0:
      if self.verbosity>=1: print(f"File uploaded to dropbox: {filename_local}")
      return True

    print(f"Got non-zero return code {r2.returncode}. Skipping file: {filename_local}")
    print(f"Full command: {c2_put}")
    return False


  def ls_dir(self, fr_dir):
    """
    Copied from getr.py
    generator of filenames (not dirs) of contents of fr_dir
    Arguments:
      fr_dir - path on dropbox as per dbxcli, eg "/Pictures"
    """
    regex = re.compile('^(\S+).*/(.+?)\s*$')
    dlcmd = ["dbxcli", "ls", "-l", fr_dir]
    proc = self.my_run(dlcmd, stdout=subprocess.PIPE, nonzero_ok=True)
    if proc.returncode!=0: return []
    lines = proc.stdout.decode('utf-8').splitlines()
    for line in lines[1:]:
      obj_id, obj_name = regex.match(line).group(1, 2)
      yield obj_id=="-", obj_id, obj_name


  def drop_root_remote(self, x):
    return self._drop_root(self.dbxdir, x)

  def drop_root_local(self, x):
    return self._drop_root(self.localdir, x)

  def _drop_root(self, d, x):
    return re.sub(fr"^{d}", "", x)


  def rglob_all_remote(self, dbxdir):
      if self.verbosity>=2: print(f"Getting remote rglob(*) for: '{dbxdir}'")
      l = self.dbx.files_list_folder(dbxdir, recursive=True)
      import re
      while True:
        for e in l.entries:
            n_full = self.drop_root_remote(e.path_display) # (e.name, , e.path_display, e.path_lower)
            if not n_full: continue
            yield n_full

        if not l.has_more: break
        l = self.dbx.files_list_folder_continue(l.cursor)


  def hash_local(self, fn):
    from .dropbox_content_hasher import DropboxContentHasher
    hasher = DropboxContentHasher()
    with open(fn, 'rb') as f:
      while True:
        chunk = f.read(1024)  # or whatever chunk size you want
        if len(chunk) == 0: break
        hasher.update(chunk)
    return hasher.hexdigest()


  def hash_remote(self, fn):
    if self.verbosity>=2: print(f"Getting remote hash for {fn}")
    md = self.dbx.files_get_metadata(fn)
    #import os
    #mtime = os.path.getmtime(fullname)
    #mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
    #size = os.path.getsize(fullname)
    return md.content_hash


  def same_hash(self, filename_local, filename_remote):
      hash_r = self.hash_remote(filename_remote)
      hash_l = self.hash_local(filename_local)
      if self.verbosity>=2: print(f"Comparing hashes: '{hash_r}' =?= '{hash_l}'")
      return hash_r == hash_l
