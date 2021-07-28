from setuptools import setup, find_packages
  
# copied from https://github.com/awslabs/git-remote-codecommit/blob/master/setup.py
import os
def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


# follow https://github.com/awslabs/git-remote-codecommit/blob/master/setup.py
# and https://packaging.python.org/tutorials/packaging-projects/
setup(
    name='dbxcli_extras',
    version="0.0.3",
    license="WTFPL",
    author="Shadi Akiki",
    author_email="shadi.akiki@ronininstitute.org",
    url='https://www.teamshadi.net',
    description="dbxcli sync command that solves https://github.com/dropbox/dbxcli/issues/53",
    long_description = 'dbxcli sync command that solves https://github.com/dropbox/dbxcli/issues/53',
    long_description_content_type="text/markdown",

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      "click==7.1.2",
      "tqdm==4.56.0",
    ],
    entry_points='''
        [console_scripts]
        dbxcli_extras=dbxcli_extras.cli:cli
    ''',
)

