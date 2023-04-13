import pytest

import os
from multiprocessing.managers import BaseManager
from queue import Queue

def pytest_addoption(parser):
    group = parser.getgroup("pytest-cocotb")
    group.addoption(
        "--sim",
        "--simulator",
        action="store",
        dest="sim",
        default=None,
        help="sets the default SIM variable used by cocotb. eg. 'icarus', 'ghdl', etc.",
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
        help="Set this to 1 to enable wave traces dump for the Aldec Riviera-PRO and Mentor Graphics Questa simulators",
    )
    ## TODO: Add additional options. Might be nice to support all environment variables used by cocotb.


class QueueManager(BaseManager): pass

@pytest.fixture()
def sim(config):
    sim_val = config.getoption("sim")
    if sim_val is None:
        sim_val = os.getenv("SIM")
    os["SIM"] = sim_val
    return sim_val

@pytest.fixture(scope="session")
def cocotb_connection(worker_id):
    base_port = 4000
    if worker_id != "master":
        port_offset = int(worker_id[2:])
    else:
        port_offset = 0
    port = base_port + port_offset

    address = ('localhost', port)
    queue = Queue()
    class QueueManager(BaseManager): pass
    QueueManager.register('get_queue', callable=lambda:queue)
    manager = QueueManager(address=address, authkey=b'cocotb')
    manager.start()
    print(f"\nManager started on {port=}\n")
    queue = manager.get_queue()
    queue.put("\n\nhello from pytest fixture\n")

    yield port
    while not queue.empty():
        print(queue.get())
    manager.shutdown()
    print(f"\nShutting down manager on {port=}\n")


# Set SIM environment variable
# Default value if not set: questa
@pytest.fixture(autouse=True, scope="session")
def sim_env():
    sim = os.getenv("SIM", "icarus")
    os.environ['SIM'] = sim
    print(f"\n{sim=}\n")
    return