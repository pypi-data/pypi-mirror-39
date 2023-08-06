from setuptools import setup, find_packages
import os

version = '1.0.2'

setup(name='pp.connector.plone',
      version=version,
      description="Produce & Publisher Plone Client Connector",
      long_description=open(os.path.join("docs", "source", "README.rst")).read() + "\n" +
                       open(os.path.join("docs", "source", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Zope2",
        "Framework :: Zope :: 2",
        "Framework :: Zope :: 4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='PDF Plone Python EBook EPUB',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      url='http://pypi.python.org/pypi/pp.client.plone',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pp', 'pp.client'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
          'pp.client-python',
          'pp.core2',
          'furl',
          # -*- Extra requirements: -*-
      ],
      tests_require=['zope.testing'],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

