from multiprocessing.managers import BaseManager
from pathlib import Path

import cocotb
from cocotb_test.simulator import run

# A basic connection test


class QueueManager(BaseManager):
    pass


@cocotb.test()
async def connection(dut):
    print("\nInside cocotb\n")

    if "port" in cocotb.plusargs:
        port = cocotb.plusargs["port"]
        address = ("localhost", int(port))
        # address = ('localhost', 6001)
        print(f"\n{address=}\n")
        QueueManager.register("get_queue")
        m = QueueManager(address=address, authkey=b"cocotb")
        print("\nConnecting to manager\n")
        m.connect()
        print("\nConnected!\n")
        queue = m.get_queue()
        queue.put("\nhello from cocotb!\n")
    else:
        print("'port' plusarg not found...")

    # assert 1 == 0


def test_connection(cocotb_connection):
    verilog_sources = []
    vhdl_sources = []
    tests_path = Path(__file__).resolve().parent
    verilog_sources = [tests_path / "hdl" / "adder.sv"]

    port = cocotb_connection

    plus_args = [f"+port={port}"]

    try:
        run(
            verilog_sources=verilog_sources,
            vhdl_sources=vhdl_sources,
            toplevel="adder",
            module="test_connection",
            testcase="connection",
            work_dir=f"sim_build",
            sim_build=f"sim_build",
            plus_args=plus_args,
            timescale="1ns/1ps",
        )
    except SystemExit:
        print("Finished")
        raise AssertionError(f"System exited due to an error.")
        # raise AssertionError("Error to see stdout")


if __name__ == "__main__":
    test_connection()
