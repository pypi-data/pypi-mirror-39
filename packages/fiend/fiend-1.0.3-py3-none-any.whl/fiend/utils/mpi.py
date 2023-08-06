"""
Tools for working with mpi4py
"""

import hashlib

import numpy as np
from mpi4py import MPI


def get_num_nodes(comm: MPI.Comm):
    """Returns the number of different nodes in the 'comm'"""

    """The idea is to convert the hostnames to integer IDs and to check how
    many unique IDs we find."""
    mynamehash = hashlib.sha224(
        MPI.Get_processor_name().encode('utf-8')).digest()
    myid = int.from_bytes(mynamehash, byteorder='big', signed=True)
    ids = np.zeros(comm.size, dtype=object)
    ids[comm.rank] = myid
    ids = comm.allreduce(sendobj=ids, op=MPI.SUM)
    return len(np.unique(ids))


def get_num_processes_on_this_node(comm: MPI.Comm):
    """Returns the number of processes of 'comm' that share the same node as the querying process"""

    """The idea is to convert the hostnames to integer IDs and to check how
    many same IDs we find."""

    mynamehash = hashlib.sha224(
        MPI.Get_processor_name().encode('utf-8')).digest()
    myid = int.from_bytes(mynamehash, byteorder='big', signed=True)
    ids = np.zeros(comm.size, dtype=object)
    ids[comm.rank] = myid
    ids = comm.allreduce(sendobj=ids, op=MPI.SUM)
    return np.sum(ids == myid)
