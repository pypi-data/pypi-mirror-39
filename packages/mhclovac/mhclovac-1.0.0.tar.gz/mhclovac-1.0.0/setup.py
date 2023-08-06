import setuptools
import os


readme_dir = os.path.dirname(__file__)
readme_path = os.path.join(readme_dir, 'README.md')
with open(readme_path, "r") as f:
    long_description = f.read()


required_packages = [
    "h5py",
    "numpy",
    "pandas",
    "python-dateutil",
    "scipy",
]


setuptools.setup(
    name="mhclovac",
    version="1.0.0",
    author="Stefan Stojanovic",
    author_email="stefs304@gmail.com",
    description="MHC binding prediction based on modeled "
                "physicochemical properties of peptides",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefs304/mhclovac",
    packages=[
        'mhclovac',
    ],
    package_data={
        'mhclovac': ['reference_data/*.hdf5'],
    },
    install_requires=required_packages,
    entry_points={
          'console_scripts': [
              "mhclovac-build=mhclovac.build_profile:main",
              "mhclovac=mhclovac.mhclovac_run:main",
          ]
    },
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry"
    )
)
