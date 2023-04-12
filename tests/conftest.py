import pytest

import os
from multiprocessing.managers import BaseManager
from queue import Queue

class QueueManager(BaseManager): pass

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