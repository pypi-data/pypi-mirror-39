import os
from distutils.core import setup


def read( file ):
    with open( os.path.join( os.path.dirname( __file__ ), file ) ) as f:
        return f.read()


setup(
    name='awebus',
    version='0.1dev',
    packages=[ 'awebus', ],
    license='MIT',
    description="Asynchronous Weak Event Bus",
    author="Daniel 'Vector' Kerr",
    author_email="admin@vector.id.au",
    url="https://gitlab.com/vectoridau/awebus",
    long_description=read( 'README.md' ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
