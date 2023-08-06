"""is the build script for setuptools. It tells setuptools about your """

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="pago46",
    version="0.0.2",
    author="Pago 46",
    author_email="admin@46degrees.net",
    maintainer='David Liencura',
    maintainer_email='dliencura@46degrees.net',
    description="Integraton package of pago46",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    keywords=['pago46', 'chile', 'payments'],
    install_requires=[
        'requests>=2.19.1',
    ],
    packages=setuptools.find_packages(),
    classifiers=(
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ),
    license='GPLv3'
)
