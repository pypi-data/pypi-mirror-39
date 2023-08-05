from setuptools import find_packages, setup

long_description = '''
Comparitve analysis of genome annotations.
'''

setup(name='companno',
      version='0.0.4',
      description='Comparative analysis of genome annotations.',
      long_description=long_description,
      author='Induja Chandrakumar',
      author_email='ic.induja@gmail.com',
      url='https://github.com/IC-Induja/companno',
      license='MIT',
      install_requires=['pandas>=0.23.4',
                        'six>=1.11.0',
                        'numpy>=1.15.1'],
      extras_require={
          'tests': ['pytest'],
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Healthcare Industry',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ],
      packages=find_packages(),
      package_dir={'companno': 'companno'},
      package_data={'companno': ['cognames.tsv']})
