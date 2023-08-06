from os import path, getcwd
from os.path import join
from setuptools import setup

requirementPath = join(getcwd(), 'requirements.txt')
install_requires = []
if path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='geopackage-python',
    version='1.0.0.0',
    packages=['scripts', 'scripts.tools', 'scripts.common', 'scripts.tiling', 'scripts.packaging', 'scripts.geopackage',
              'scripts.geopackage.nsg', 'scripts.geopackage.nsg.resources', 'scripts.geopackage.srs',
              'scripts.geopackage.core', 'scripts.geopackage.tiles', 'scripts.geopackage.utility',
              'scripts.geopackage.extensions', 'scripts.geopackage.extensions.metadata',
              'scripts.geopackage.extensions.metadata.metadata_reference', 'scripts.geopackage.extensions.vector_tiles',
              'scripts.geopackage.extensions.vector_tiles.vector_fields',
              'scripts.geopackage.extensions.vector_tiles.vector_layers'
              ],
    url='https://gitlab.com/GitLabRGI/erdc/geopackage-python',
    license='The MIT License (MIT)',
    author='Jenifer Cochran',
    author_email='jenifer.cochran@rgi-corp.com',
    description=' Python-based tools for creating OGC GeoPackages.',
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
