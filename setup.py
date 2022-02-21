from setuptools import setup, find_packages
  
# copied from https://github.com/awslabs/git-remote-codecommit/blob/master/setup.py
import os
def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


# follow https://github.com/awslabs/git-remote-codecommit/blob/master/setup.py
# and https://packaging.python.org/tutorials/packaging-projects/
setup(
    name='dbxcli_extras',
    version="0.0.8",
    license="WTFPL",
    author="Shadi Akiki",
    url='https://www.github.com/shadiakiki1986/dbxcli-extras',

    # Follow similar description and package name to git-extras
    # https://github.com/tj/git-extras
    description="dbxcli utilities: sync, recursive get",
    long_description = 'dbxcli utilities: sync, recursive get',
    long_description_content_type="text/markdown",

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      "click==7.1.2",
      "tqdm==4.56.0",
      "dropbox==11.22.0",
    ],
    entry_points='''
        [console_scripts]
        dbxcli_extras=dbxcli_extras.cli:cli
    ''',
)

