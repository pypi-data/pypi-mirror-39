#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import ctypes
import os
import sqlite3
import sys

import _sqlite3

if hasattr(ctypes.pythonapi, "Py_InitModule4_64"):
    Py_ssize_t = ctypes.c_int64
else:
    _Py_ssize_t = ctypes.c_int


class _PyObject(ctypes.Structure):
    pass


_PyObject._fields_ = [
    ("ob_refcnt", _Py_ssize_t),
    ("ob_type", ctypes.POINTER(_PyObject)),
]


class _Connection(_PyObject):
    pass


_Connection._fields_ = [("db", ctypes.c_void_p)]


if sys.platform == "darwin":
    sqlite3_lib_name = "libsqlite3.dylib"
elif sys.platform.startswith("linux"):
    sqlite3_lib_name = "libsqlite3.so.0"
elif sys.platform == "win32":
    base_folder = os.path.dirname(os.path.abspath(_sqlite3.__file__))
    sqlite3_lib_name = os.path.join(base_folder, "sqlite3.dll")
else:
    raise RuntimeError("platform {} not supported".format(sys.platform))

_sqlite3 = ctypes.CDLL(sqlite3_lib_name)

_sqlite3.sqlite3_backup_init.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_void_p,
    ctypes.c_char_p,
]
_sqlite3.sqlite3_backup_init.restype = ctypes.c_void_p


# int sqlite3_backup_step(sqlite3_backup *p, int nPage);
_sqlite3.sqlite3_backup_step.argtypes = [ctypes.c_void_p, ctypes.c_int]
_sqlite3.sqlite3_backup_step.restype = ctypes.c_int

# int sqlite3_backup_finish(sqlite3_backup *p);
_sqlite3.sqlite3_backup_finish.argtypes = [ctypes.c_void_p]
_sqlite3.sqlite3_backup_finish.restype = ctypes.c_int

# int sqlite3_backup_remaining(sqlite3_backup *p);
_sqlite3.sqlite3_backup_remaining.argtypes = [ctypes.c_void_p]
_sqlite3.sqlite3_backup_remaining.restype = ctypes.c_int


# int sqlite3_backup_pagecount(sqlite3_backup *p);
_sqlite3.sqlite3_backup_pagecount.argtypes = [ctypes.c_void_p]
_sqlite3.sqlite3_backup_pagecount.restype = ctypes.c_int


def backup(source_connection, target_connection, pages=100):
    source = _Connection.from_address(id(source_connection))
    target = _Connection.from_address(id(target_connection))

    handle = _sqlite3.sqlite3_backup_init(target.db, b"main", source.db, b"main")

    rc = _sqlite3.sqlite3_backup_step(handle, pages)
    assert rc in (0, 101), "got rc {} in sqlite3_backup_step".format(rc)
    while True:
        remaining = _sqlite3.sqlite3_backup_remaining(handle)
        if not remaining:
            break
        rc = _sqlite3.sqlite3_backup_step(handle, pages)
        assert rc in (0, 101), "got rc {} in sqlite3_backup_step".format(rc)
    rc = _sqlite3.sqlite3_backup_finish(handle)
    assert rc == 0, "got rc {} in sqlite3_backup_finish".format(rc)
