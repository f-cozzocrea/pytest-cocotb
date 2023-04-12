import cocotb
from cocotb_test.simulator import run
import pytest

from pathlib import Path
from multiprocessing.managers import BaseManager
from queue import Queue

# A basic connection test

class QueueManager(BaseManager): pass

@cocotb.test()
async def multiple_connections(dut):

    if "port" in cocotb.plusargs:
        port = cocotb.plusargs["port"]
        address = ('localhost', int(port))
        QueueManager.register('get_queue')
        m = QueueManager(address=address, authkey=b'cocotb')
        m.connect()
        queue = m.get_queue()
        print(f"{queue.get()}")
        queue.put("hello from cocotb!")
    else:
        print("'port' plusarg not found...")

    #assert 1 == 0

@pytest.mark.parametrize("parameters", [{"DATA_WIDTH": "8"}, {"DATA_WIDTH": "16"}, {"DATA_WIDTH": "32"}, {"DATA_WIDTH": "64"}])
@pytest.mark.parametrize("seed", range(64))
def test_multiple_connections(cocotb_connection, parameters, seed):
    verilog_sources = []
    vhdl_sources = []
    tests_path = Path(__file__).resolve().parent
    verilog_sources = [ tests_path / "hdl" / "adder.sv"]

    port = cocotb_connection

    plus_args = [f"+port={port}"]

    try:
        run(
            verilog_sources=verilog_sources,
            vhdl_sources=vhdl_sources,
            parameters=parameters,
            seed=seed,
            toplevel="adder",
            module="test_multiple_connections",
            testcase="multiple_connections",
            work_dir=f"sim_build",
            sim_build=f"sim_build",
            plus_args=plus_args,
            timescale="1ns/1ps"
        )
    except SystemExit:
        print("Finished")
        raise AssertionError("Error to see stdout")


if __name__ == "__main__":
    test_multiple_connections()