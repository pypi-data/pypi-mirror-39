import os
from setuptools import setup

requirements = [
    "sense_core>=0.0.5",
    "numpy>=1.15",
    "pypinyin>=0.33.1",
]

setup(
    name='sense-django',
    version='0.1',
    packages=[
            "sense_django",
    ],
    license='BSD License',  # example license
    description='sense django',
    install_requires=requirements,
    long_description=__doc__,
    url='',
    author='kafka0102',
    author_email='yujianjia@sensedeal.ai',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)