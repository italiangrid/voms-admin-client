'''
Created on 23/ago/2011

@author: andreaceccanti

'''
import sys
sys.path.append("src")

from VOMSAdmin import __version__
from distutils.core import setup

SUMMARY="""
The voms-admin command line tool provides access to most common VOMS administrative operations.
"""

LONG_DES="""
The Virtual Organization Membership Service is a Grid attribute authority which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of their roles and other attributes in order to issue trusted attribute certificates
and assertions used in the Grid environment for authorization purposes.

The VOMS Admin service is a web application providing tools for administering the VOMS VO structure. It provides an intuitive web user interface for daily administration tasks

The voms-admin command line tool provides access to the most common VOMS Admin service administrative operations.
"""

setup(name='voms-admin-client',
      version='2.0.20',
      author="Andrea Ceccanti",
      author_email="andrea.ceccanti@cnaf.infn.it",
      maintainer="Andrea Ceccanti",
      maintainer_email="andrea.ceccanti@cnaf.infn.it",
      description=SUMMARY.strip(),
      long_description=SUMMARY.strip(),
      license="Apache Software License v. 2.0",
      url="http://italiangrid.github.com/voms/",
      package_dir={'':'src'},
      packages=['VOMSAdmin'],
      scripts=["src/voms-admin"],
      data_files=[('share/doc/voms-admin-client',['README.md', 'LICENSE', 'CHANGELOG']),
                  ('share/man/man1', ['doc/voms-admin.1'])])
