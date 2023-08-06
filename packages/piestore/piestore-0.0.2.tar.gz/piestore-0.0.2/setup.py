"""
PieStore is A Python API for RESTful Store Services.
Copyright (C) 2018  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: one.chillindude@me.com
"""

from setuptools import setup, find_packages

from piestore.__version__ import __version__, _version_min_python_

with open("README.rst", "r") as fh:
    long_description = fh.read()

required = [
    "requests>=2.21.0"
]

setup(
    name='piestore',
    version=__version__,
    python_requires=f">={_version_min_python_}",
    install_requires=required,

    packages=find_packages(),

    license='AGPLv3',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Environment :: Web Environment",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],

    url='https://pypi.org/project/piestore/',
    author="Brian Farrell",
    author_email="one.chillindude@me.com",
    description="A Python API for RESTful Store Services",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords="interface",
    zip_safe=False,
)
