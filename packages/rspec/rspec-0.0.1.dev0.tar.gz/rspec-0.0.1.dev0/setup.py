from os import path
from setuptools import find_packages, setup

cwd = path.abspath(path.dirname(__file__))

# get the long description from README.md
with open(path.join(cwd, "README.md"), encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    # published project name
    name="rspec",

    # from dev to release
    #   bumpversion release
    # to next version
    #   bump patch/minor/major
    version='0.0.1.dev',

    # one-line description for the summary field
    description="A Python image processing package for LLSM.",

    long_description=long_description,
    long_description_content_type='text/markdown',

    # project homepage
    url="https://github.com/liuyenting/rspec",

    # name or organization
    author="Liu, Yen-Ting",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research'
    ],

    keywords="",

    packages=find_packages(),

    python_requires='>=3.6',

    # other packages the build system would require during compilation
    setup_requires=[
    ],

    # other packages the project depends on to run
    #   install_requires -> necessity
    #   requirements.txt -> deployment (use conda environent.yml)
    install_requires=[
        # core
        'ipykernel',

        # numeric and processing
        'numpy',
        'scipy',
        'pandas',

        # database

        # plot
        'plotly',

        # utils
        'click',
        'coloredlogs',
        'tqdm'
    ],

    dependency_links=[
    ],

    # additional groups of dependencies here for the "extras" syntax
    extras_require={
    },

    # data files included in packages
    package_data={
    },
    # include all package data found implicitly
    #include_package_data=True,

    # data files outside of packages, installed into '<sys.prefix>/my_data'
    data_files=[
    ],

    # executable scripts
    entry_points={
        'console_scripts': [
        ]
    }
)