from pathlib import Path
import os
from tqdm.auto import tqdm
from .dropbox_api import DropboxAPI


def morify(l):
  return ", ".join(l[:5]) + ("" if len(l)<=5 else f" (and {len(l)-5} more)")



class DbxcliSync:
  def __init__(self, localdir: str, dbxdir: str, verbosity: int):
    assert verbosity in [0,1,2]
    # use str(Path(...)) for some cleanup
    self.localdir = str(Path(localdir))
    if dbxdir[0]!="/": dbxdir="/"+dbxdir
    self.dbxdir = str(Path(dbxdir))
    self.verbosity = verbosity
    self.cache_dbx_dirls = {}
    self.dbxapi = DropboxAPI(verbosity)


  def sync_file(self, filename_local: str):
    fnr_noroot = filename_local.replace(self.localdir+"/", "")
    filename_remote = os.path.join(self.dbxdir, fnr_noroot)


    # First, check in cache of dir listings
    fr_dir = os.path.dirname(filename_remote)
    if fr_dir not in self.cache_dbx_dirls.keys():
      self.cache_dbx_dirls[fr_dir] = [obj_name for is_dir, _, obj_name in self.dbxapi.ls_dir(fr_dir) if not is_dir]

    fr_key = filename_remote.replace(fr_dir+"/", "")
    if fr_key in self.cache_dbx_dirls.get(fr_dir, []):
      # file already exists in dropbox
      if self.dbxapi.same_hash(filename_local, filename_remote):
        if self.verbosity>=1: print(f"File already exists in dropbox and hash is the same (checked from cache): {fnr_noroot}")
        return "exists in cache"

    # Update: it turns out that revs still shows a non-zero result for deleted files,
    # so using ls instead
    if self.dbxapi.exists(filename_remote):
      if self.dbxapi.same_hash(filename_local, filename_remote):
        if self.verbosity>=1: print(f"File already exists in dropbox and hash is the same (checked local file): {fnr_noroot}")
        return "exists"
      else:
        if self.verbosity>=1: print(f"File already exists in dropbox but content hash changed (checked local file): {fnr_noroot}")

    if self.dbxapi.put(filename_local, filename_remote):
      return "uploaded"

    return "error in upload"



  def sync_dir(self):
    path_l = Path(self.localdir).rglob('*')
    path_l = sorted(path_l)
    if self.verbosity==0: path_l = tqdm(path_l, desc="New/modified local files")
    for path_i in path_l:
      if not path_i.is_file(): continue
      filename = str(path_i)
      r3 = self.sync_file(filename)
      if self.verbosity==2: print(f"{r3}: {filename}")
      #if r3=="uploaded": break

    # check for deleted files locally and delete them remotely
    str_l_remote = list(self.dbxapi.rglob_all_remote(self.dbxdir))
    str_l_local  = [self.dbxapi.drop_root_local(str(x)) for x in path_l]
    if self.verbosity>=2:
        print(f"Remote files: {morify(str_l_remote)}")
        print(f"Local  files: {morify(str_l_local)}")

    fdel_l = sorted(list(set(str_l_remote).difference(set(str_l_local))))
    if self.verbosity==0: fdel_l = tqdm(fdel_l, desc="Locally deleted files")
    for fdel_i in fdel_l:
        fdel_i = self.dbxdir + fdel_i
        if self.verbosity>=1: print(f"Deleting remote file: '{fdel_i}'")
        self.dbxapi.dbx.files_delete(fdel_i)
