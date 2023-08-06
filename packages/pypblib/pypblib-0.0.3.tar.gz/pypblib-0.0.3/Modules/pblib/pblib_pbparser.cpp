/*
 * PyPB PBParser bindings
 */

#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_pbparser.hpp"

#ifdef __cplusplus
extern "C" {
#endif

// PyPBLibPBParser base object methods
//====================================================================

static void PyPBLibPBParser_Dealloc(PyObject* self)
{
	self->ob_type->tp_free(self);
}


//PyPBLibParser methods
//====================================================================

static PyObject* PyPBLibParser_getMaxVarID(PyPBLibPBParser* self, void* /*closure*/)
{
	return Py_BuildValue("i", self-> parser.getMaxVarID());
}

static PyObject* PyPBLibPBParser_IsOk(PyPBLibPBParser* self, PyObject* args)
{
	self->parser.isOk();
	Py_RETURN_NONE;
}

static PyObject* PyPBLibPBParser_HasObjectiveFunction(PyPBLibPBParser* self, PyObject* args)
{
	self->parser.hasObjectiveFunction();
	Py_RETURN_NONE;
}

static PyMethodDef PyPBLibPBParser_methods[] = {
	{"getMaxVarID", (PyCFunction)PyPBLibParser_getMaxVarID,
	 METH_NOARGS, "DESCRIPTION"},
	{"isOk", (PyCFunction)PyPBLibPBParser_IsOk,
	 METH_NOARGS, "DESCRIPTION"},
	{"hasObjectiveFunction",
	 (PyCFunction)PyPBLibPBParser_HasObjectiveFunction, METH_NOARGS,
	 "DESCRIPTION"},
	{NULL}	/* sentinel */
};

// PBLib parser Python type definition
//=====================================================================

static const char* PyPBLibPBParser_doc = "PBLib PBParser structure";


PyTypeObject PyPBLibPBParser_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyPBLibPBParser_NAME,    /* tp_name */
    sizeof(PyPBLibPBParser),                       /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyPBLibPBParser_Dealloc,                       /* tp_dealloc */
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
    PyPBLibPBParser_doc,                           /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyPBLibPBParser_methods,                       /* tp_methods */
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

