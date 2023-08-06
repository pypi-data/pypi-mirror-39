# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 11:39:16 2014

@author: mwojc
"""
import numpy as np


class Field(np.ndarray):
    def __new__(cls, data, prefix=1, groups=None):
        data = np.asarray(data)
        shape = data.shape
        assert len(shape) >= prefix
        field = data.view(cls)
        field.prefix = prefix
        field.pshape = data.shape[:prefix]
        field.sshape = data.shape[prefix:]
        if not isinstance(groups, dict):
            groups = {}
        if not hasattr(cls, 'groups'):
            field.groups = groups
        return field

    def __array_finalize__(self, field):
        if field is None:
            return
        self.prefix = getattr(field, 'prefix', 1)
        self.pshape = getattr(field, 'pshape', ())
        self.sshape = getattr(field, 'sshape', ())
        if not hasattr(self.__class__, 'groups'):
            self.groups = getattr(field, 'groups', {})

    def __array_wrap__(self, out_arr, context=None):
        arr = out_arr.view(np.ndarray)
        if len(arr.shape) >= self.prefix:
            if arr.shape[:self.prefix] == self.pshape:
                arr = self.factory(arr)
        if arr.ndim == 0:
            arr = arr[()]
        return arr

    def __reduce__(self):
        # Get the parent's __reduce__ tuple
        pickled_state = super(Field, self).__reduce__()
        # Create our own tuple to pass to __setstate__  (with custom __dict__)
        new_state = pickled_state[2] + (self.__dict__,)
        # Return a tuple that replaces the parent's __setstate__ tuple
        # with our own
        return (pickled_state[0], pickled_state[1], new_state)

    def __setstate__(self, state):
        self.__dict__.update(state[-1])  # Recover __dict__
        # Call the parent's __setstate__ with the other tuple elements.
        super(Field, self).__setstate__(state[0:-1])

    def __getslice__(self, i, j):
        return np.ndarray.__getslice__(self, i, j).view(np.ndarray)

    def __getitem__(self, key):
        key = self._get_key(key)
        return np.ndarray.__getitem__(self, key).view(np.ndarray)
        # TODO: get subdomain here?

    def __setitem__(self, key, value):
        key = self._get_key(key)
        return np.ndarray.__setitem__(self, key, value)

    def _get_key(self, key):
        if isinstance(key, str):
            key = (key,)
        if isinstance(key, tuple) and isinstance(key[0], str):
            key = (self.groups[key[0]], ) + key[1:]
        return key

    @property
    def sufix(self):
        return len(self.shape) - self.prefix

    @property
    def ssize(self):
        return np.prod(self.sshape, dtype=int)

    @property
    def paxes(self):
        return tuple(range(self.prefix))

    @property
    def saxes(self):
        return tuple(range(self.prefix, len(self.shape)))

    def factory(self, data=None):
        if data is None:
            data = np.zeros(self.sshape)
        return self.__class__(data, prefix=self.prefix, groups=self.groups)


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
