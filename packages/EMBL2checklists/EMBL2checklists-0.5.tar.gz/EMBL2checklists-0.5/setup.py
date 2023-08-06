import os
import glob
import unittest
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='EMBL2checklists',
    version='0.5',
    author='Michael Gruenstaeudl, PhD',
    author_email='m.gruenstaeudl@fu-berlin.de',
    description='Converts EMBL- or GenBank-formatted flatfiles to submission checklists (i.e., tab-separated spreadsheets) for submission to ENA via the interactive Webin submission system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/michaelgruenstaeudl/EMBL2checklists',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
    keywords='novel DNA sequences, public sequence databases, European Nucleotide Archive, file conversion, data upload',
    license='BSD',
    entry_points={  # For automatic script generation
        'console_scripts': [
            'EMBL2checklists_CLI = EMBL2checklists.CLIOps:start_EMBL2checklists_CLI',
        ],
        'gui_scripts': [
            'EMBL2checklists_GUI = EMBL2checklists.GUIOps:start_EMBL2checklists_GUI',
        ]
    },
    packages=['EMBL2checklists'], # So that the subfolder 'EMBL2checklists' is read immediately.
    #packages = find_packages(),
    install_requires=['biopython', 'argparse'],
    scripts=glob.glob('scripts/*'),
    test_suite='setup.my_test_suite',
    include_package_data=True,
    zip_safe=False
)
