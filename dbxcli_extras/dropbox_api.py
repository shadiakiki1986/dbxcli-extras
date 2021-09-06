import subprocess
import re

class DropboxAPI:
  """
  Dropbox python API
  """
  def __init__(self, verbosity: int):
    self.verbosity=verbosity


  def my_run(self, cx, stdout=subprocess.DEVNULL):
    if self.verbosity>=2: print(f"Command: {' '.join(cx)}")
    return subprocess.run(cx, stdout=stdout, stderr=subprocess.DEVNULL)


  def exists(self, filename_remote):
    # Update: it turns out that revs still shows a non-zero result for deleted files,
    # so using ls instead
    c1_revs = ["dbxcli", "ls", filename_remote]
    r1 = self.my_run(c1_revs)
    if r1.returncode==0:
      if self.verbosity>=1: print(f"File already exists in dropbox: {filename_remote}")
      return True
    return False


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
    if self.verbosity>=2: print(dlcmd)
    proc = self.my_run(dlcmd, stdout=subprocess.PIPE)
    lines = proc.stdout.decode('utf-8').splitlines()
    for line in lines[1:]:
      obj_id, obj_name = regex.match(line).group(1, 2)
      yield obj_id=="-", obj_name
