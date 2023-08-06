from setuptools import setup, find_packages

from exceptbool import __version__


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    author="Konrad Kocik",
    author_email='konrad.kocik@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Converts caught exception into bool value.",
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='except exception catching bool boolean decorator',
    name='exceptbool',
    packages=find_packages(include=['exceptbool']),
    test_suite='tests',
    tests_require=['pytest~=3.8.2', 'pytest-cov~=2.6.0', 'tox~=3.5.2', 'flake8~=3.5.0'],
    url='https://github.com/konrad-kocik/exceptbool',
    version=__version__,
    zip_safe=False,
)
