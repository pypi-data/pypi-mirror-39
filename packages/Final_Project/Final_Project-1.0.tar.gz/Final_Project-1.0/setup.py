from setuptools import setup

setup(
    name='Final_Project',
    version='1.0',
    description='Extracting home information from zillow.com',
    author='Disaiah Benentt',
    author_email='dlbennett365@students.ecsu.edu',
    url='http://dislbenn.github.io',
    #install_requires=['numpy>=1.14.0', 'biopython>=1.60'], # add the dependencies
    packages=['webcrawler',],
    package_dir={'':'src'},
    package_data={'webcrawler':['other/*']},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    scripts=['src/extract',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
)
