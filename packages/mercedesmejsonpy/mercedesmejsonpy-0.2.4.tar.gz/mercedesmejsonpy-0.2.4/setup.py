""" Setup configuration fo pypi

"""
from setuptools import setup
setup(
    name='mercedesmejsonpy',
    version='0.2.4',
    packages=['mercedesmejsonpy'],
    include_package_data=True,
    python_requires='>=3',
    license='WTFPL',
    description='A library to work with Mercedes Connected Vehicle API.',
    long_description='A library to work with Mercedes Connected Vehicle API.',
    author='Rene Nulsch',
    author_email='github.mercedesmejsonpy@nulsch.de',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
    ],
    install_requires=[
        'requests>=2.18.4'
    ]
)
