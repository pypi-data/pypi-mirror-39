# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 23:24:04 2014

@author: mwojc
"""
import numpy as np
from fempy.fields import tools
from fempy.domain.tools import cached_property, invalidate_caches
from fempy.fields.fields import Field


def transpose(a, *axes):
    '''
    Transposes only field axes
    '''
    if not isinstance(a, Field):
        return np.transpose(a, *axes)
    if a.sufix < 2:
        return a
    if len(axes) == 0:
        axes = tuple(reversed(a.saxes))
    axes = a.paxes + axes
    return np.transpose(a, axes)


def tensordot(a, b, axes=2):
    ap, af, bp, bf, rp = tools.get_prefixes(a, b)

    # If not fields make regular tensordot
    if ap == 0 and bp == 0:
        return np.tensordot(a, b, axes)

    # If there are fields use einsum
    pa = 'abcdefgh'[:ap]   # prefix
    pb = 'abcdefgh'[:bp]
    pr = 'abcdefgh'[:rp]
    sa = 'ijklmnop'[:af]   # sufix
    sb = 'qrstuvwx'[:bf]

    if isinstance(axes, int):
        axes = np.asarray([range(-axes, 0), range(0, axes)])
    else:
        axes = np.asarray(axes)
        if len(axes.shape) == 1:
            axes.shape = (2, 1)
    sar = sa
    sbr = sb
    for ai, bi in axes.T:
        sar = sar.replace(sa[ai], '')
        sbr = sbr.replace(sb[bi], '')
        sa = sa.replace(sa[ai], sb[bi])

    subscripts = '%s%s,%s%s->%s%s' % (pa, sa, pb, sb, pr, sar+sbr)
    r = np.einsum(subscripts, a, b)

    # Return type from field factory
    if hasattr(a, 'factory'):
        return a.factory(r)
    else:
        return b.factory(r)


def dot(a, b):
    # If not fields use regular np.dot
    if not isinstance(a, Field):
        if not isinstance(b, Field):
            return np.dot(a, b)
    # If fields use einsum (via tensordot)
    ap, af, bp, bf, rp = tools.get_prefixes(a, b)
    if af == 0 or bf == 0:  # scalar
        return tensordot(a, b, 0)
    if bf == 1:  # vector on the right
        return tensordot(a, b, 1)
    return tensordot(a, b, np.array([[-1], [-2]]))


def norm(a, ord=None, axis=None, keepdims=False):
    if not isinstance(a, Field):
        return np.linalg.norm(a, ord=ord, axis=axis, keepdims=keepdims)
    ax = a.saxes
    if axis is not None:
        ax = np.asarray(ax)[axis]
        if not isinstance(ax, (int, np.int, np.int64, np.int32, np.int8)):
            ax = tuple(ax)
    norm = np.linalg.norm(a, ord=ord, axis=ax, keepdims=keepdims)
    return a.factory(norm)


def normalize(a, ord=2, axis=-1):
    return a/norm(a, ord=ord, axis=axis, keepdims=True)


def flatten(a):
    return a.reshape(a.pshape + (np.prod(a.sshape, dtype=int),))


def identity_like(a):  # Valid for 2D fields
    n = a.sshape[-1]
    i = np.identity(n, dtype=a.dtype)
    return np.zeros_like(a) + i


def eye_like(a, k=0):  # Valid for 2D fields
    i = np.eye(*a.sshape, k=k, dtype=a.dtype)
    return np.zeros_like(a) + i


def psort(pvals, pvecs):
    M = np.prod(pvals.shape[:-1])
    N = pvals.shape[-1]
    ishape = pvals.shape[:-1] + (1,)
    #
    idx = np.argsort(-pvals)  # '-' is for descending order
    idx += np.arange(M).reshape(ishape)*N  # for sorting flattened array
    pvals = pvals.ravel()[idx]
    # pvecs = pvecs.reshape(M*N, -1)[idx]
    swap = np.swapaxes
    pvecs = swap(swap(pvecs, -1, -2).reshape(M*N, -1)[idx], -1, -2)
    return pvals, pvecs


def rotate(a, r):
    if isinstance(a, Field):
        r = a.factory(r)
        n = len(a.sshape)
    else:
        n = len(a.shape)
    if n == 0:  # scalar
        return a
    if n == 1:
        aprim = np.einsum('...ls,...s->...l', r, a)
    if n == 2:
        aprim = np.einsum('...kr,...ls,...rs->...kl',
                          r, r, a, optimize=True)
    if n == 3:
        aprim = np.einsum('...jq,...kr,...ls,...qrs->...jkl',
                          r, r, r, a, optimize=True)
    if n == 4:
        aprim = np.einsum('...ip,...jq,...kr,...ls,...pqrs->...ijkl',
                          r, r, r, r, a, optimize=True)
    if isinstance(a, Field):
        return a.factory(aprim)
    else:
        return a


class TensorCalc(object):
    def __init__(self, tensor=None):
        self.tensor = tensor

    @property
    def tensor(self):
        if not hasattr(self, '_tensor'):
            self._tensor = None
        if self._tensor is None:
            raise AttributeError("Set tensor first...")
        return self._tensor

    @tensor.setter
    def tensor(self, t):
        if t is not None:
            if not isinstance(t, Field):
                t = Field(t, len(t.shape) - 2)
            assert t.sufix == 2, 'Second rank tensor needed'
            assert t.shape[-2] == t.shape[-1], 'Second rank tensor needed'
            assert t.shape[-1] in (2, 3), '2D or 3D second rank tensor needed'
        self._tensor = t
        invalidate_caches(self)

    @cached_property
    def shape(self):
        return self.tensor.sshape

    @cached_property
    def T(self):
        return transpose(self.tensor)

    @cached_property
    def sym(self):
        return 0.5*(self.tensor + self.T)

    @cached_property
    def skew(self):
        return 0.5*(self.tensor - self.T)

    @cached_property
    def diag(self):
        t = self.tensor
        return np.diagonal(t, axis1=-2, axis2=-1)

    @cached_property
    def trace(self):
        t = self.tensor
        return np.trace(t, axis1=-2, axis2=-1)

    @cached_property
    def mean(self):
        trace = self.trace
        n = self.shape[-1]
        return trace/n

    @cached_property
    def dev(self):
        mean = self.mean
        dev = self.tensor.copy()
        n = self.shape[-1]
        for i in range(n):
            dev[..., i, i] -= mean
        return dev

    @cached_property
    def pvals(self):
        return self.eig[0]

    @cached_property
    def pvecs(self):
        return self.eig[1]

    @cached_property
    def kron(self):
        return eye_like(self.tensor)

    @cached_property
    def ptensor(self):
        pv = self.pvals  # possibly imaginary
        pt = np.zeros_like(self.tensor, dtype=pv.dtype)
        n = self.shape[-1]
        for i in range(n):
            pt[..., i, i] = pv[..., i]
        return pt

    @cached_property
    def polar(self):
        W, S, V = self.svd
        R = dot(W, V)
        VS = np.einsum('...ij,...i->...ij', V, S)  # S is diagonal
        U = dot(V, VS)
        return R, U

    @cached_property
    def svd(self):
        return np.linalg.svd(self.tensor)

    @cached_property
    def eig(self):
        return psort(*np.linalg.eig(self.tensor))

    @cached_property
    def inv(self):
        return np.linalg.inv(self.tensor)

    @cached_property
    def det(self):
        return np.linalg.det(self.tensor)

    @cached_property
    def I1(self):
        return self.trace

    @cached_property
    def I2(self):
        return 0.5*(self.trace**2 - self.tensordot(self.T))

    @cached_property
    def I3(self):
        return self.det

    @cached_property
    def _dev(self):
        return TensorCalc(self.dev)

    @cached_property
    def J2(self):
        return -self._dev.I2

    @cached_property
    def J3(self):
        return self._dev.I3

    @cached_property
    def sqrtJ2(self):
        return np.sqrt(self.J2)

    @cached_property
    def p(self):
        P = self.pvals
        return 0.5*(P[..., 0] + P[..., -1])

    @cached_property
    def q(self):
        P = self.pvals
        return 0.5*np.abs((P[..., 0] - P[..., -1]))

    @cached_property
    def b(self):
        P = self.pvals
        if self.shape[0] == 2:
            return 0.5
        return (P[..., 0] - P[..., 1])/(P[..., 0] - P[..., 2])

    @cached_property
    def a(self):
        return 2*self.b - 1.

    @cached_property
    def theta(self):
        return np.arctan(self.a/np.sqrt(3))

    def tensordot(self, other):
        return tensordot(self.tensor, other)

    def dot(self, other):
        return dot(self.tensor, other)


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
