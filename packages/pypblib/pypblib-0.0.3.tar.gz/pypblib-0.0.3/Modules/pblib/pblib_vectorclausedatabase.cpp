/*
 * PyPB VectorClauseDatabase
 */
#include <fstream>
#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_vectorclausedatabase.hpp"
#include "pblib_pbconfig.hpp"

#ifdef __cplusplus
extern "C" {
#endif


//PyVectorClauseDatabase base objects methods
//=================================================================

static void PyVectorClauseDatabase_Dealloc(PyObject* self)
{
    self->ob_type->tp_free(self);
}


static PyObject * VectorClauseDatabase_One_Param(PyTypeObject *type, PyObject *args)
{
    PyObject *conf;
    if(!PyArg_ParseTuple(args, "O", &conf) || !PyPBConfig_Check(conf)){
        PyErr_SetString(PyExc_TypeError, "parameter must be a PBConfig");
        return NULL;
    }

    PyVectorClauseDatabase* self = (PyVectorClauseDatabase*)type->tp_alloc(type,1);
    if(self != NULL) {

        new (&self->vector_cdb) VectorClauseDatabase(((PyPBConfig*)conf)->config);
    }

    return(PyObject *) self;
}

static PyObject * VectorClauseDatabase_Two_Param(PyTypeObject *type, PyObject *args)
{
    PyObject *conf;
    PyObject *seq;
    if(!PyArg_ParseTuple(args, "OO", &conf, &seq) || !PyPBConfig_Check(conf)){
        PyErr_SetString(PyExc_TypeError, "parameter must be a PBConfig");
        return NULL;
    }

    PyObject *iter, *item;
    if ((iter = PyObject_GetIter(seq)) == NULL) {
        PyErr_SetString(PyExc_TypeError, "Second parameter must be iterable");
        return NULL;
    }

    std::vector<int> vect;
    std::vector<std::vector<int>>* clauses = new std::vector<std::vector<int>>;
    while (item = PyIter_Next(iter)) {

        vect.clear();
        if(Get_Int_Vector_From_C_To_Python(vect, item)) {
            PyErr_SetString(PyExc_TypeError, "Second parameter must be a list of integer's list");
            Py_DECREF(item);
            Py_DECREF(iter);
            return NULL;
        }
        clauses->push_back(vect);
        Py_DECREF(item);
    }

    Py_DECREF(iter);

    PyVectorClauseDatabase* self = (PyVectorClauseDatabase*)type->tp_alloc(type,1);
    if(self != NULL) {

        new (&self->vector_cdb) VectorClauseDatabase(((PyPBConfig*)conf)->config, clauses);
    }

    return(PyObject *) self;
}


static PyObject * PyVectorClauseDatabase_New(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    switch(PyTuple_Size(args))
    {
        case 0:
            PyErr_SetString(PyExc_TypeError, "paramaters are needed. ClauseDataBase takes PBConfig, or PBConfig and clauses (integer's list).");
            return NULL;
        case 1:
            return VectorClauseDatabase_One_Param(type, args);
        case 2:
            return VectorClauseDatabase_Two_Param(type, args);
        default:
            PyErr_SetString(PyExc_TypeError, "there are too many parameter. ClauseDataBase only takes one or two parameters.");
            return NULL;
    }
}


static PyObject* PyVectorClauseDatabase_Repr(PyVectorClauseDatabase* self) {
    std::stringstream ss;
    std::vector<std::vector<int32_t>> formula = ((PyVectorClauseDatabase*)self)->
                                                  vector_cdb.getClauses();
    ss << "Num. Causes: " << formula.size() << std::endl;
    ss << "==============================" << std::endl;
    for (auto clause : formula) {
	   for(unsigned int i=0; i < clause.size(); i++) {

            ss << clause[i] << " ";
		}
        ss << "0" <<std::endl;
	}
    ss << "==============================" << std::endl;
    return PyUnicode_FromString(ss.str().c_str());
}


static PyObject* PyVectorClauseDatabase_Str(PyVectorClauseDatabase* self) {
    std::stringstream ss;
    std::vector<std::vector<int32_t>> formula = ((PyVectorClauseDatabase*)self)->
                                                  vector_cdb.getClauses();
    for (auto clause : formula) {
	   for(unsigned int i=0; i < clause.size(); i++) {

            ss << clause[i] << " ";
		}
        ss << "0" <<std::endl;
	}
    return PyUnicode_FromString(ss.str().c_str());
}


// VectorClauseDatabase methods
//=============================================================================

static PyObject* PyVectorClauseDatabase_Get_Clauses(PyVectorClauseDatabase* self, void*)
{
    std::vector<std::vector<int>> vect_clauses = self->vector_cdb.getClauses();
    PyObject* list_clauses = PyList_New(0);
    PyObject* item;

    for (unsigned int i = 0; i < vect_clauses.size(); i++) {
        std::vector<int> cl = vect_clauses[i];
        PyObject* list = PyList_New(0);

        for(unsigned int j = 0; j < cl.size(); j++) {
		    item = Py_BuildValue("i", cl[j]);
		    PyList_Append(list, item);
        }

        PyList_Append(list_clauses, list);
	}

    return list_clauses;
}


static PyObject* PyVectorClauseDatabase_PrintFormula(
    PyVectorClauseDatabase* self, PyObject* args)
{
    if(PyTuple_Size(args) == 0) {
        ((PyVectorClauseDatabase*)self)->vector_cdb.printFormula();
        Py_RETURN_NONE;
    }

    PyObject* py_str;
    int cnt;
    if(!PyArg_ParseTuple(args, "O!i", &PyUnicode_Type, &py_str, &cnt)){
        PyErr_SetString(PyExc_TypeError, "parameter must an string & int");
        return NULL;
    }

#if PY_MAJOR_VERSION >= 3
    const char* file_name = PyUnicode_AsUTF8(py_str);
#else
    PyObject* temp_obj = PyUnicode_AsASCIIString(py_str);
    const char* file_name = PyByteArray_AsString(temp_obj);
    Py_XDECREF(temp_obj);
#endif

    std::ofstream fs;
    fs.open(file_name);
    std::vector<std::vector<int32_t>> formula = ((PyVectorClauseDatabase*)self)
                                                ->vector_cdb.getClauses();

    fs << "p cnf " <<  cnt << " " << formula.size() << std::endl;
    for (auto clause : formula) {
	   for(unsigned int i=0; i < clause.size(); i++) {

            fs << clause[i] << " ";
		}
        fs << "0" <<std::endl;
	}

    fs.close();

    Py_RETURN_NONE;
}


static PyObject* PyVectorClauseDatabase_Get_Num_Clauses(PyVectorClauseDatabase* self, void*)
{
    return Py_BuildValue("i", ((PyVectorClauseDatabase*)self)->vector_cdb.getClauses().size());
}

static PyObject* PyVectorClauseDatabase_Clear_Database(PyVectorClauseDatabase* self, void*)
{
    self->vector_cdb.clearDatabase();
    Py_RETURN_NONE;
}

static PyObject* PyVectorClauseDatabase_Reset_Internal_Unsat_State(PyVectorClauseDatabase* self, void*)
{
    self->vector_cdb.resetInternalUnsatState();
    Py_RETURN_NONE;
}


// PyPBLibStatistic definition of methods, members, getters, setters, ...
//=============================================================================

static PyMethodDef PyVectorClauseDatabase_methods[] = {
    {"get_clauses", (PyCFunction)PyVectorClauseDatabase_Get_Clauses,
     METH_NOARGS, "Returns a list of integer's lists that represents the clauses in VectorClauseDatabase"},
    {"print_formula", (PyCFunction)PyVectorClauseDatabase_PrintFormula,
     METH_VARARGS, "Prints formula in to a file with specified name"},
    {"get_num_clauses", (PyCFunction)PyVectorClauseDatabase_Get_Num_Clauses,
     METH_NOARGS, "Returns the number of clauses in VectorClauseDatabase"},
    {"clear_database", (PyCFunction)PyVectorClauseDatabase_Clear_Database,
     METH_NOARGS, "Resets the clause database"},
    {"reset_internal_unsat_state", (PyCFunction)PyVectorClauseDatabase_Reset_Internal_Unsat_State,
     METH_NOARGS, "Sets the internal unsat state to false"},
    {NULL}  /* sentinel */
};

// PBLib VectorClauseDatabase Python type definition
//=======================================================================

static const char* PyVectorClauseDatabase_doc = "PBLib vectorclausedatabase structure";


PyTypeObject PyVectorClauseDatabase_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyVectorClauseDatabase_NAME,   /* tp_name */
    sizeof(PyVectorClauseDatabase),                      /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyVectorClauseDatabase_Dealloc,                /* tp_dealloc */
    NULL,                                          /* tp_print */
    NULL,                                          /* tp_getattr */
    NULL,                                          /* tp_setattr */
    NULL,                                          /* tp_compare */
    (reprfunc)PyVectorClauseDatabase_Repr,         /* tp_repr */
    NULL,                                          /* tp_as_number */
    NULL,                                          /* tp_as_sequence */
    NULL,                                          /* tp_as_mapping */
    PyObject_HashNotImplemented,                   /* tp_hash */
    NULL,                                          /* tp_call */
    (reprfunc)PyVectorClauseDatabase_Str,          /* tp_str */
    NULL,                                          /* tp_getattro */
    NULL,                                          /* tp_setattro */
    NULL,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                            /* tp_flags */
    PyVectorClauseDatabase_doc,                    /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyVectorClauseDatabase_methods,                /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyVectorClauseDatabase_New,                    /* tp_new */
};

#ifdef __cplusplus
}
#endif


