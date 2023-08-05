# Copyright (C) 2016-2018 Barry A. Warsaw
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ast import NodeVisitor
from collections import namedtuple
from enum import Enum
from flufl.flake8 import __version__


class ImportType(Enum):
    non_from = 0
    from_import = 1
    future_import = 2


ImportRecord = namedtuple('ImportRecord', 'itype lineno colno, module, names')


U401_NONFROM_FOLLOWS_FROM = 'U401 Non-from import follows from-import'
U402_NONFROM_MULTIPLE_NAMES = 'U402 Multiple names on non-from import'
U403_NONFROM_SHORTER_FOLLOWS = 'U403 Shorter non-from import follows longer'
U404_NONFROM_ALPHA_UNSORTED = (
    'U404 Same-length non-from imports not sorted alphabetically')
U405_NONFROM_EXTRA_BLANK_LINE = (
    'U405 Unexpected blank line since last non-from import')
U406_NONFROM_DOTTED_UNSORTED = (
    'U406 Dotted non-from import not sorted alphabetically')

U411_FROMIMPORT_MISSING_BLANK_LINE = (
    'U411 Expected one blank line since last non-from import')
U412_FROMIMPORT_ALPHA_UNSORTED = 'U412 from-import not sorted alphabetically'
U413_FROMIMPORT_MULTIPLE = 'U413 Multiple from-imports of same module'
U414_FROMIMPORT_NAMES_UNSORTED = (
    'U414 from-imported names are not sorted alphabetically')
U415_FROMIMPORT_MISORDERED_FUTURE = (
    'U415 __future__ import appears after other imports')


class ImportVisitor(NodeVisitor):
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        if node.col_offset != 0:
            # Ignore nested imports.
            return
        names = [alias.name for alias in node.names]
        self.imports.append(
            ImportRecord(ImportType.non_from, node.lineno, node.col_offset,
                         None, names))

    def visit_ImportFrom(self, node):
        if node.col_offset != 0:
            # Ignore nested imports.
            return
        import_type = (ImportType.future_import
                       if node.module == '__future__'
                       else ImportType.from_import)
        names = [alias.name for alias in node.names]
        self.imports.append(
            ImportRecord(import_type, node.lineno, node.col_offset,
                         node.module, names))


class ImportOrder:
    name = 'flufl-import-order'
    version = __version__
    off_by_default = True

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def _error(self, record, error):
        code, space, text = error.partition(' ')
        return (record.lineno, record.colno,
                '{} {}'.format(code, text), ImportOrder)

    def run(self):
        visitor = ImportVisitor()
        visitor.visit(self.tree)
        last_import = None
        future_is_okay = True
        for record in visitor.imports:
            if record.itype is ImportType.future_import:
                if not future_is_okay:
                    yield self._error(
                        record, U415_FROMIMPORT_MISORDERED_FUTURE)
                continue
            if last_import is None:
                last_import = record
                continue
            if record.itype is ImportType.non_from:
                future_is_okay = False
                if len(record.names) != 1:
                    yield self._error(record, U402_NONFROM_MULTIPLE_NAMES)
                if last_import.itype is ImportType.from_import:
                    yield self._error(record, U401_NONFROM_FOLLOWS_FROM)
                # Shorter imports should always precede longer import *except*
                # when they are dotted imports and everything but the last
                # path component are the same.  In that case, they should be
                # sorted alphabetically.
                last_name = last_import.names[0]
                this_name = record.names[0]
                if '.' in last_name and '.' in this_name:
                    last_parts = last_name.split('.')
                    this_parts = this_name.split('.')
                    if (last_parts[:-1] == this_parts[:-1] and
                            last_parts[-1] > this_parts[-1]):
                        yield self._error(record, U406_NONFROM_DOTTED_UNSORTED)
                elif len(last_name) > len(this_name):
                    yield self._error(record, U403_NONFROM_SHORTER_FOLLOWS)
                # It's also possible that the imports are the same length, in
                # which case they must be sorted alphabetically.
                if (len(last_import.names[0]) == len(record.names[0]) and
                        last_import.names[0] > record.names[0]):
                    yield self._error(record, U404_NONFROM_ALPHA_UNSORTED)
                if last_import.lineno + 1 != record.lineno:
                    yield self._error(record, U406_NONFROM_DOTTED_UNSORTED)
            else:
                assert record.itype is ImportType.from_import
                future_is_okay = False
                if (last_import.itype is ImportType.non_from and
                        record.lineno != last_import.lineno + 2):
                    yield self._error(
                        record, U411_FROMIMPORT_MISSING_BLANK_LINE)
                if last_import.itype is ImportType.non_from:
                    last_import = record
                    continue
                if last_import.module > record.module:
                    yield self._error(record, U412_FROMIMPORT_ALPHA_UNSORTED)
                # All imports from the same module should show up in the same
                # multiline import.
                if last_import.module == record.module:
                    yield self._error(record, U413_FROMIMPORT_MULTIPLE)
                # Check the sort order of the imported names.
                if sorted(record.names) != record.names:
                    yield self._error(record, U414_FROMIMPORT_NAMES_UNSORTED)
                # How to check for no blank lines between from imports?
            # Update the last import.
            last_import = record
