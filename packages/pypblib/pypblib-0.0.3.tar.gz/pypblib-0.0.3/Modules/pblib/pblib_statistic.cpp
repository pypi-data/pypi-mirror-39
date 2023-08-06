/*
 * PyPB PBLib::statistics bindings
 */

#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_statistic.hpp"


#ifdef __cplusplus
extern "C" {
#endif

// PyPBLibStatistic base object methods
//=============================================================================

static void PyPBLibStatistic_Dealloc(PyObject* self)
{
    self->ob_type->tp_free(self);
}


// PyPBLibStatistic methods
//=============================================================================

static PyObject* PyPBLibStatistic_Print(
    PyPBLibStatistic* self, PyObject* args)
{
    self->statistic.printStatistic();
    Py_RETURN_NONE;
}

static PyObject* PyPBLibStatistic_PrintRelative(
    PyPBLibStatistic* self, PyObject* args)
{
    self->statistic.printStatisticRelative();
    Py_RETURN_NONE;
}

// PyPBLibStatistic definition of methods, members, getters, setters, ...
//=============================================================================

static PyMethodDef PyPBLibStatistic_methods[] = {
    {"print", (PyCFunction)PyPBLibStatistic_Print,
     METH_NOARGS, "Prints into the stdout absolute statistic values"},
    {"print_relative",
     (PyCFunction)PyPBLibStatistic_PrintRelative, METH_NOARGS,
     "Prints into the stdout relative statistic values"},
    {NULL}  /* sentinel */
};


// PBLib statistic Python type definition
//=============================================================================

static const char* PyPBLibStatistic_doc =
"PBLib statistic structure";


PyTypeObject PyPBLibStatistic_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyPBLibStatistic_NAME,   /* tp_name */
    sizeof(PyPBLibStatistic),                      /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyPBLibStatistic_Dealloc,                      /* tp_dealloc */
    NULL,                                          /* tp_print */
    NULL,                                          /* tp_getattr */
    NULL,                                          /* tp_setattr */
    NULL,                                          /* tp_compare */
    NULL,                                          /* tp_repr */
    NULL,                                          /* tp_as_number */
    NULL,                                          /* tp_as_sequence */
    NULL,                                          /* tp_as_mapping */
    PyObject_HashNotImplemented,                   /* tp_hash */
    NULL,                                          /* tp_call */
    NULL,                                          /* tp_str */
    NULL,                                          /* tp_getattro */
    NULL,                                          /* tp_setattro */
    NULL,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                            /* tp_flags */
    PyPBLibStatistic_doc,                          /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyPBLibStatistic_methods,                      /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyType_GenericNew,                             /* tp_new */
};


#ifdef __cplusplus
}
#endif
