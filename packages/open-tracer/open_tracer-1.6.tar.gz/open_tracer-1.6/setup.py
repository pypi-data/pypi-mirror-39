from distutils.core import setup
setup(
  name = 'open_tracer',
  packages = ['open_tracer'],
  version = '1.6',
  license='MIT',
  description = 'Open-tracer : To trace every applications request',
  author = 'arun.rs',
  author_email = 'arunrs@uninstall.io',
  url = 'https://github.com/rsarun-uninstallio/open_tracer',
  download_url = 'https://github.com/rsarun-uninstallio/open_tracer/archive/v1.6.tar.gz',
  keywords = ['tracing', 'open_tracing', 'open_tracer'],
  install_requires=['uuid', 'requests', 'datetime', 'logging', 'mysqlclient'],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7',
  ],
)