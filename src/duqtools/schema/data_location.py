from typing import Optional

from pydantic import Field

from ._basemodel import BaseModel
from ._description_helpers import formatter as f


class DataLocation(BaseModel):
    """Specification for the data generated by the create step.

    When setting up a sequence of UQ runs, duqtools reads the source data from
    the template. For each individual UQ run needs, two locations must be
    defined.
        1. The location of the input data. This is where duqtools stores
        the modified source data.
        2. The location of the output data. The modelling software must know
        in advance where to store the results of the simulation.

    Input data are defined by `run_in_start_at`, and output data by
    `run_out_start_at`. A sequence is generated starting from these numbers.

    For example, with `run_in_start_at`: 7000 and `run_out_start_at`: 8000,
    the generated input stored at run number 7000 would correspond to output
    8000, 7001 to 8001, 7002 to 8002, etc.

    Note that these sequences may overlap with existing data sets. Duqtools
    will stop if it detects that data will be overwritten.
    """

    user: Optional[str] = Field(
        description='Username for the IMAS database to use,'
        ' defaults to current user')

    imasdb: str = Field(description='IMAS database or machine name.')

    run_in_start_at: int = Field(description=f("""
            The sequence of input data files start with this run number.
            """))

    run_out_start_at: int = Field(description=f("""
            The sequence of output data files start with this run number.
            """))
