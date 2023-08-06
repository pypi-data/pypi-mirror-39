from setuptools import setup

setup(name='enduhub_downloader',
      version='0.2',
      description='Download  run results from https://enduhub.com/',
      url='https://github.com/mojek/enduhub_downloader',
      author='Michał Mojek',
      author_email='m.mojek@gmail.com',
      license='MIT',
      packages=['enduhub_downloader'],
      install_requires=[
          'requests',
          'beautifulsoup4'
      ],
      zip_safe=False)