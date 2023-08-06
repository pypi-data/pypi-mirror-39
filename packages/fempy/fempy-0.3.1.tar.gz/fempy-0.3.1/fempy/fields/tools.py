# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 11:39:16 2014

@author: mwojc
"""
import numpy as np
from fempy.fields.fields import Field


def get_prefixes(a, b):
    if not isinstance(a, Field) and not isinstance(b, Field):
        a = np.asarray(a)
        b = np.asarray(b)
        ap = 0
        af = len(a.shape)
        bp = 0
        bf = len(b.shape)
        rp = 0
    elif isinstance(a, Field) and not isinstance(b, Field):
        b = np.asarray(b)
        ap = a.prefix
        af = a.sufix
        bp = 0
        bf = len(b.shape)
        if len(b.shape) >= ap:
            if b.shape[:ap] == a.pshape:
                bp = ap
                bf = len(b.shape[bp:])
        rp = ap
    elif not isinstance(a, Field) and isinstance(b, Field):
        a = np.asarray(a)
        bp = b.prefix
        bf = b.sufix
        ap = 0
        af = len(a.shape)
        if len(a.shape) >= bp:
            if a.shape[:bp] == b.pshape:
                ap = bp
                af = len(a.shape[ap:])
        rp = bp
    else:
        ap = a.prefix
        af = a.sufix
        bp = b.prefix
        bf = b.sufix
        if a.pshape != b.pshape:
            raise ValueError("Inconsistent fields: %s, %s)"
                             % (a.pshape, b.pshape))
        rp = ap
    return ap, af, bp, bf, rp


def is_matrix_field(a):
    return a.sufix == 2


def is_square_matrix_field(a):
    if is_matrix_field(a):
        return a.sshape[0] == a.sshape[1]
    return False


def is_broadcastable(shp1, shp2):
    for a, b in zip(shp1[::-1], shp2[::-1]):
        if a == 1 or b == 1 or a == b:
            pass
        else:
            return False
    return True
