from setuptools import setup

setup(
    name="bayerstraits_16s",
    packages=['bayerstraits_16s'],
    version="1.0.5",
    description="Inferring traits by 16S",
    author='Anni Zhang',
    author_email='anniz44@mit.edu',
    url='https://github.com/caozhichongchong/BayersTraits_16S',
    keywords=['16S', 'bacterial genomes', 'function', 'traits'],
    license='MIT',
    #install_requires=['python>=3.0'],
    include_package_data=True,
    long_description=open('README.md').read(),
    package_dir={'bayerstraits_16s': 'bayerstraits_16s'},
    package_data={'bayerstraits_16s': ['scripts/*','data/*','example/*']},
    entry_points={'console_scripts': ['bayerstraits_16s = bayerstraits_16s.__main__:main']},
    #zip_safe=False,
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest'],
    classifiers=[
        #'Development Status :: 1 - Alpha',
        #'Intended Audience :: Bioinformatics and Researchers',
        #'License :: MIT',
        #'Operating System :: MacOS',
        #'Operating System :: Microsoft :: Windows',
        #'Operating System :: LINUX',
        'Programming Language :: Python :: 3',
        #'Topic :: Antibiotic resistance :: risk ranking',
        #'Topic :: Metagenomes :: Antibiotic resistance',
    ]
)
