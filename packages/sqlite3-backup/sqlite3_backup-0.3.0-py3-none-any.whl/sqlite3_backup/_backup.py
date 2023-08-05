#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import ctypes
import os
import sqlite3
import sys

import _sqlite3

SQLITE_OK = 0
SQLITE_DONE = 101


if hasattr(ctypes.pythonapi, "Py_InitModule4_64"):
    _Py_ssize_t = ctypes.c_int64
else:
    _Py_ssize_t = ctypes.c_int


class Sqlite3ModuleInternals:

    """Allows access to raw c pointer wrapped within Pyhon sqlite3
    module via ctypes.
    """

    class _Connection(ctypes.Structure):

        _fields_ = [
            ("ob_refcnt", _Py_ssize_t),
            ("ob_type", ctypes.c_void_p),
            ("db", ctypes.c_void_p),
        ]

    @classmethod
    def db_handle_c_pointer(clz, connection):
        assert isinstance(connection, sqlite3.Connection)
        return clz._Connection.from_address(id(connection)).db


def load_sqlite3_shared_library():

    """loads sqlite3 shared library (the one from sqlite3 iteself,
    not the compile python extension module).
    """

    if sys.platform == "darwin":
        sqlite3_lib_name = "libsqlite3.dylib"
    elif sys.platform.startswith("linux"):
        sqlite3_lib_name = "libsqlite3.so.0"
    elif sys.platform == "win32":
        base_folder = os.path.dirname(os.path.abspath(_sqlite3.__file__))
        sqlite3_lib_name = os.path.join(base_folder, "sqlite3.dll")
    else:
        raise RuntimeError("platform {} not supported".format(sys.platform))
    return ctypes.CDLL(sqlite3_lib_name)


def check_err_code(function, *allowed_codes):
    """function decorator to raise exceptions if lower level c functions
    return error codes indicating failure.
    """

    def wrapped(*a, **kw):
        rc = function(*a, **kw)
        if rc not in allowed_codes:
            msg = "got invalid error code {} from {}".format(rc, function.__name__)
            raise sqlite3.InternalError(msg)

    return wrapped


def setup_c_functions():
    """loads sqlite3 shared library and configures ctypes accessors,
    including error handing for some error return codes.
    """
    _sqlite3 = load_sqlite3_shared_library()

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

    # const char *sqlite3_db_filename(sqlite3 *db, const char *zDbName)
    _sqlite3.sqlite3_db_filename.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    _sqlite3.sqlite3_db_filename.restype = ctypes.c_char_p

    db_file_name = _sqlite3.sqlite3_db_filename
    backup_init = _sqlite3.sqlite3_backup_init
    backup_step = check_err_code(_sqlite3.sqlite3_backup_step, SQLITE_OK, SQLITE_DONE)
    backup_remaining = _sqlite3.sqlite3_backup_remaining
    backup_finish = check_err_code(_sqlite3.sqlite3_backup_finish, SQLITE_OK)

    return db_file_name, backup_init, backup_step, backup_remaining, backup_finish


db_file_name, backup_init, backup_step, backup_remaining, backup_finish = (
    setup_c_functions()
)


def get_db_file_name(connection):
    connection_c_pointer = Sqlite3ModuleInternals.db_handle_c_pointer(connection)
    return db_file_name(connection_c_pointer, b"main")


def is_inmemory_or_temp_db(connection):
    return get_db_file_name(connection) == b""


def get_sqlite3_backup_handle(
    source_connection, source_db_name, target_connection, target_db_name
):
    """extracts raw c pointers from sqlite3 connection Python object and
    initialises  s qlite3 backup handle.
    """
    source_c_pointer = Sqlite3ModuleInternals.db_handle_c_pointer(source_connection)
    target_c_pointer = Sqlite3ModuleInternals.db_handle_c_pointer(target_connection)

    handle = backup_init(
        target_c_pointer,
        bytes(target_db_name, "ascii"),
        source_c_pointer,
        bytes(source_db_name, "ascii"),
    )
    return handle


def backup(
    source_connection, source_db_name, target_connection, target_db_name, pages=100
):
    """actual main method to copy database for given connection
    objects.
    """
    assert isinstance(source_connection, sqlite3.Connection)
    assert isinstance(target_connection, sqlite3.Connection)

    if is_inmemory_or_temp_db(source_connection):
        pages = -1  # copy all in one

    handle = get_sqlite3_backup_handle(
        source_connection, source_db_name, target_connection, target_db_name
    )
    backup_step(handle, pages)
    while True:
        remaining = backup_remaining(handle)
        if not remaining:
            break
        backup_step(handle, pages)
    backup_finish(handle)
