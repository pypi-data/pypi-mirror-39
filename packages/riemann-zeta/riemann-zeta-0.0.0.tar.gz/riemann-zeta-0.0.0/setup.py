# flake8: noqa

from setuptools import setup, find_packages

setup(
    name='riemann-zeta',
    version='0.0.0',
    description=('Ultra-minimal Bitcoin light client'),
    author='James Prestwich',
    author_email='james@summa.one',
    license='LGPLv3.0',
    install_requires=[],
    packages=find_packages(),
    keywords = 'bitcoin cryptocurrency blockchain',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security :: Cryptography',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
