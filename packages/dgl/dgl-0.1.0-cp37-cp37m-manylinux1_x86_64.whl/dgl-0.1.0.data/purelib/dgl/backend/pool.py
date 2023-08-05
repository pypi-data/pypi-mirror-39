
import torch as T
import numpy as np
import numbers

class DGLTensorReference(object):
    def __init__(self, pool, index):
        self.pool = pool
        self.index = index

    @property
    def _value(self):
        return self.pool.get(self.index)

class DGLTensorPool(object):
    pools = {}
    def __new__(cls, dtype, shape):
        '''
        DGLTensorPool maintains a list of memory blocks.
        Each memory block is a tensor of dtype and shape
            [?] + shape

        The first dimension does not need to be the same for all
        blocks.
        '''
        if (dtype, shape) not in cls.pools:
            instance = object.__new__(cls)
            instance._dtype = dtype
            instance._shape = shape

            instance._blocks = []
            # the indices of each block in the concatenated tensor.
            # the last element is the number of tensors in the pool.
            instance._offsets = [0]

            cls.pools[(dtype, shape)] = instance
        return cls.pools[(dtype, shape)]

    def _getblock(self, index):
        for i in range(len(self._offsets) - 1):
            if self._offsets[i] <= index < self._offsets[i+1]:
                return i, index - self._offsets[i]

        raise ValueError(
                'index %d too big (%d tensors available)' %
                (index, self._offsets[-1])
                )

    def get(self, refs):
        '''
        Returns the subtensor indexed along the first dimension
        of the concatenated blocks

        refs: DGLTensorReference or list of DGLTensorReference
        '''
        if isinstance(refs, DGLTensorReference):
            block_idx, block_offset = self._getblock(refs.index)
            return self._blocks[block_idx][block_offset]
        else:
            index = T.from_numpy(np.array([r.index for r in refs]))
            return T.cat(self._blocks, 0)[index]

    def add(self, value):
        '''
        Add the tensors into the pool.

        Returns DGLTensorReferences
        '''
        self._blocks.append(value)
        self._offsets.append(value.shape[0])
