from setuptools import setup

setup(
    name='bam_reducers',
    version='0.1',
    packages=['bamreducers'],
    url='https://github.com/nijibabulu/bam_reducers',
    license='MIT',
    author='Bob Zimmermann',
    author_email='robert.zimmermann@univie.ac.at',
    scripts=['bin/bam_reducer.py',
             'bin/bam_downsampler.py',
             'bin/bam_splitter.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
    description='Reduce the size of BAM files',
    python_requires='>=3.6',
    install_requires=['pysam']
)
