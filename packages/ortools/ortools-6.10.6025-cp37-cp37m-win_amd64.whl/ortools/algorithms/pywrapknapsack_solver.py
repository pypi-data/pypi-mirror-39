# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_pywrapknapsack_solver')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_pywrapknapsack_solver')
    _pywrapknapsack_solver = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_pywrapknapsack_solver', [dirname(__file__)])
        except ImportError:
            import _pywrapknapsack_solver
            return _pywrapknapsack_solver
        try:
            _mod = imp.load_module('_pywrapknapsack_solver', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _pywrapknapsack_solver = swig_import_helper()
    del swig_import_helper
else:
    import _pywrapknapsack_solver
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _pywrapknapsack_solver.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _pywrapknapsack_solver.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _pywrapknapsack_solver.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _pywrapknapsack_solver.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _pywrapknapsack_solver.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _pywrapknapsack_solver.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _pywrapknapsack_solver.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _pywrapknapsack_solver.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _pywrapknapsack_solver.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _pywrapknapsack_solver.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _pywrapknapsack_solver.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _pywrapknapsack_solver.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _pywrapknapsack_solver.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _pywrapknapsack_solver.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _pywrapknapsack_solver.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _pywrapknapsack_solver.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _pywrapknapsack_solver.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _pywrapknapsack_solver.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class KnapsackSolver(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KnapsackSolver, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KnapsackSolver, name)
    __repr__ = _swig_repr
    KNAPSACK_BRUTE_FORCE_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_BRUTE_FORCE_SOLVER
    KNAPSACK_64ITEMS_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_64ITEMS_SOLVER
    KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER
    KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER
    KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER

    def __init__(self, *args):
        this = _pywrapknapsack_solver.new_KnapsackSolver(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _pywrapknapsack_solver.delete_KnapsackSolver
    __del__ = lambda self: None

    def Init(self, profits: 'std::vector< int64,std::allocator< int64 > > const &', weights: 'std::vector< std::vector< int64,std::allocator< int64 > >,std::allocator< std::vector< int64,std::allocator< int64 > > > > const &', capacities: 'std::vector< int64,std::allocator< int64 > > const &') -> "void":
        return _pywrapknapsack_solver.KnapsackSolver_Init(self, profits, weights, capacities)

    def Solve(self) -> "int64":
        return _pywrapknapsack_solver.KnapsackSolver_Solve(self)

    def BestSolutionContains(self, item_id: 'int') -> "bool":
        return _pywrapknapsack_solver.KnapsackSolver_BestSolutionContains(self, item_id)

    def set_use_reduction(self, use_reduction: 'bool') -> "void":
        return _pywrapknapsack_solver.KnapsackSolver_set_use_reduction(self, use_reduction)
KnapsackSolver_swigregister = _pywrapknapsack_solver.KnapsackSolver_swigregister
KnapsackSolver_swigregister(KnapsackSolver)

# This file is compatible with both classic and new-style classes.


