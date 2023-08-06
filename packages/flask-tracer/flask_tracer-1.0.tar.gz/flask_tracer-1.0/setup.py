from distutils.core import setup

setup(
  name = 'flask_tracer',
  packages = ['flask_tracer'],
  version = '1.0',
  license='MIT',
  description = 'FlaskTracer : To trace every Flask request',
  author = 'Arjun Narayan',
  author_email = 'arjun@uninstall.io',
  url = 'https://github.com/rsarun-uninstallio/flask_tracer',
  download_url = 'https://github.com/rsarun-uninstallio/flask_tracer/archive/v1.0.tar.gz',
  keywords = ['tracing', 'flask_tracing', 'flask_tracer'],
  install_requires=['open_tracer'],
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
