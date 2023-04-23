import os
from multiprocessing.managers import BaseManager

import pytest


def pytest_addoption(parser):
    group = parser.getgroup("pytest-cocotb")
    group.addoption(
        "--sim",
        "--simulator",
        action="store",
        dest="sim",
        default=None,
        help="sets the default SIM variable used by cocotb. \n\
              eg. 'icarus', 'ghdl', etc.",
    )
    group.addoption(
        "--top-level",
        action="store",
        dest="top-level",
        default=None,
        help="sets the top level of HDL that is used",
    )
    group.addoption(
        "--seed",
        "--random-seed",
        action="store",
        dest="seed",
        default=None,
        help="set the default seed that's used for test(s)",
    )
    group.addoption(
        "--cocotb-log-level",
        action="store",
        dest="cocotb-log-level",
        default=None,
        help="sets the log level used by cocotb",
    )
    group.addoption(
        "--gui",
        action="store",
        dest="gui",
        default=None,
        help="enables the use of a gui mode in simulator that support it",
    )
    group.addoption(
        "--waves",
        action="store",
        dest="waves",
        default=None,
        help="Set this to 1 to enable wave traces dump for \n\
              the Aldec Riviera-PRO and Mentor Graphics Questa simulators",
    )


"""
TODO: Add additional options. Might be nice to support
all environment variables used by cocotb.
"""


class QueueManager(BaseManager):
    pass


@pytest.fixture()
def sim(config):
    sim_val = config.getoption("sim")
    if sim_val is None:
        sim_val = os.getenv("SIM", "icarus")
    os.environ["SIM"] = sim_val
    return sim_val


# Set SIM environment variable
# Default value if not set: questa
@pytest.fixture(autouse=True, scope="session")
def sim_env():
    sim = os.getenv("SIM", "icarus")
    os.environ["SIM"] = sim
    print(f"\n{sim=}\n")
    return
