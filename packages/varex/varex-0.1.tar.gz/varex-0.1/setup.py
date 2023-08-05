from setuptools import setup

setup(name='varex',
      version='0.1',
      description='Genomic variant explorer',
      long_description=open('README.rst').read(),
      author='Kate McKenzie',
      author_email='kate.j.mckenzie@gmail.com',
      url='http://github.com/Alaya/varex',
      download_url='https://github.com/Alaya/varex/archive/v0.1-alpha.tar.gz',
      license='MIT',
      py_modules=['varex'],
      install_requires=['flask'],
      classifiers=[
            'Framework :: Flask',
            'Topic :: Database :: Front-Ends',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Development Status :: 2 - Pre-Alpha',
            'Programming Language :: Python :: 3.7',
            'Intended Audience :: Science/Research'
      ],
      zip_safe=False)
