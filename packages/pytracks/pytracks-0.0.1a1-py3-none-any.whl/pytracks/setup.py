from setuptools import setup

FTL_NAME = 'pytracks'
FTL_VERSION = '0.0.1'
FTL_URL = 'http://github.com/alexandrejaguar/pytracks'
FTL_DESCR = 'pytracks: Acquiring fission-tracks using image processing'
FTL_AUTHOR = 'Alexandre Fioravante de Siqueira'
FTL_EMAIL = 'siqueiraaf@gmail.com'
FTL_LIC = 'GNU GPL'

setup(name = FTL_NAME,
      version = FTL_VERSION,
      description = FTL_DESCR,
      url = FTL_URL,
      author = FTL_AUTHOR,
      author_email = FTL_EMAIL,
      license = FTL_LIC,
      packages = ['pytracks'],
      zip_safe = False)
