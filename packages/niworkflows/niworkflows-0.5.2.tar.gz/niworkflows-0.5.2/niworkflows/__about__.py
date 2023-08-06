# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
These pipelines are developed by the Poldrack lab at Stanford University
(https://poldracklab.stanford.edu/) for use at
the Center for Reproducible Neuroscience (http://reproducibility.stanford.edu/),
as well as for open-source software distribution.
"""
from datetime import datetime
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__packagename__ = 'niworkflows'
__author__ = 'The CRN developers'
__copyright__ = 'Copyright {}, Center for Reproducible Neuroscience, Stanford University'.format(
    datetime.now().year)
__credits__ = ['Oscar Esteban', 'Ross Blair', 'Shoshana L. Berleant',
               'Christopher J. Markiewicz', 'Chris Gorgolewski',
               'Russell A. Poldrack']
__license__ = '3-clause BSD'
__maintainer__ = 'Oscar Esteban'
__email__ = 'code@oscaresteban.es'
__status__ = 'Prototype'

__description__ = """\
NeuroImaging Workflows provides processing tools for magnetic \
resonance images of the brain.\
"""
__longdesc__ = """\
NeuroImaging Workflows (NIWorkflows) is a selection of image processing workflows \
for magnetic resonance images of the brain. It is designed to provide an easily \
accessible, state-of-the-art interface that is robust to differences in scan \
acquisition protocols and that requires minimal user input. \
This open-source neuroimaging data processing tool is being developed as a part of \
the MRI image analysis and reproducibility platform offered by the CRN.\
"""
__url__ = 'https://github.com/poldracklab/{}'.format(__packagename__)

DOWNLOAD_URL = (
    'https://pypi.python.org/packages/source/{name[0]}/{name}/{name}-{ver}.tar.gz'.format(
        name=__packagename__, ver=__version__))
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

REQUIRES = [
    'nipype>=1.1.0',
    'nilearn>=0.2.6',
    'grabbit==0.2.3',
    'pybids==0.6.5',
    'sklearn',
    'pandas',
    'matplotlib',
    'jinja2',
    'svgutils',
    'seaborn',
    'packaging',
    'scikit-image',
    'scipy',
    'jinja2',
    'versioneer',
]

SETUP_REQUIRES = []
REQUIRES += SETUP_REQUIRES

LINKS_REQUIRES = []
TESTS_REQUIRES = ['mock', 'codecov', 'pytest-xdist', 'pytest']

EXTRA_REQUIRES = {
    'doc': ['sphinx'],
    'tests': TESTS_REQUIRES,
    'duecredit': ['duecredit']
}

# Enable a handle to install all extra dependencies at once
EXTRA_REQUIRES['all'] = list(EXTRA_REQUIRES.values())
