from distutils.core import setup

from babble import __version__, __author__, __contact__, __license__, __doc__

setup(name='babble',
      version=__version__,
      author=__author__,
      author_email=__contact__,
      packages=['babble', ],
      url='http://github.com/bear/babble/',
      license=__license__,
      description=__doc__,
      long_description=open('README.md').read(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
     )
