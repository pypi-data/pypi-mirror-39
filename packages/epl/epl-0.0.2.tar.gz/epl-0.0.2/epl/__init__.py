"""
epl (pronounced 'epple') provides enhanced package logistics
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

__all__ = ['__version__', '_version_t_', '_version_min_python_t_']
__status__ = 'Prototype'

import os
import sys

from epl.__version__ import __version__, _version_t_, _version_min_python_t_
from epl.virtual import EplEnvBuilder


def main(args=None):
    compatible = True
    if sys.version_info < tuple(_version_min_python_t_[:3]):
        compatible = False
    elif not hasattr(sys, 'base_prefix'):
        compatible = False
    if not compatible:
        min_python = '.'.join(map(str, tuple(_version_min_python_t_[:3])))
        raise ValueError('This script is only for use with '
                         f'Python {min_python} or later\n')
    else:
        import argparse

        parser = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]),
            description='Creates virtual Python environments in one or '
                        'more target directories.'
        )

        parser.add_argument(
            '--clear',
            default=False,
            action='store_true',
            dest='clear',
            help=('Delete the contents of the virtual environment directory'
                  'if it already exists, before virtual environment '
                  'creation.')
        )

        parser.add_argument(
            'dirs',
            metavar='ENV_DIR',
            nargs='+',
            help='A directory in which to create the virtual environment.'
        )

        parser.add_argument(
            '--no-pip',
            default=False,
            action='store_true',
            dest='nopip',
            help="Don't install pip in the virtual environment."
        )

        parser.add_argument(
            '--no-setuptools',
            default=False,
            action='store_true',
            dest='nodist',
            help="Don't install setuptools or pip in the virtual environment."
        )

        if os.name == 'nt':
            use_symlinks = False
        else:
            use_symlinks = True
        parser.add_argument(
            '--symlinks',
            default=use_symlinks,
            action='store_true',
            dest='symlinks',
            help='Try to use symlinks rather than copies, when symlinks '
                 'are not the default for the platform.'
        )

        parser.add_argument(
            '--system-site-packages',
            default=False,
            action='store_true',
            dest='system_site',
            help='Give the virtual environment access to the '
                 'system site-packages dir.'
        )

        parser.add_argument(
            '--upgrade',
            default=False,
            action='store_true',
            dest='upgrade',
            help='Upgrade the virtual environment directory to use this '
                 'version of Python, assuming Python has been upgraded '
                 'in-place.'
        )

        parser.add_argument(
            '--verbose',
            default=False,
            action='store_true',
            dest='verbose',
            help='Display the output from the scripts which '
                 'install setuptools and pip.'
        )

        options = parser.parse_args(args)

        if options.upgrade and options.clear:
            raise ValueError('you cannot supply --upgrade and '
                             '--clear together.')

        builder = EplEnvBuilder(
            system_site_packages=options.system_site,
            clear=options.clear,
            symlinks=options.symlinks,
            upgrade=options.upgrade,
            nodist=options.nodist,
            nopip=options.nopip,
            verbose=options.verbose
        )

        for d in options.dirs:
            builder.create(d)
