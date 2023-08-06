
from setuptools import setup

setup(
    name = 'idefixx',
    packages = ['idefixx'],
    version = '0.15',  # Ideally should be same as your GitHub release tag varsion
    description = 'Identical image crosscheck',
    license = 'MIT',
    author = 'Roger van Daalen',
    author_email = 'roger@vandaalen.eu',
    url = 'https://github.com/rogervdf/idefix-ml/',
    download_url = 'https://github.com/rogervdf/idefix-ml/archive/0.15.tar.gz',
    install_requires=[            # I get to this in a second
          'opencv-python',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
