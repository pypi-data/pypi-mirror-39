from distutils.core import setup
setup(
  name='plugwise',
  packages=['plugwise'],
  version='0.2',
  license='MIT',
  description='A library for communicating with Plugwise smartplugs',
  author='Sven Petai',
  author_email='hadara@bsd.ee',
  url='https://bitbucket.org/hadara/python-plugwise/wiki/Home',
  download_url='https://github.com/cyberjunky/plugwise/archive/0.2.tar.gz',
  install_requires=[
        'crcmod',
        'pyserial',
  ],
  scripts=['plugwise_util'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)

