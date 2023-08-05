"""
Module for wrapped MPI interfaces used in scaks.
"""

import logging
from itertools import chain
from functools import wraps

try:
    from mpi4py import MPI
    MPI_INSTALLED = True
except ImportError:
    MPI_INSTALLED = False

from .descriptors.descriptors import Property


class MPIUtil(object):
    ''' Higher level wrapper for MPI interfaces
    '''
    def __init__(self):
        logger_name = 'scaks.{}'.format(self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)

    def bcast(self, data):
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            bdata = mpi_comm.bcast(data, root=0)
        else:
            bdata = data
        return bdata

    def barrier(self):
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            mpi_comm.barrier()

    @Property
    def rank(self):
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            return mpi_comm.Get_rank()
        else:
            return 0

    @Property
    def size(self):
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            return mpi_comm.Get_size()
        else:
            return 1

    @Property
    def is_master(self):
        return self.rank == 0

    # Utility methods.
    def split_seq(self, sequence):
        ''' Split the sequence according to rank and processor number.

        :param sequence: The data sequence to be divided for parallel processing
        :type sequence: list
        '''
        starts = [i for i in range(0, len(sequence), len(sequence)//self.size)]
        ends = starts[1: ] + [len(sequence)]
        start, end = list(zip(starts, ends))[self.rank]

        return sequence[start: end]

    def split_size(self, size):
        ''' Split a size number(int) to sub-size number.

        :param size: The size to be splitted for each process
        :type size: int
        '''
        if size < self.size:
            warn_msg = ('Splitting size({}) is smaller than process ' +
                        'number({}), more processor would be ' +
                        'superflous').format(size, self.size)
            self._logger.warning(warn_msg)
            splited_sizes = [1]*size + [0]*(self.size - size)
        elif size % self.size != 0:
            residual = size % self.size
            splited_sizes = [size // self.size]*self.size
            for i in range(residual):
                splited_sizes[i] += 1
        else:
            splited_sizes = [size // self.size]*self.size

        return splited_sizes[self.rank]

    def merge_seq(self, seq):
        ''' Gather data in sub-process to root process.

        :param seq: Sequence to be merged
        :type seq: list
        '''
        if self.size == 1:
            return seq

        mpi_comm = MPI.COMM_WORLD
        merged_seq= mpi_comm.allgather(seq)
        return list(chain(*merged_seq))

mpi = MPIUtil()

def master_only(func):
    ''' Decorator to limit a function to be called only in master process in MPI env.
    '''
    @wraps(func)
    def _call_in_master_proc(*args, **kwargs):
        if mpi.is_master:
            return func(*args, **kwargs)

    return _call_in_master_proc

