import sys

from setuptools import setup
from pyultrasonic.__main__ import VERSION

if sys.version_info < (3,4):
    sys.exit('Sorry, Python < 3.4 is not supported')

#install_requires = list(val.strip() for val in open('requirements.txt'))
tests_require = list(val.strip() for val in open('test_requirements.txt'))

setup(name='pyultrasonic',
      version=VERSION,
      description='Retrieve distances using a Raspberry Pi with ultrasonic sensor HC-SR04',
      author='Richard Dubois',
      author_email='dubois.richard@gmail.com',
      url='https://github.com/richie256/pyultrasonic',
      package_data={'': ['LICENSE']},
      include_package_data=True,
      packages=['pyultrasonic'],
      entry_points={
          'console_scripts': [
              'pyultrasonic = pyultrasonic.__main__:main'
          ]
      },
      license='Apache 2.0',
      install_requires=['RPi.GPIO'],
      tests_require=tests_require,
      classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ]

)
