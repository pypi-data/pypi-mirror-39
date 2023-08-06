import io
import os
from setuptools import setup, find_packages


def local_file(*name):
    return os.path.join(
        os.path.dirname(__file__),
        *name)


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def read_version():
    """Read the `(version-string, version-info)` from
    `src/highlight_ranges/version.py`.
    """

    version_file = local_file(
        'src', 'highlight_ranges', 'version.py')
    local_vars = {}
    with open(version_file) as handle:
        exec(handle.read(), {}, local_vars)  # pylint: disable=exec-used
    return (local_vars['__version__'], local_vars['__version_info__'])


long_description = read(local_file('README.rst'), mode='rt')

setup(
    name='highlight_ranges',
    version=read_version()[0],
    packages=find_packages('src'),

    author='Sixty North AS',
    author_email='austin@sixty-north.com',
    description='Highlighting ranges in pygments',
    license='MIT',
    keywords='',
    url='http://github.com/sixty-north/highlight-ranges/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    platforms='any',
    include_package_data=True,
    package_dir={'': 'src'},
    # package_data={'highlight_ranges': ['data/*.css']},
    install_requires=[
        'pygments',
        'spor',
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax, for
    # example: $ pip install -e .[dev,test]
    extras_require={
        'dev': ['black', 'flake8', 'twine', 'wheel'],
        # 'doc': ['sphinx', 'cartouche'],
        'test': ['pytest'],
    },
    entry_points={
        'pygments.filters': [
            'highlight-ranges = highlight_ranges.filters:SporRangeFilter',
        ], 
        'pygments.styles': [
            'highlight-ranges-black-on-red = highlight_ranges.styles:BlackOnRed',
        ]
    },
    long_description=long_description,
)
