"""Setup script for din."""


# [ Imports:Python ]
import pathlib
import typing

# [ Imports:Third Party ]
import setuptools  # type: ignore


# [ Version ]
def _get_version() -> str:
    version_path = pathlib.Path(__file__).parent / 'version.py'
    version_code = version_path.read_text()
    version_state: typing.Dict[str, str] = {}
    # we own this code - executing it is fine
    # pylint: disable=exec-used
    exec(version_code, version_state)  # nosec
    # pylint: enable=exec-used
    return str(version_state['VERSION'])


VERSION = _get_version()


# [ Setup ]
setuptools.setup(
    # package name
    name='din',
    # package version
    version=VERSION,
    # short description
    description='Dunder Mixins',
    # the documentation displayed on pypi
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # not strictly necessary, but it's a good practice to provide a url if you have one (and you should)
    url='https://gitlab.com/toejough/din',
    # you.  you want attribution, don't you?
    author='toejough',
    # your email.  Or, *an* email.  If you supply an 'author', pypi requires you supply an email.
    author_email='toejough@gmail.com',
    # a license
    license='MIT',
    # "classifiers", for reasons.  Below is adapted from the official docs at https://packaging.python.org/en/latest/distributing.html#classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    # keywords.  because classifiers are for serious metadata only?
    keywords="dunder mixin equal equality repr str",
    # what packages are included.
    packages=setuptools.find_packages(),
    # minimum requirements for installation (third-party packages your package uses)
    install_requires=[
    ],
    # dependency links besides the package index
    dependency_links=[],
    # extras
    extras_require={
        'test': [
            'bandit',  # installed for bin
            'better_exceptions',
            'blessed',
            'click',
            'coverage',
            'flake8-assertive',  # imported by flake8 as plugin
            'flake8-author',  # imported by flake8 as plugin
            'flake8-blind-except',  # imported by flake8 as plugin
            'flake8-bugbear',  # imported by flake8 as plugin
            'flake8-builtins-unleashed',  # imported by flake8 as plugin
            'flake8-commas',  # imported by flake8 as plugin
            'flake8-comprehensions',  # imported by flake8 as plugin
            'flake8-copyright',  # imported by flake8 as plugin
            'flake8-debugger',  # imported by flake8 as plugin
            'flake8-docstrings',  # imported by flake8 as plugin
            'flake8-double-quotes',  # imported by flake8 as plugin
            'flake8-expandtab',  # imported by flake8 as plugin
            'flake8-imports',  # imported by flake8 as plugin
            'flake8-logging-format',  # imported by flake8 as plugin
            'flake8-mutable',  # imported by flake8 as plugin
            'flake8-pep257',  # imported by flake8 as plugin
            'flake8-self',  # imported by flake8 as plugin
            'flake8-single-quotes',  # imported by flake8 as plugin
            'flake8-super-call',  # imported by flake8 as plugin
            'flake8-tidy-imports',  # imported by flake8 as plugin
            'flake8-todo',  # imported by flake8 as plugin
            'flake8',  # installed for bin
            'mypy',  # installed for bin
            'mypy_extensions',
            'pylint',  # installed for bin
            'pipe',
            'vulture',  # installed for bin
        ],
        'dev': [
            'bpython==0.17.1',  # installed for bin
        ],
        'dist': [
            'setuptools',
            'wheel',
            'twine',
        ],
    },
    # if desired, include single files at the top level as packages via `py_modules=[<modules>]`
    py_modules=['din'],
)
