from setuptools import setup
from pyzonky import __version__

def readme():
    with open('README.rst') as f:
        return f.read()


# https://pypi.org/pypi?%3Aaction=list_classifiers
setup(name='pyzonky',
      version=__version__,
      description='',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='',
      url='',
      author='',
      author_email='',
      license='',
      packages=['pyzonky'],
      install_requires=[],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
)