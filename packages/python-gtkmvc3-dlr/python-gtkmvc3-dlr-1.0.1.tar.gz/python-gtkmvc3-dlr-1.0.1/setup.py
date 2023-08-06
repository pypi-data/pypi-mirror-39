#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author: Ionutz Borcoman <borco@go.ro>
#
# ----------------------------------------------------------------------

import os

try:
    from setuptools import setup
except:
    from distutils.core import setup
    pass

from gtkmvc3 import get_version

root_path = os.path.dirname(os.path.abspath(__file__))

readme_file_path = os.path.join(root_path, "README")
with open(readme_file_path, "r") as f:
    long_description = f.read()

setup(name="python-gtkmvc3-dlr",
      version=".".join(map(str, get_version())), 
      description="Model-View-Controller and Observer patterns for developing pygtk-based applications",
      long_description=long_description,
      author="Roberto Cavada, Sebastian Brunner, Rico Belder, Franz Steinmetz",
      author_email="roboogle@gmail.com",
      maintainer='Sebastian Brunner',
      maintainer_email='sebastian.brunner@dlr.de',
      license="LGPL",
      url="https://github.com/roboogle/gtkmvc3/",
      keywords=('mvc', ),

      packages=['gtkmvc3', 'gtkmvc3.support', 'gtkmvc3.adapters', 'gtkmvc3.progen'],
      package_data={'gtkmvc3.progen': ['progen.ui']},
      scripts=['scripts/gtkmvc3-progen'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          ],
      
     )
