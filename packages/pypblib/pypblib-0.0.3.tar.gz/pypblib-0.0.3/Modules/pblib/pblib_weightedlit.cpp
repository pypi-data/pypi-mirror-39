/*
 * PyPB PBLib::weightedlit bindings
 */

#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_weightedlit.hpp"


//PyPBLibWeightedlit Utility methods
//=====================================================================

inline PyObject* PyWeightedLit_From_Raw_Data(PyTypeObject* type,
                                             int literal, long weight)
{
  PyPBLibWeightedLit* self = (PyPBLibWeightedLit*)type->tp_alloc(type, 1);
	if(self != NULL){
		// Constructs Weightedlit on already allocated memory
		new (&self->wl) PBLib::WeightedLit(literal, weight);
	}

	return (PyObject *) self;
}


PyObject* PyWeightedLit_From_WeightedLit(const PBLib::WeightedLit &wl)
{
  return PyWeightedLit_From_Raw_Data(&PyPBLibWeightedLit_Type, wl.lit,
                                     wl.weight);
}


#ifdef __cplusplus
extern "C" {
#endif

//PyPBLibWeightedlit base Object methods
//=====================================================================

static void PyPBLibWeightedLit_Dealloc(PyObject* self)
{
	self->ob_type->tp_free(self);
}


static PyObject * PyWeightedLit_New(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	int literal;
	long weight;
	if(!PyArg_ParseTuple(args, "il", &literal, &weight)){
		//...handle error here
		PyErr_SetString(PyExc_TypeError, "parameter must be an int and a long.");
		return NULL;
	}

  return PyWeightedLit_From_Raw_Data(type, literal, weight);
}


static PyObject* PyWeightedLit_Repr(PyPBLibWeightedLit* wl) {
    std::stringstream ss;
    ss << "WeightedLit(lit=" << wl->wl.lit << ", weight="
       << wl->wl.weight << ")";
    return PyUnicode_FromString(ss.str().c_str());
}


static PyObject* PyWeightedLit_Str(PyPBLibWeightedLit* wl) {
    std::stringstream ss;
    ss << "(" << wl->wl.lit << ", " << wl->wl.weight << ")";
    return PyUnicode_FromString(ss.str().c_str());
}


// PyPBLibWeightedlit methods
//=============================================================================

static PyObject* PyWeightedLit_Comp_Variable_Asc(PyPBLibWeightedLit* self, PyObject* args)
{
	PyObject *lhs, *rhs;

	if(!PyArg_ParseTuple(args, "OO", &lhs, &rhs)){
		PyErr_SetString(PyExc_TypeError, "parameters must be a WeightedLit.");
		return NULL;
	}

    if(!PyPBWeightedLit_Check(lhs) || !PyPBWeightedLit_Check(rhs)) {
        PyErr_SetString(PyExc_TypeError, "parameters must be a WeightedLit.");
        return NULL;
    }

    if(self->wl.compVariable_asc(((PyPBLibWeightedLit*)lhs)->wl,
                                 ((PyPBLibWeightedLit*)rhs)->wl)) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


static PyObject* PyWeightedLit_Comp_Variable_Des(PyPBLibWeightedLit* self, PyObject* args)
{
	PyObject *lhs, *rhs;

	if(!PyArg_ParseTuple(args, "OO", &lhs, &rhs)){
		PyErr_SetString(PyExc_TypeError, "parameters must be a WeightedLit.");
		return NULL;
	}

    if(!PyPBWeightedLit_Check(lhs) || !PyPBWeightedLit_Check(rhs)) {
        PyErr_SetString(PyExc_TypeError, "parameters must be a WeightedLit.");
        return NULL;
    }

    if(self->wl.compVariable_des(((PyPBLibWeightedLit*)lhs)->wl,
                                 ((PyPBLibWeightedLit*)rhs)->wl)) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


static PyObject* PyWeightedLit_Comp_Variable_Des_Var(PyPBLibWeightedLit* self, PyObject* args)
{
	PyObject *lhs, *rhs;

	if(!PyArg_ParseTuple(args, "OO", &lhs, &rhs)){
		PyErr_SetString(PyExc_TypeError, "parameters must be a WeightedLit.");
		return NULL;
	}

    if(!PyPBWeightedLit_Check(lhs) || !PyPBWeightedLit_Check(rhs)) {
        PyErr_SetString(PyExc_TypeError, "parameters must be a WeightedLit.");
        return NULL;
    }

    if(self->wl.compVariable_des_var(((PyPBLibWeightedLit*)lhs)->wl,
                                     ((PyPBLibWeightedLit*)rhs)->wl)) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}


// PyPBLibWeightedlit definition of methods, members, getters, setters, ...
//=============================================================================

static PyMethodDef PyPBlibWeightedLit_methods[] = {
	{"comp_variable_asc", (PyCFunction)PyWeightedLit_Comp_Variable_Asc,
	METH_VARARGS, "return true if the weight of first WeightedLit is bigger than the weight of the second. Return false otherwise" },
    {"comp_variable_des", (PyCFunction)PyWeightedLit_Comp_Variable_Des,
	METH_VARARGS, "return true if the weight of first WeightedLit is smaller than the weight of the second. Return false otherwise" },
    {"comp_variable_des_var", (PyCFunction)PyWeightedLit_Comp_Variable_Des_Var,
	METH_VARARGS, "return true if absolute value literal's of the WeightedLit is smaller than absolute value of the literal's of specified WeightedLit. Return false otherwise" },
	{NULL}  /*sentinel */
};


// PBLib weightedlit Python type definition
//=============================================================================

static const char* PyPBWeightedLit_doc = "PBLib weightedlit structure";



PyTypeObject PyPBLibWeightedLit_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyPBLibWeightedLit_NAME,   /* tp_name */
    sizeof(PyPBLibWeightedLit),                      /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyPBLibWeightedLit_Dealloc,                    /* tp_dealloc */
    NULL,                                          /* tp_print */
    NULL,                                          /* tp_getattr */
    NULL,                                          /* tp_setattr */
    NULL,                                          /* tp_compare */
    (reprfunc)PyWeightedLit_Repr,                  /* tp_repr */
    NULL,                                          /* tp_as_number */
    NULL,                                          /* tp_as_sequence */
    NULL,                                          /* tp_as_mapping */
    PyObject_HashNotImplemented,                   /* tp_hash */
    NULL,                                          /* tp_call */
    (reprfunc)PyWeightedLit_Str,                   /* tp_str */
    NULL,                                          /* tp_getattro */
    NULL,                                          /* tp_setattro */
    NULL,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                            /* tp_flags */
    PyPBWeightedLit_doc,                           /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyPBlibWeightedLit_methods,                    /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyWeightedLit_New,                             /* tp_new */
};

#ifdef __cplusplus
}
#endif

