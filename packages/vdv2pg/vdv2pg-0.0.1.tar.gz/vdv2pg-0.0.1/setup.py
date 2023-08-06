import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'requirements.txt')) as f:
    requires = [line.strip() for line in f
                if len(line) > 1 and not line.startswith('#')]

setup(
    name='vdv2pg',
    version='0.0.1',
    url='https://github.com/geops/vdv2pg',
    description='Import VDV 451 files into a database',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Milan Oberkirch | geOps',
    author_email='milan.oberkirch@geops.de',
    keywords='vdv2pg sql database',
    license='MIT',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=['vdv2pg'],
    install_requires=requires,
    include_package_data=True,
    entry_points="""\
        [console_scripts]
        vdv2pg = vdv2pg:main
    """,
  )
