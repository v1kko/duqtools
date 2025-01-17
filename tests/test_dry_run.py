import os
import shutil
from pathlib import Path

import pytest
from pytest import TEST_DATA

from duqtools.cli import cli_clean, cli_create, cli_init, cli_plot, cli_submit
from duqtools.utils import work_directory

config_file = 'config_jetto.yaml'


@pytest.fixture(scope='session', autouse=True)
def extra_env():
    # Add required coverage env variable to each test
    os.environ['COVERAGE_PROCESS_START'] = str(Path.cwd() / 'setup.cfg')


@pytest.fixture(scope='session', autouse=True)
def collect_cov(cmdline_workdir):
    yield None
    # Executed at end of session, but before closure of cmdline_workdir
    for cov_file in cmdline_workdir.glob('.coverage.*'):
        shutil.copy(cov_file, Path.cwd())


@pytest.fixture(scope='session')
def cmdline_workdir(tmp_path_factory, request):
    # Create working directory for cmdline tests, and set up input files
    workdir = tmp_path_factory.mktemp('test_cmdline')
    (workdir / Path('workspace')).mkdir()
    shutil.copy(TEST_DATA / config_file, workdir / 'config.yaml')
    shutil.copytree(TEST_DATA / 'template_model',
                    workdir / Path('template_model'))
    return workdir


@pytest.mark.dependency()
def test_clean_database(cmdline_workdir):
    with work_directory(cmdline_workdir):
        cli_create(['-c', 'config.yaml', '--force', '--yes'],
                   standalone_mode=False)
        cli_clean(['-c', 'config.yaml', '--force', '--out', '--yes'],
                  standalone_mode=False)
        assert (not Path('./run_0000').exists())
        assert (not Path('./run_0001').exists())
        assert (not Path('./runs.yaml').exists())
        assert (Path('./runs.yaml.old').exists())


def test_init(cmdline_workdir):
    with work_directory(cmdline_workdir):
        cli_init(['--dry-run'], standalone_mode=False)
        assert (not Path('./duqtools.yaml').exists())


@pytest.mark.dependency(depends=['test_clean_database'])
def test_create(cmdline_workdir):
    with work_directory(cmdline_workdir):
        cli_create(['-c', 'config.yaml', '--dry-run', '--force'],
                   standalone_mode=False)
        assert (not Path('./run_0000').exists())
        assert (not Path('./run_0001').exists())
        assert (not Path('./runs.yaml').exists())


@pytest.mark.dependency(depends=['test_create'])
@pytest.mark.dependency()
def test_real_create(cmdline_workdir):
    with work_directory(cmdline_workdir):
        cli_create(['-c', 'config.yaml', '--force', '--yes'],
                   standalone_mode=False)
        assert (Path('./run_0000').exists())
        assert (Path('./run_0001').exists())
        assert (Path('./runs.yaml').exists())


@pytest.mark.dependency(depends=['test_real_create'])
def test_submit(cmdline_workdir):
    with work_directory(cmdline_workdir):
        cli_submit(['-c', 'config.yaml', '--dry-run'], standalone_mode=False)
        assert (not Path('./run_0000/duqtools.lock').exists())
        assert (not Path('./run_0001/duqtools.lock').exists())


@pytest.mark.xfail(reason='https://github.com/duqtools/duqtools/issues/257')
@pytest.mark.dependency(depends=['test_real_create'])
def test_plot(cmdline_workdir):
    with work_directory(cmdline_workdir):
        cli_plot([
            '-c',
            'config.yaml',
            '--dry-run',
            '-v',
            't_i_ave',
            '-h',
            'g2aho/jet/94875/1',
        ],
                 standalone_mode=False)
        assert (not Path('./chart.html').exists())
