from distutils.core import setup
import py2exe

setup(console=['serverNew.py'], options={"py2exe":{"dist_dir": "server package"}})
setup(console=['clientNew.py'], options={"py2exe":{"dist_dir": "client package"}})