#!/usr/bin/env python
"""
ncdiff

Command-Line Utility to show the differences between two NetCDF files

Copyright 2017, University Corporation for Atmospheric Research
LICENSE: See the LICENSE.rst file for details
"""

from os import linesep
from os.path import isfile
from argparse import ArgumentParser
from netCDF4 import Dataset, Dimension, Variable
from random import randint

#===================================================================================================
# Argument Parser
#===================================================================================================
__PARSER__ = ArgumentParser(description='Difference two NetCDF files')
__PARSER__.add_argument('--header', default=False, action='store_true',
                        help='Difference header information only')
__PARSER__.add_argument('-s', '--spot', default=10, type=int,
                        help='Number of spot checks in data to difference')
__PARSER__.add_argument('file1', type=str, help='Name of first NetCDF file')
__PARSER__.add_argument('file2', type=str, help='Name of second NetCDF file')


#===================================================================================================
# cli - Command-Line Interface
#===================================================================================================
def cli(argv=None):
    """
    Command-Line Interface
    """
    return __PARSER__.parse_args(argv)


#===================================================================================================
# _cmp - Comparison function
#===================================================================================================
def _cmp(a1,a2):
    if a1 is None or a2 is None:
        return True
    elif isinstance(a1, Dimension):
        if a1.name != a2.name:
            return True
        elif a1.size != a2.size:
            return True
        else:
            return a1.isunlimited() != a2.isunlimited()
    elif isinstance(a1, Variable):
        if a1.name != a2.name:
            return True
        elif a1.dtype != a2.dtype:
            return True
        else:
            return a1.dimensions != a2.dimensions
    else:
        return a1 != a2


#===================================================================================================
# _str - String producing function
#===================================================================================================
def _str(a):
    if a is None:
        return '-'*5
    elif isinstance(a, Dimension):
        return '{}({}{})'.format(a.name, a.size, '+' if a.isunlimited() else '')
    elif isinstance(a, Variable):
        dstr = '({})'.format(','.join(a.dimensions))
        return '{} {}{}'.format(a.dtype, a.name, dstr)
    else:
        return str(a)

        
#===================================================================================================
# diff_dicts
#===================================================================================================
def diff_dicts(d1, d2, name='object'):
    d12union = set.union(set(d1), set(d2))
    diffs = []
    for k in sorted(d12union):
        d1k = d1.get(k, None)
        d2k = d2.get(k, None)
        if _cmp(d1k, d2k):
            diffs.append((str(k), _str(d1k), _str(d2k)))
    if len(diffs) > 0:
        print
        print 'Differences found in {}:'.format(name)
        klen = max([len(ks) for ks, _, _ in diffs])
        d1len = max([len(d1s) for _, d1s, _ in diffs])
        d2len = max([len(d2s) for _, _, d2s in diffs])
        for ks, d1s, d2s in diffs:
            print ('   {:{kl}s}:  [1]   {:>{d1}s}  <--->  {:{d2}s}   '
                   '[2]'.format(ks, d1s, d2s, kl=klen, d1=d1len, d2=d2len))


#===================================================================================================
# _int_to_indices
#===================================================================================================
def _int_to_indices(n, shape):
    indices = []
    strides = reversed([reduce(lambda x,y: x*y, shape[:i], 1) for i in xrange(len(shape))])
    for s in strides:
        indices.append(n // s)
        n = n % s
    return tuple(reversed(indices))


#===================================================================================================
# _sample_indices
#===================================================================================================
def _sample_indices(shape):
    samples = []
    size = 2**len(shape)
    for i in xrange(size):
        samples.append(tuple([n*(s-1) for n,s in zip(_int_to_indices(i, [2]*size), shape)]))
    return samples

    
#===================================================================================================
# main - Main Program
#===================================================================================================
def main(argv=None):
    """
    Main program
    """
    args = cli(argv)

    FILE1 = args.file1
    if not isfile(FILE1):
        raise ValueError('NetCDF file {} not found'.format(FILE1))
    shortf1 = FILE1.split('/')[-1]

    FILE2 = args.file2
    if not isfile(FILE2):
        raise ValueError('NetCDF file {} not found'.format(FILE2))
    shortf2 = FILE2.split('/')[-1]

    ncf1 = Dataset(FILE1)
    ncf2 = Dataset(FILE2)
    
    print
    print '[1]:  {}'.format(shortf1)
    print '[2]:  {}'.format(shortf2)
    
    # Global file attributes
    f1atts = {a:ncf1.getncattr(a) for a in ncf1.ncattrs()}
    f2atts = {a:ncf2.getncattr(a) for a in ncf2.ncattrs()}
    diff_dicts(f1atts, f2atts, name='Global File Attributes')
    
    # Dimensions
    f1dims = {d:ncf1.dimensions[d] for d in ncf1.dimensions}
    f2dims = {d:ncf2.dimensions[d] for d in ncf2.dimensions}
    diff_dicts(f1dims, f2dims, name='File Dimensions')
    
    # Variable Header Info
    f1vars = {v:ncf1.variables[v] for v in ncf1.variables}
    f2vars = {v:ncf2.variables[v] for v in ncf2.variables}
    diff_dicts(f1vars, f2vars, name='Variable Headers')
    
    # Variable Data
    if not args.header:
        f12vars = [v for v in ncf1.variables if v in ncf2.variables]
        vars = [v for v in f12vars if ncf1.variables[v].shape == ncf2.variables[v].shape]
        for v in vars:
            v1 = ncf1.variables[v]
            v2 = ncf2.variables[v]
            v1data = {idx:v1[idx] for idx in _sample_indices(v1.shape)}
            v2data = {idx:v2[idx] for idx in _sample_indices(v2.shape)}
            diff_dicts(v1data, v2data, name='{!r} Data'.format(v))


#===================================================================================================
# Command-line Operation
#===================================================================================================
if __name__ == '__main__':
    main()
