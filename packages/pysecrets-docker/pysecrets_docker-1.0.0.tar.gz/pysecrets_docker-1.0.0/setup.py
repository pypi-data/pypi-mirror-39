#!/usr/bin/env python

from setuptools import setup, find_packages

DESCRIPTION = "Docker secrets to ENV"

INSTALL_REQUIRES = open('requirements.txt', 'r').read()
INSTALL_REQUIRES = INSTALL_REQUIRES.split('\n')

EXTRAS_REQUIRE = {
    "docs": ["sphinx", "alabaster", "sphinxcontrib-embedly"],
    "tests": ["pytest", "tox", "coverage"],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["docs"]

setup(
    name="pysecrets_docker",
    version="1.0.0",
    description=DESCRIPTION,
    author="Luiz Oliveira",
    author_email="ziuloliveira@gmail.com",
    license="GPL3",
    platforms=["any"],
    packages=find_packages(),
    # test_suite="tests",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=2.7",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
