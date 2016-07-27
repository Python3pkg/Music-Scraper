import music_scrapper

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    from pkgutil import walk_packages


    def _find_packages(path='.', prefix=''):
        yield prefix
        prefix += "."
        for _, name, is_package in walk_packages(path,
                                                 prefix,
                                                 onerror=lambda x: x):
            if is_package:
                yield name


    def find_packages():
        return list(_find_packages(music_scrapper.__path__, music_scrapper.__name__))

setup(name='music_scrapper',
      version='0.0.1',
      install_requires=['scrapy >= 1.1.1'],
      description='Gets Songs from the web and allows users to download the same',
      url='',
      author='srivatsan-ramesh',
      author_email='sriramesh4@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['music_scrapper=music_scrapper.main:main'],
      },
      zip_safe=False)
