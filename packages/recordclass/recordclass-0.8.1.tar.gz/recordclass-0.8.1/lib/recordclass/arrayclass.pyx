#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3
#cython: embedsignature=True
#cython: initializedcheck=False

cimport cython
from cython cimport sizeof, pointer
from libc.string cimport memset
from cpython.object cimport Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_HEAPTYPE

cdef extern from "Python.h":
        
    ctypedef struct PyObject:
        Py_ssize_t ob_refcnt
        PyTypeObject *ob_type

    ctypedef PyObject * (*unaryfunc)(PyObject *)
    ctypedef PyObject * (*binaryfunc)(PyObject *, PyObject *)
    ctypedef PyObject * (*ternaryfunc)(PyObject *, PyObject *, PyObject *)
    ctypedef int (*inquiry)(PyObject *) except -1
    ctypedef Py_ssize_t (*lenfunc)(PyObject *) except -1
    ctypedef PyObject *(*ssizeargfunc)(PyObject *, Py_ssize_t)
    ctypedef PyObject *(*ssizessizeargfunc)(PyObject *, Py_ssize_t, Py_ssize_t)
    ctypedef int(*ssizeobjargproc)(PyObject *, Py_ssize_t, PyObject *)
    ctypedef int(*ssizessizeobjargproc)(PyObject *, Py_ssize_t, Py_ssize_t, PyObject *)
    ctypedef int(*objobjargproc)(PyObject *, PyObject *, PyObject *)

    ctypedef int (*objobjproc)(PyObject *, PyObject *)
    
    ctypedef PyObject *(*newfunc)(PyTypeObject *, PyObject *, PyObject *)
    ctypedef PyObject *(*allocfunc)(PyTypeObject *, Py_ssize_t)
    ctypedef int (*initproc)(PyObject *, PyObject *, PyObject *)
    
    ctypedef int (*visitproc)(PyObject *, void *) except -1
    ctypedef int (*traverseproc)(PyObject *, visitproc, void *) except -1
    #ctypedef int (*inquiry)(PyObject *) except -1
    ctypedef void (*freefunc)(void *)
    ctypedef void (*destructor)(PyObject *)
    
    #ctypedef void (*freefunc)(void *)
    #ctypedef void (*destructor)(PyObject *)

    ctypedef struct PySequenceMethods:
        lenfunc sq_length
        binaryfunc sq_concat
        ssizeargfunc sq_repeat
        ssizeargfunc sq_item
        void *was_sq_slice
        ssizeobjargproc sq_ass_item
        void *was_sq_ass_slice
        objobjproc sq_contains

        binaryfunc sq_inplace_concat
        ssizeargfunc sq_inplace_repeat


    ctypedef struct PyMappingMethods:
        lenfunc mp_length
        binaryfunc mp_subscript
        objobjargproc mp_ass_subscript

    ctypedef struct PyTypeObject:
        Py_ssize_t tp_basicsize
        Py_ssize_t tp_itemsize
        Py_ssize_t tp_dictoffset
        Py_ssize_t tp_weaklistoffset
        unsigned long tp_flags

        PyTypeObject *tp_base
        PyObject *tp_bases
        PyObject *tp_mro

        destructor tp_dealloc

        newfunc tp_new
        allocfunc tp_alloc
        initproc tp_init
        freefunc tp_free
        traverseproc tp_traverse
        inquiry tp_clear
        
        PySequenceMethods *tp_as_sequence
        PyMappingMethods *tp_as_mapping
        

    ctypedef struct PyHeapTypeObject:
        PyTypeObject ht_type
        PyObject *ht_name
        PyObject *ht_slots
        PyObject *ht_qualname
    
    cdef inline PyTypeObject* Py_TYPE(PyObject*)
    cdef inline void Py_INCREF(PyObject*)
    cdef inline void Py_DECREF(PyObject*)
    cdef inline void Py_XDECREF(PyObject*)
    cdef Py_ssize_t PyNumber_AsSsize_t(PyObject*, PyObject*) except? -1
    cdef PyObject* PyErr_Occurred()
    cdef PyObject* PyExc_IndexError
    cdef PyObject* PyExc_TypeError
    cdef PyObject* Py_None
    cdef void PyErr_SetString(PyObject*, char*)
    
    cdef inline void PyTuple_SET_ITEM(PyObject*, Py_ssize_t, PyObject*)
    cdef inline PyObject* PyTuple_GET_ITEM(PyObject*, Py_ssize_t)
    cdef PyObject* PyTuple_New(Py_ssize_t)
    
    cdef void PyType_Modified(PyTypeObject*)
    cdef bint PyType_IS_GC(PyTypeObject *o)

    void* PyObject_Malloc(size_t size)    
    
    cdef Py_ssize_t Py_SIZE(PyObject*)
    cdef void Py_CLEAR(PyObject*)
    
    cdef PyObject* _PyObject_GC_New(PyTypeObject*)
    cdef PyObject* _PyObject_GC_Malloc(size_t size)
    
    cdef void PyObject_INIT(PyObject *op, PyTypeObject *tp) 

    cdef PyObject* PyErr_NoMemory() except NULL
    
    cdef void PyObject_GC_Track(PyObject*)
    cdef void PyObject_GC_UnTrack(PyObject*)
    cdef void PyObject_GC_Del(void*)
    cdef void PyObject_Del(void*)

# cdef extern from "objimpl.h":
#     cdef void Py_VISIT(PyObject*)
    
from cpython.object cimport Py_TPFLAGS_HAVE_GC 

cdef inline int py_visit(PyObject *ob, visitproc visit, void *arg) except -1:
    cdef int vret
    if ob:
        vret = visit(ob, arg)
        if vret:
            return vret
    return 0

cdef PyObject* arrayclass_alloc(PyTypeObject *tp, Py_ssize_t n):
    cdef PyObject *op
    cdef Py_ssize_t size = tp.tp_basicsize
    cdef bint is_gc

    is_gc = PyType_IS_GC(tp)
    if is_gc:
        op = _PyObject_GC_Malloc(size)
    else:
        op = <PyObject*>PyObject_Malloc(size)

    if op == NULL:
        return PyErr_NoMemory()

    memset(op, 0, size)

    if tp.tp_flags and Py_TPFLAGS_HEAPTYPE:
        Py_INCREF(<PyObject*>tp)
    
    PyObject_INIT(op, tp)

    if is_gc:
        PyObject_GC_Track(op)

    return op

# cdef PyObject* arrayclass_new(PyTypeObject *tp, PyObject *args, PyObject *kwds):
#     cdef PyObject *op
#     cdef PyObject *val
#     cdef PyObject **items
#     cdef Py_ssize_t i, n, m, l
#     cdef tuple t
#     cdef dict kw
#     cdef tuple fields
    
#     op = tp.tp_alloc(tp, 0)
    
#     n = arrayclass_len(op)
#     items = arrayclass_items(op)
    
#     if args == NULL:
#         t = ()
#     elif type(<object>args) is tuple:
#         t = <tuple>args
#     else:
#         t = tuple(<object>args)
        
#     m = len(t)
    
#     if kwds:
#         if type(<object>kwds) is dict:
#             kw = <dict>kwds
#         else:
#             kw = dict(<object>kwds)
#         l = len(kw)
#     else:
#         kw = {}
#         l = 0
    
#     print(n, m, l, t, kw)
    
#     if n != m + l:
#         PyErr_SetString(PyExc_TypeError, "Invalid length of args")
#         return NULL
    
#     if m > 0:
#         for i in range(m):
#             val = PyTuple_GET_ITEM(<PyObject*>t, i)
#             Py_INCREF(val)
#             items[i] = val
    
    
#     if l:
#         _fields = (<object>tp)._fields
#         if type(_fields) is tuple:
#             fields = <tuple>_fields
#         else:
#             fields = tuple(_fields)
        
#         for i in range(m, n):
#             key = fields[i]
#             if key not in kw:
#                 raise TypeError('Invalid keyword argument ' + key)
#             val = <PyObject*>kw[fields[i]] 
#             Py_INCREF(val)
#             items[i] = val
    
#     return op

cdef void arrayclass_free(void *op):
    if PyType_IS_GC(Py_TYPE(<PyObject*>op)):
        PyObject_GC_UnTrack(<PyObject*>op)
        PyObject_GC_Del(<PyObject*>op)
    else:
        PyObject_Del(<PyObject*>op)
    

cdef inline PyObject** arrayclass_items(PyObject *op):
    return <PyObject**>(<char*>op + sizeof(PyObject))    

cdef inline PyObject** arrayclass_dictptr(PyObject *op, PyTypeObject *tp):
    return <PyObject**>(<char*>op + tp.tp_dictoffset)

cdef inline PyObject** arrayclass_weaklistptr(PyObject *op, PyTypeObject *tp):
    return <PyObject**>(<char*>op + tp.tp_weaklistoffset)    

cdef inline Py_ssize_t arrayclass_len(PyObject *op):
    cdef PyTypeObject *tp = Py_TYPE(op)
    cdef Py_ssize_t size
    
    size = (tp.tp_basicsize - sizeof(PyObject))//sizeof(PyObject*)
    if tp.tp_dictoffset != 0:
        size -= 1
        
    return size

cdef inline PyObject* arrayclass_item(PyObject *op, Py_ssize_t i):
    cdef Py_ssize_t n
    cdef PyObject* val
    cdef PyObject **items

    n = arrayclass_len(op)
    items = arrayclass_items(op)
    
    if i < 0:
        i += n
    if i < 0 or i >= n:
        PyErr_SetString(PyExc_IndexError, "index out of range")
        return NULL

    val = items[i]
    Py_INCREF(val)
    return val

cdef inline int arrayclass_ass_item(PyObject *op, Py_ssize_t i, PyObject *val):
    cdef Py_ssize_t n
    cdef PyObject **items

    n = arrayclass_len(op)
    items = arrayclass_items(op)
    
    if i < 0:
        i += n
    if i < 0 or i >= n:
        PyErr_SetString(PyExc_IndexError, "index out of range")
        return 0

    Py_INCREF(val)
    items[i] = val
    return 0

cdef inline PyObject* arrayclass_subscript(PyObject *op, PyObject *ind):
    cdef PyObject *val
    cdef Py_ssize_t i, n
    cdef PyObject **items

    n = arrayclass_len(op)
    items = arrayclass_items(op)
    
    i = PyNumber_AsSsize_t(ind, <PyObject*>PyExc_IndexError)
    if i < 0:
        i += n
    if i >= n or i < 0:
        PyErr_SetString(PyExc_IndexError, "index out of range")
        return NULL        

    val = items[i]
    Py_INCREF(val)
    return val

cdef inline int arrayclass_ass_subscript(PyObject *op, PyObject *ind, PyObject *val):
    cdef Py_ssize_t i, n
    cdef PyObject **items

    n = arrayclass_len(op)
    items = arrayclass_items(op)

    i = PyNumber_AsSsize_t(ind, <PyObject*>PyExc_IndexError)
    if i < 0:
        i += n
    if i >= n or i < 0:
        PyErr_SetString(PyExc_IndexError, "index out of range")
        return 0

    Py_INCREF(val)
    items[i] = val
    return 0

cdef inline int arrayclass_clear(PyObject *op) except -1:
    cdef PyObject **items
    cdef PyObject **temp
    cdef PyObject *ob
    cdef PyTypeObject *tp = Py_TYPE(op)
    cdef Py_ssize_t i, n

    n = arrayclass_len(op)
    items = arrayclass_items(op)    

    for i in range(n):
        ob = items[i]
        Py_XDECREF(ob)
        Py_INCREF(Py_None)
        items[i] = Py_None

    if tp.tp_dictoffset != 0:
        temp = arrayclass_dictptr(op, tp)
        ob = temp[0]
        Py_XDECREF(ob)
        temp[0] = Py_None
        Py_INCREF(Py_None)
    if tp.tp_weaklistoffset != 0:
        temp = arrayclass_weaklistptr(op, tp)
        ob = temp[0]
        Py_XDECREF(ob)
        temp[0] = Py_None
        Py_INCREF(Py_None)
        
    return 0

# cdef inline void arrayclass_dealloc(PyObject *op):
#     cdef PyObject **items, *temp
#     cdef PyTypeObject *tp
#     cdef Py_ssize_t i, n

#     tp = Py_TYPE(op)
#     n = arrayclass_len(op)

#     if PyType_IS_GC(tp):
#         PyObject_GC_UnTrack(op)
        
#     items = arrayclass_items(op)    
#     for i in range(n):
#         Py_CLEAR(items[i])

#     if tp.tp_dictoffset != 0:
#         temp = <PyObject*>arrayclass_dictptr(op, tp)
#         Py_CLEAR(temp)
# #     if tp.tp_weaklistoffset != 0:
# #         temp = arrayclass_weaklistptr(op, tp)
# #         Py_CLEAR(temp)

#     if PyType_IS_GC(tp):
#         PyObject_GC_Del(op)
#     else:
#         PyObject_Del(op)
    
    
cdef inline int arrayclass_traverse(PyObject *op, visitproc visit, void *arg) except -1:
    cdef PyTypeObject *tp = Py_TYPE(op)
    cdef PyObject **items
    cdef PyObject **temp
    cdef PyObject *ob
    cdef PyObject *v
    cdef Py_ssize_t i, n
    cdef int vret

    n = arrayclass_len(op)

    items = arrayclass_items(op)    

    for i in range(n):
        ob = items[i]
        if ob:
            vret = visit(ob, arg)
            if vret:
                return vret

    if tp.tp_dictoffset != 0:
        temp = arrayclass_dictptr(op, tp)
        obj = <object>temp[0]
        for key in obj:
            v = <PyObject*>obj[key]
            if v:
                vret = visit(v, arg)
                if vret:
                    return vret
#     if tp.tp_weaklistoffset != 0:
#         temp = arrayclass_weaklist(op, tp)
#         ob = temp[0]
#         py_visit(ob, visit, arg)

    return 0

@cython.auto_pickle(False)
cdef class ArrayClass:
    
    def __cinit__(self, *args, **kw):
        cdef PyObject *op=<PyObject*>self
        cdef PyObject **items
        cdef PyTypeObject *tp = Py_TYPE(op)
        cdef PyObject **dictptr
        cdef PyObject *v
        cdef Py_ssize_t i, n
        cdef tuple t

        n = arrayclass_len(op)
        items = arrayclass_items(op)

        if type(args) is tuple:
            t = args
        else:
            t = tuple(args)

        if n != len(t):
            raise TypeError("Invalid length of args")

        if n > 0:
            v = items[0]
            Py_XDECREF(v)
            for i in range(n):
                v = PyTuple_GET_ITEM(<PyObject*>t, i)
                Py_INCREF(v)
                items[i] = v
                
        if tp.tp_dictoffset != 0:
            dictptr = arrayclass_dictptr(op, tp)
            vv = {}
            Py_INCREF(<PyObject*>vv)
            dictptr[0] = <PyObject*>vv

    def __dealloc__(self):
        cdef PyObject* op = <PyObject*>self
        cdef PyTypeObject *tp = Py_TYPE(op)
        cdef PyObject **items
        cdef PyObject *v
        cdef Py_ssize_t i, n

        n = arrayclass_len(op)

        if n > 0:
            items = arrayclass_items(op)    
            for i in range(0,n):
                Py_CLEAR(items[i])

        if tp.tp_dictoffset != 0:
            dictptr = arrayclass_dictptr(op, tp)
            v = dictptr[0]
            Py_XDECREF(v)
            dictptr[0] = NULL
        
    def __getitem__(ob, ind):
        cdef PyObject* op = <PyObject*>ob
        cdef PyObject** items
        cdef PyObject *o
        cdef Py_ssize_t i, n

        n = arrayclass_len(op)
        items = arrayclass_items(op)
                
        i = PyNumber_AsSsize_t(<PyObject*>ind, <PyObject*>PyExc_IndexError)
        if i < 0:
            i += n
        if i >= n or i < 0:
            raise IndexError('Index %s out of range' % i)
            
        o = items[i]
        Py_INCREF(o)
        return <object>o
    
    def __setitem__(ob, ind, val):
        cdef PyObject* op = <PyObject*>ob
        cdef PyObject** items
        cdef Py_ssize_t i, n

        n = arrayclass_len(op)
        items = arrayclass_items(op)

        i = PyNumber_AsSsize_t(<PyObject*>ind, <PyObject*>PyExc_IndexError)
        if i < 0:
            i += n
        if i >= n or i < 0:
            raise IndexError('Index %s out of range' % i)
        
        items[i] = <PyObject*>val
        Py_INCREF(<PyObject*>val)
    
    def _astuple(ob):
        n = len(ob)
        return tuple([ob[i] for i in range(n)])
            
    def __len__(ob):
        return arrayclass_len(<PyObject*>ob)
                        
    def __richcmp__(self, other, flag):
        n_self = len(self)
        n_other = len(other)
        try:
            if flag == 2:
                if n_self != n_other:
                    return False
                for i in range(n_self):
                    if self[i] != other[i]:
                        return False
                return True
            elif flag == 3:
                if n_self != n_other:
                    return True
                for i in range(n_self):
                    if self[i] != other[i]:
                        return True
                return False
        except TypeError:
            pass

        switch = True
        if flag == 0:    # <
            if n_self >= n_other:
                return False
            little, big = self, other

        elif flag == 1:  # <=
            if n_self > n_other:
                return False
            little, big = self, other

        elif flag == 2:    # ==
            if n_self != n_other:
                return False
            little, big = self, other

        elif flag == 3:  # !=
            if n_self != n_other:
                return True
            little, big = self, other
            switch = False

        elif flag == 4:  # >
            if n_self <= n_other:
                return False
            little, big = other, self

        elif flag == 5:  # >=
            if n_self < n_other:
                return False
            little, big = other, self

        try:
            for k, v in enumerate(little):
                if v != big[k]:
                    return not switch
            return switch
        except IndexError:
            return not switch

    def __iter__(self):
        n = len(self)
        gen = (self[i] for i in range(n))
        return iter(gen)
        
    def __getstate__(self):
        'Exclude the OrderedDict from pickling'
        return None

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)
                
    def __reduce__(self):
        'Reduce'
        return type(self), tuple(self)
    
    def __copy__(self):
        tp = self.__class__
        args = tuple(self)
        return tp(*args)

cdef _type_configure(ob, n, readonly=False, usedict=False, gc=False, weaklist=False):
    cdef PyTypeObject *tp = <PyTypeObject*>ob;
    cdef Py_ssize_t size = PyNumber_AsSsize_t(<PyObject*>n, <PyObject*>PyExc_IndexError)
    
    tp.tp_basicsize = size * sizeof(PyObject*) + sizeof(PyObject)
    tp.tp_dictoffset = 0
    tp.tp_weaklistoffset = 0
    
    if tp.tp_bases:
        all_AC = all(c is ArrayClass for c in <object>tp.tp_bases)
    else:
        all_AC = False
    
    if usedict or not all_AC:
        tp.tp_dictoffset = tp.tp_basicsize
        tp.tp_basicsize += sizeof(PyObject*)
    if weaklist:
        tp.tp_weaklistoffset = tp.tp_basicsize
        tp.tp_basicsize += sizeof(PyObject*)

    tp.tp_itemsize = 0
    if gc:
        if not tp.tp_flags & Py_TPFLAGS_HAVE_GC:
            tp.tp_flags |= Py_TPFLAGS_HAVE_GC
    else:
        if tp.tp_flags & Py_TPFLAGS_HAVE_GC:
            tp.tp_flags ^= Py_TPFLAGS_HAVE_GC
    
    if tp.tp_as_sequence.sq_item != NULL:
       tp.tp_as_sequence.sq_item = arrayclass_item
       if readonly:
           tp.tp_as_sequence.sq_ass_item = NULL
       else:
           tp.tp_as_sequence.sq_ass_item = arrayclass_ass_item
    if tp.tp_as_mapping.mp_subscript != NULL:
       tp.tp_as_mapping.mp_subscript = arrayclass_subscript
       if readonly:
           tp.tp_as_mapping.mp_ass_subscript = NULL
       else:
           tp.tp_as_mapping.mp_ass_subscript = arrayclass_ass_subscript
    
    #tp.tp_new = arrayclass_new
    tp.tp_traverse = arrayclass_traverse
    tp.tp_clear = arrayclass_clear
    tp.tp_alloc = arrayclass_alloc
    #tp.tp_dealloc = arrayclass_dealloc
    tp.tp_free = arrayclass_free
    tp.tp_init = NULL

cdef dict slotsgetset_cache = {}

class structclasstype(type):
    #
    def __init__(cls, name, bases, ns):
        type.__init__(cls, name, bases, ns)
        readonly = ns.pop('readonly', False)
        usedict = ns.pop('usedict', False)
        gc = ns.pop('gc', False)
        weaklist = ns.pop('weaklist', False)
        if not hasattr(cls, '_fields'):
            raise TypeError('Missing _fields')
        _type_configure(cls, len(cls._fields), readonly, usedict, gc, weaklist)
        for index, name in enumerate(cls._fields):
            try:
                itemgetset_object = slotsgetset_cache[index]
            except KeyError:
                itemgetset_object = ArrayClassGetSet(index)
                slotsgetset_cache[index] = itemgetset_object
            setattr(cls, name, itemgetset_object)
        
class arrayclasstype(type):
    #
    def __init__(cls, name, bases, ns):
        type.__init__(cls, name, bases, ns)
        readonly = ns.pop('readonly', False)
        usedict = ns.pop('usedict', False)
        gc = ns.pop('gc', False)
        weaklist = ns.pop('weaklist', False)
        _type_configure(cls, len(cls._fields), readonly, usedict, gc, weaklist)
            
@cython.final
cdef class ArrayClassGetSet:
    
    cdef Py_ssize_t i
    
    def __init__(self, i):
        self.i = i
    
    def __get__(self, ob, tp):
        if ob is None:
            return self
        return <object>arrayclass_item(<PyObject*>ob, self.i)

    def __set__(self, ob, val):
        if ob is None:
            raise ValueError('None object')
        arrayclass_ass_item(<PyObject*>ob, self.i, <PyObject*>val)

cdef class SequenceProxy:
    cdef object ob
    cdef Py_hash_t hash
    
    @property
    def obj(self):
        return self.ob
    
    def __init__(self, ob):
        self.ob = ob
        self.hash = 0
        
    def __getitem__(self, ind):
        return self.ob.__getitem__(ind)
    
    def __len__(self):
        return self.ob.__len__()
    
    def __hash__(self):
        if self.hash == 0:
            self.hash = hash(tuple(self.ob))
        return self.hash

    def __richcmp__(self, other, flag):
        return self.ob.__richcmp__(other, flag)
    
    def __iter__(self):
        return iter(self.ob)
    
    def __repr__(self):
        return "sequenceproxy(" + repr(self.ob) + ")"
    
    
def sequenceproxy(ob):
    return SequenceProxy(ob)

