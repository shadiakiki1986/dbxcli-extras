from pathlib import Path
import os
import subprocess
from tqdm.auto import tqdm


def my_run(cx):
    return subprocess.run(cx, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class DbxcliSync:
  def __init__(self, localdir: str, dbxdir: str, verbosity: int):
    assert verbosity in [0,1,2]
    # use str(Path(...)) for some cleanup
    self.localdir = str(Path(localdir))
    self.dbxdir = str(Path(dbxdir))
    self.verbosity = verbosity

  def sync_file(self, filename_local: str):
    filename_remote = filename_local.replace(self.localdir, self.dbxdir)
    #filename_remote = os.path.join(self.dbxdir, filename_remote)

    # Update: it turns out that revs still shows a non-zero result for deleted files,
    # so using ls instead
    c1_revs = ["dbxcli", "ls", filename_remote]
    if self.verbosity>=2: print(f"Command: {' '.join(c1_revs)}")
    r1 = my_run(c1_revs)
    if r1.returncode==0:
      if self.verbosity>=1: print(f"File already exists: {filename_local}")
      return "exists"

    c2_put = ['dbxcli', 'put', filename_local, filename_remote]
    if self.verbosity>=2: print(f"Command: {' '.join(c2_put)}")
    r2 = my_run(c2_put)
    if r2.returncode==0:
      if self.verbosity>=1: print(f"File uploaded: {filename_local}")
      return "uploaded"
    
    print(f"Got non-zero return code {r2.returncode}. Skipping file: {filename_local}")
    print(f"Full command: {c2_put}")
    return "error"

  def sync_dir(self):
    path_l = Path(self.localdir).rglob('*')
    path_l = sorted(path_l)
    if self.verbosity==0: path_l = tqdm(path_l)
    for path_i in path_l:
      if not path_i.is_file(): continue
      filename = str(path_i)
      r3 = self.sync_file(filename)
      #if r3=="uploaded": break

