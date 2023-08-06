# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bin2fasta', 'bin2fasta.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'tqdm>=4.28,<5.0']

entry_points = \
{'console_scripts': ['bin2fasta = bin2fasta:main']}

setup_kwargs = {
    'name': 'bin2fasta',
    'version': '0.0.2',
    'description': 'Store any file as a fasta file',
    'long_description': "Disclaimer: this is only a proof-of-concept (and a joke), please don't actually use this.\n\n\n# bin2fasta\n\nStore any file as a fasta file!\n\n\n## Installation\n\n```bash\n$ pip install bin2fasta\n```\n\n\n## Usage\n\n```bash\n$ bin2fasta --help\nUsage: bin2fasta [OPTIONS] FILENAME\n\n  Store any file as a fasta file\n\nOptions:\n  -D, --decode           Enable conversion from FASTA to\n                         binary.\n  -o, --output FILENAME  File to write to.\n  --help                 Show this message and exit.\n```\n\nBasic example:\n```bash\n$ file foo.png\nfoo.png: PNG image data, 618 x 257, 8-bit/color RGBA, non-interlaced\n$ bin2fasta -o bar.fasta foo.png\n319400it [00:00, 683649.99it/s]\n$ head -c50 bar.fasta\n>Sequence_master\nAGTTGAGGCGCCTTACTGCCGAATTAGTTAAGA\n$ bin2fasta --decode -o baz.png bar.fasta\n159700it [00:00, 455825.67it/s]\n$ file baz.png\nbaz.png: PNG image data, 618 x 257, 8-bit/color RGBA, non-interlaced\n$ diff foo.png baz.png\n$\n```\n\nNote that you can easily chain multiple commands by piping their respective outputs and using `-`:\n```bash\n$ cat foo.png | xz | gpg -c | bin2fasta - > bar.fasta\n$ cat bar.fasta | bin2fasta -D - | gpg -d | xz --decompress > baz.png\n$ diff foo.png baz.png\n$\n```\n\n\n## Poetry workflow\n\nOnly relevant for [developers](https://poetry.eustace.io/docs/):\n\nRun executable:\n```bash\n$ poetry run bin2fasta\n```\n\nPublish to PyPi:\n```bash\n$ poetry --build publish\n```\n",
    'author': 'kpj',
    'author_email': 'kpjkpjkpjkpjkpjkpj@gmail.com',
    'url': 'https://github.com/kpj/bin2fasta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
