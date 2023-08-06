from setuptools import setup

setup(name='HBdataMonitor',
      version='1.0.0',
      description='Tool to visualize HB SQLite databases',
      url='https://github.com/menno94/HBdataMonitor',
      author='Menno de ridder',
      author_email='menno.deridder@deltares.nl',
	  long_description=open('README.md').read(),
	  long_description_content_type='text/markdown',
      license='MIT',
      packages=['HBdataMonitor'],
	  python_requires='>=3, <4',
      zip_safe=False)