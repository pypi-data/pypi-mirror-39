/*
 *  PyPB PBLib::AuxVarManager bindings
 */

#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "aux_var_manager.hpp"

#ifdef __cplusplus
extern "C" {
#endif


//PyAuxVarManager base object methods
//=============================================

static void PyAuxVarManager_Dealoc(PyObject* self)
{
    self->ob_type->tp_free(self);
}

static PyObject * PyAuxVarManager_New(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    int var;
    if(!PyArg_ParseTuple(args, "i", &var)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be an integer.");
        return NULL;
    }

    PyAuxVarManager* self = (PyAuxVarManager*)type->tp_alloc(type,1);

    if(self != NULL) {
        new (&self->aux_var)AuxVarManager(var);
    }

    return (PyObject *) self;
}

// PyAuxVarManager methods
//========================================================

static PyObject* PyAuxVarManager_Get_Variable(PyAuxVarManager* self, void*)
{
    return Py_BuildValue("i", self->aux_var.getVariable());
}

static PyObject* PyAuxVarManager_Free_Variable(PyAuxVarManager* self, PyObject *args)
{
    int var;
    if(!PyArg_ParseTuple(args, "i", &var)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be an integer.");
        return NULL;
    }

    self->aux_var.freeVariable(var);
    Py_RETURN_NONE;
}

static PyObject* PyAuxVarManager_Free_Range_Variables(PyAuxVarManager* self, PyObject *args)
{
    int var_start;
    int var_end;
    if(!PyArg_ParseTuple(args, "ii", &var_start, &var_end)) {
        PyErr_SetString(PyExc_TypeError, "parameters must be integers.");
        return NULL;
    }

    self->aux_var.freeVariables(var_start, var_end);
    Py_RETURN_NONE;
}


static PyObject* PyAuxVarManager_Free_Variables(PyAuxVarManager* self, PyObject *args)
{
    PyObject* vars_list;
	if(!PyArg_ParseTuple(args, "O", &vars_list)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a vector of integers");
		return NULL;
	}

    std::vector<int> variables;
    if(Get_Int_Vector_From_C_To_Python(variables, vars_list)) {
        self->aux_var.freeVariables(variables);
    }
    Py_RETURN_NONE;
}


static PyObject* PyAuxVarManager_GetBiggestReturnedAuxVar(PyAuxVarManager* self, void*)
{
    return Py_BuildValue("i", self->aux_var.getBiggestReturnedAuxVar());
}


static PyObject* PyAuxVarManager_ResetAuxVarsTo(PyObject *self, PyObject *args)
{
    int var;
    if(!PyArg_ParseTuple(args, "i", &var)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be an integer.");
        return NULL;
    }

    ((PyAuxVarManager*)self)->aux_var.resetAuxVarsTo(var);
    Py_RETURN_NONE;
}


// PyAuxVarManager definition of methods, memebers, getters, setters,...
//========================================================

static PyMethodDef PyAuxVarManager_methods[] = {
    {"get_variable", (PyCFunction)PyAuxVarManager_Get_Variable,
	 METH_NOARGS, "returns an unused variable"},
    {"free_variable", (PyCFunction)PyAuxVarManager_Free_Variable,
	 METH_VARARGS, "frees an used variable to refill a gap later on"},
    {"free_range_variables", (PyCFunction)PyAuxVarManager_Free_Range_Variables,
	 METH_VARARGS, "frees a rage of variables"},
    {"free_variables", (PyCFunction)PyAuxVarManager_Free_Variables,
	 METH_VARARGS, "frees the specified variables"},
	{"get_biggest_returned_auxvar", (PyCFunction)PyAuxVarManager_GetBiggestReturnedAuxVar,
	 METH_NOARGS, "returns the biggest auxiliary variable"},
    {"reset_aux_var_to", (PyCFunction)PyAuxVarManager_ResetAuxVarsTo,
	 METH_VARARGS, "reset aux var to new number"},
    //TODO:
    //startRememberReturnedVariables()
    //stopRememberReturnedVariables()
	{NULL}	/* sentinel */
};


// PBLib AuxVarManager Python type definition
//========================================================

static const char* PyAuxVarManager_doc = "PBLib auxvarmanager structure";

PyTypeObject PyAuxVarManager_Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyAuxVarManager_NAME,	   /* tp_name */
    sizeof(PyAuxVarManager),                   	   /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyAuxVarManager_Dealoc,                   	   /* tp_dealloc */
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
    PyAuxVarManager_doc,                           /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyAuxVarManager_methods,                       /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyAuxVarManager_New,                           /* tp_new */
};


#ifdef __cplusplus
}
#endif

