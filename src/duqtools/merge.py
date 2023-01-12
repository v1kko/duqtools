from __future__ import annotations

import logging

import click

from .config import var_lookup
from .ids import ImasHandle, merge_data
from .operations import op_queue
from .utils import read_imas_handles_from_file

logger = logging.getLogger(__name__)
info, debug = logger.info, logger.debug


def merge(*, merge_all: bool, target: str, template: str, handles: list[str],
          input_files: list[str], var_names: list[str] | None, force: bool,
          **kwargs):
    """Merge as many data as possible."""
    template = ImasHandle.from_string(template)
    target = ImasHandle.from_string(target)

    handles = [ImasHandle.from_string(handle) for handle in handles]
    for file in input_files:
        handles = handles + list(read_imas_handles_from_file(file).values())

    handles = set(handles)  # Remove duplicate handles

    for handle in handles:
        op_queue.add_no_op(description=click.style('Source for merge',
                                                   fg='green',
                                                   bold=False),
                           extra_description=f'{handle}')

    if merge_all:
        ids_variables = tuple(var_lookup.filter_type('IDS-variable').values())

        op_queue.add_no_op(description=click.style(
            'Merging all known variables', fg='green', bold=False))
    else:
        if not var_names or len(var_names) == 0:
            op_queue.add_no_op('No variables specified for merge', 'aborting')
            return

        ids_variables = tuple(var_lookup[name] for name in var_names)
        for variable in ids_variables:
            op_queue.add_no_op(description=click.style('Variable for merge',
                                                       fg='green',
                                                       bold=False),
                               extra_description=f'{variable.name}')

    op_queue.add(description=click.style('Template for merge',
                                         fg='green',
                                         bold=False),
                 extra_description=f'{template}')

    if target.exists() and not force:
        op_queue.add_no_op(description='Abort merge',
                           extra_description=f'{target} already exists, '
                           'use --force to overwrite')
        return

    template.copy_data_to(target)

    merge_data(handles, target, ids_variables)
