from pathlib import Path
import os
from tqdm.auto import tqdm
from .dropbox_api import DropboxAPI


class DbxcliSync:
  def __init__(self, localdir: str, dbxdir: str, verbosity: int):
    assert verbosity in [0,1,2]
    # use str(Path(...)) for some cleanup
    self.localdir = str(Path(localdir))
    self.dbxdir = str(Path(dbxdir))
    self.verbosity = verbosity
    self.cache_dbx_dirls = {}
    self.dbxapi = DropboxAPI(verbosity)


  def sync_file(self, filename_local: str):
    filename_remote = os.path.join(self.dbxdir, filename_local.replace(self.localdir+"/", ""))

    # First, check in cache of dir listings
    fr_dir = os.path.dirname(filename_remote)
    if fr_dir not in self.cache_dbx_dirls.keys():
      ld_l = list(self.dbxapi.ls_dir(fr_dir))
      ld_l = [x[1] for x in ld_l if not x[0]] # filename only, no dirs
      self.cache_dbx_dirls[fr_dir] = ld_l


    if filename_remote.replace(fr_dir+"/", "") in self.cache_dbx_dirls.get(fr_dir, []):
      # file already exists in dropbox
      if self.verbosity>=1: print(f"File already exists in dropbox: {filename_remote}")
      return "exists in cache"

    # Update: it turns out that revs still shows a non-zero result for deleted files,
    # so using ls instead
    if self.dbxapi.exists(filename_remote):
      return "exists"

    if self.dbxapi.put(filename_local, filename_remote):
      return "uploaded"

    return "error in upload"


  def sync_dir(self):
    path_l = Path(self.localdir).rglob('*')
    path_l = sorted(path_l)
    if self.verbosity==0: path_l = tqdm(path_l)
    for path_i in path_l:
      if not path_i.is_file(): continue
      filename = str(path_i)
      r3 = self.sync_file(filename)
      if self.verbosity==2: print(f"{r3}: {filename}")
      #if r3=="uploaded": break
