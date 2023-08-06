# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 23:24:04 2014

@author: mwojc
"""

import numpy as np
from scipy import sparse
from fempy.fields.algebra import dot, transpose
from fempy.fields.fields import Field
from fempy.fields.nfields import nField, nScalar, nVector, nTensor, nTensor3, \
                                 nTensor4
from fempy.fields.gfields import gField, gScalar, gVector, gTensor, gTensor3, \
                                 gTensor4


class BaseOperator(Field):
    def __new__(cls, nfield, operator):
        assert isinstance(nfield, nField), "nField must be provided"
        f = nfield
        d = f.domain
        ne = d.nelem
        ng = d.etype.ngauss
        nn = d.etype.nnode
        prefix = len(f.shape) + 2  # +2 for gn
        assert operator.shape[:prefix] == (ne, ng, nn) + f.sshape
        operator = Field.__new__(cls, operator, prefix=prefix)
        operator.nfield = nfield
        return operator

    def __array_finalize__(self, op):
        if op is None:
            return
        Field.__array_finalize__(self, op)
        self.nfield = getattr(op, 'nfield', None)

    @property
    def groups(self):
        return self.field.domain.egroups

    @property
    def gfield(self):
        fs = 'abcdefgh'[:self.nfield.sufix]  # sshape of underlaying field
        os = 'pqrstuvw'[:self.sufix]  # sshape of operator (and values)
        vals = np.einsum('egn%s%s,en%s->eg%s' % (fs, os, fs, os),
                         self, onelems(self.nfield))
        return gField(self.nfield.domain, vals)

    def factory(self, data=None):
        if data is None:
            data = np.zeros(self.shape)
        op = self.copy()
        op[:] = data
        return op


class Operator(BaseOperator):
    def __new__(cls, field):
        f = field
        egn = f.domain.egn
        if f.sufix > 0:
            ss = f.sshape
            pss = np.prod(ss, dtype=int)
            op = np.zeros((pss, pss) + egn.shape)
            op[range(pss), range(pss)] = egn
            ax = list(range(len(op.shape)))
            op = op.transpose(ax[2:] + [0, 1])
            op = op.reshape(op.shape[:-2] + ss*2)
            egn = op
            # ss = f.sshape
            # eye = np.eye(np.prod(ss)).reshape(ss*2)
            # egn = np.einsum('egn...,...->egn...', egn, eye)
            # TODO: use numpy as_strided here for memory saving
        egn = BaseOperator.__new__(cls, field, egn)
        return egn
operator = Operator


class Nabla(BaseOperator):
    def __new__(cls, field):
        f = field
        egnk = f.domain.egnk
        if f.sufix > 0:
            ss = f.sshape
            pss = np.prod(ss, dtype=int)
            op = np.zeros((pss, pss) + egnk.shape)
            op[range(pss), range(pss)] = egnk
            ax = list(range(len(op.shape)))
            op = op.transpose(ax[2:-1] + [0, 1, -1])
            op = op.reshape(op.shape[:-3] + ss*2 + (op.shape[-1],))
            egnk = op
            # ss = f.sshape
            # eye = np.eye(np.prod(ss, dtype=int)).reshape(ss*2)
            # egnk = np.einsum('egnk...,...->egn...k', egnk, eye)
            # TODO: use numpy as_strided here for memory saving
        egnk = BaseOperator.__new__(cls, field, egnk)
        return egnk
nabla = Nabla


class SmallStrain(BaseOperator):
    def __new__(cls, field):
        assert isinstance(field, nVector), \
            "SmallStrain can only be applied to nVector"
        nbl = Nabla(field)
        sstr = 0.5*(nbl + transpose(nbl))
        sstr = sstr.view(cls)
        # egnk = BaseOperator.__new__(cls, field, egnk)
        return sstr
small_strain = SmallStrain


class SmallRotation(BaseOperator):
    def __new__(cls, field):
        assert isinstance(field, nVector), \
            "SmallRotation can only be applied to nVector"
        nbl = Nabla(field)
        sstr = 0.5*(nbl - transpose(nbl))
        sstr = sstr.view(cls)
        # egnk = BaseOperator.__new__(cls, field, egnk)
        return sstr
small_rotation = SmallRotation


class Divergence(BaseOperator):
    def __new__(cls, field):
        assert isinstance(field, (nVector, nTensor, nTensor3, nTensor4) +
                                 (gVector, gTensor, gTensor3, gTensor4)), \
            "Divergence can be computed for vectors and tensors only"
        nbl = Nabla(field)
        # dv = div(nbl)
        dv = np.einsum('egn...ii->egn...', nbl)  # just like in div
        dv = BaseOperator(field, dv)
        dv = dv.view(cls)
        return dv
divergence = Divergence


def onnodes(f, order=0, power=0):
    if isinstance(f, nField):
        return f
    # Get weights
    d = f.domain
    ec = d.ecoors
    gc = d.gcoors
    egni = np.einsum('eni,g->egni', ec, np.ones(d.etype.ngauss))
    egni = (egni.transpose(2, 0, 1, 3) - gc).transpose(1, 2, 0, 3)  # egni
    egn = np.linalg.norm(egni, axis=-1)  # egn, distance
    egn = 1./egn**power
    e1n = egn.sum(1, keepdims=True)
    egn = egn/e1n  # normalized weights
    # Calculate nodal values using weights
    en = np.einsum('eg...,egn...->en...', f, egn)
    n = nField(d, np.zeros(f.sshape))
    np.add.at(n, d.conec, en)  # assemble
    # And average them (not weighted here)
    n = dot(n, 1./d.ndeg)
    nres = n
    # if order > 1 calculate derivatives and update
    for i in range(order):
        egi = grad(nres)  # interpolated field derivatives (with shape func.)
        df = np.einsum('eg...i,egni->egn...', egi, egni)
        df = np.einsum('egn...,egn...->en...', df, egn)
        dn = nField(d, np.zeros(f.sshape))
        np.add.at(dn, d.conec, df)  # assemble
        dn = dot(dn, 1./d.ndeg)
        nres = n + dn
    return nres


def onelems(f):
    return onnodes(f)[f.domain.conec]


def ongauss(f):
    if isinstance(f, gField):
        eg = f
    else:
        # gn = domain.etype.gshp
        egn = f.domain.egn
        eg = np.einsum('egn...,en...->eg...', egn, onelems(f))
        eg = gField(f.domain, eg)
    return eg


def onboundary(f):
    assert isinstance(f, nField), "nField must be provided"
    b = f.domain.boundary
    return nField(b, f['boundary'])


def grad(f):
    egnk = f.domain.egnk
    egk = np.einsum('egnk...,en...->eg...k', egnk, onelems(f))
    return gField(f.domain, egk)


def div(f):
    # assert f.sufix and f.shape[-1] == f.domain.ndime, \
    #     "Last field axis must be equal to the domain dimension."
    assert isinstance(f, (nVector, nTensor, nTensor3, nTensor4) +
                         (gVector, gTensor, gTensor3, gTensor4)), \
        "Divergence can be computed for vectors and tensors only"
    g = grad(f)
    d = np.einsum('eg...ii->eg...', g)
    return gField(f.domain, d)


def integrate(f):
    # TODO: This function should be removed or renamed because its name is
    #       misleading. It actually assembles divergence of the field,
    #       equivalent to:
    #       lform(f, v=nabla(f))
    d = f.domain
    eg = dot(ongauss(f), d.gvol)  # to gauss points and multiply by volumes
    en = np.einsum('eg...k,egn...k->en...', eg, d.egnk)
    F = nField(d, np.zeros(f.sshape[:-1]))
    np.add.at(F, d.conec, en)  # assemble
#    if isinstance(f, gField):
#        print 'aaa'
#        fn = nField(f.domain, np.zeros(f.sshape))
#        print fn.shape
#    else:
#        fn = f
#    F = lform(f, nabla(fn))
    return F


def integrate2(f):
    f = ongauss(f)
    v = f.domain.gvol
    return np.einsum('eg...,eg->...', f, v)


def lform(f, v=None):
    # R_enA = F_egBA * N_egnAB
    # A = i_1 ... i_n
    # B = j_1 ... j_n
    d = f.domain
    # Use 'operator' by default
    if v is None:
        fn = f
        if isinstance(f, gField):
            fn = nField(f.domain, np.zeros(f.sshape))
        v = operator(fn)
    eg = dot(ongauss(f), d.gvol)  # to gauss points and multiply by volumes
    # TODO: checks for f, v shapes
    j = 'rstuvwxy'[:eg.sufix]
    subscripts = 'eg%s...,egn...%s->en...' % (j, j)
    en = np.einsum(subscripts, eg, v)  # integrate to nodes, to be assembled
    # Assemble
    F = np.zeros((d.eidx.nidx.g.na,) + en.shape[2:])
    np.add.at(F, d.eidx.conec_a, en)
    return F  # TODO: we should return nfield here


def lformu(f):
    d = f.domain
    gf = ongauss(f)
    gvals = np.einsum('eg...,eg->eg...', gf, d.gvol)
    evals = gvals.sum(1)
    envals = np.zeros((d.nelem, d.etype.nnode)+f.sshape)
    envals[:] = evals[:, None]/d.etype.nnode
    F = np.zeros((d.eidx.nidx.g.na,) + f.sshape)
    np.add.at(F, d.eidx.conec_a, envals)
    return F


def eij(u, v):
    as_strided = np.lib.stride_tricks.as_strided
    eipos1 = u.nfield.eipos
    m1, n1 = eipos1.shape
    sz = eipos1.itemsize
    eipos2 = v.nfield.eipos
    m2, n2 = eipos2.shape
    sz = eipos2.itemsize
    ei = as_strided(eipos1, shape=(m1, n1, n2), strides=(n1*sz, sz, 0))
    ej = as_strided(eipos2, shape=(m2, n1, n2), strides=(n2*sz, 0, sz))
    return ei, ej


def qform(A, u=None, v=None):
    d = A.domain
    # Use 'nabla' by default
    if u is None:
        An = A
        if isinstance(A, gField):
            An = nField(A.domain, np.zeros(A.sshape[A.sufix//2+1:]))
        u = nabla(An)
    if v is None:
        v = u
    if not isinstance(u, BaseOperator):
        u = BaseOperator(v.nfield, u)
    if not isinstance(v, BaseOperator):
        v = BaseOperator(u.nfield, v)
    # assert u.nfield is v.nfield
    # We are ready to integrate and assemble
    A = dot(ongauss(A), d.gvol)  # to gauss points and multiply by volumes
    # TODO: checks for A, u, v shapes
    i = 'abcd'[:u.nfield.sufix]
    j = 'fhyz'[:v.nfield.sufix]
    pq = 'ijklopq'[:u.sufix]
    rs = 'rstuvwx'[:v.sufix]
#    k = np.einsum('eg%s%s, egm%s%s, egn%s%s -> em%sn%s'
#                  % (pq, rs, i, pq, j, rs, i, j), A, u, v)  # SLOW!!!
    A = np.einsum('egm%s%s, eg%s%s -> egm%s%s' % (i, pq, pq, rs, i, rs), u, A)
    k = np.einsum('egm%s%s, egn%s%s -> em%sn%s' % (i, rs, j, rs, i, j), A, v)
    i, j = eij(u, v)  # u.nfield.eij
    shape = (u.nfield.nsize, v.nfield.nsize)
    k = k.ravel()
    i = i.ravel()
    j = j.ravel()
    K = sparse.coo_matrix((k, (i, j)), shape=shape).tocsc()  # assemble
    return K


def dirichlet(f):
    return f.__class__(f.domain, False)


if __name__ == '__main__':
    from fempy.testing import testmodule
    testmodule(__file__, '-v')
