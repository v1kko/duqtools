import logging
import sys
from pathlib import Path
from string import Template
from typing import Sequence

from ..config import Config
from ..utils import read_imas_handles_from_file

from math import prod

logger = logging.getLogger(__name__)

MAX_RUN = 9999

DUMMY_VARS = {
    'TEMPLATE_USER': 'user',
    'TEMPLATE_DB': 'db',
    'TEMPLATE_SHOT': 123,
    'TEMPLATE_RUN': 456,
    'RUNS_DIR': '.',
    'RUN_IN_START': 10,
    'RUN_OUT_START': 20,
}


class SetupError(Exception):
    ...


def _get_n_samples(cfg: Config) -> int:
    """Grab number of samples generated by this config, from
    1. `sampler.n_samples`
    2. As a product of the number of dimensions.
    """
    if not cfg.create:
        raise SetupError('Config has no section `create`.')

    try:
        n_samples = cfg.create.sampler.n_samples
    except AttributeError:
        matrix = (model.expand() for model in cfg.create.dimensions)
        n_samples = prod([len(model) for model in matrix])

    return n_samples


def setup(*, template_file, input_file, runs_dir, **kwargs):
    runs_dir = Path(runs_dir)
    cwd = Path.cwd()

    if not input_file:
        raise IOError('Input file not defined.')

    handles = read_imas_handles_from_file(input_file)

    with open(template_file) as f:
        template = Template(f.read())

    dummy_cfg = Config.parse_raw(template.substitute(DUMMY_VARS))

    n_samples = _get_n_samples(dummy_cfg)

    current_run_number = 0

    for name, handle in handles.items():

        run_in_start = current_run_number
        run_out_start = run_in_start + n_samples
        current_run_number = run_out_start + n_samples

        if current_run_number > MAX_RUN:
            raise ValueError(f'Cannot write data with run number > {MAX_RUN}')

        cfg = template.substitute(
            TEMPLATE_USER=handle.user,
            TEMPLATE_DB=handle.db,
            TEMPLATE_SHOT=handle.shot,
            TEMPLATE_RUN=handle.run,
            RUNS_DIR=runs_dir / name,
            RUN_IN_START=run_in_start,
            RUN_OUT_START=run_out_start,
        )

        Config.parse_raw(cfg)  # make sure config is valid

        out_drc = cwd / name
        out_drc.mkdir(exist_ok=False, parents=True)

        with open(out_drc / 'duqtools.yaml', 'w') as f:
            f.write(cfg)
