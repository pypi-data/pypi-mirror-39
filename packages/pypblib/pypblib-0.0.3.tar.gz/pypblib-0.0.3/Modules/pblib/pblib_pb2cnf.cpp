/*
 *  PYPB pb2cnf bindings
 */
#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_pb2cnf.hpp"
#include "pblib_statistic.hpp"
#include "pblib_pbconfig.hpp"
#include "pblib_pbconstraint.hpp"
#include "pblib_incpbconstraint.hpp"
#include "pblib_vectorclausedatabase.hpp"
#include "aux_var_manager.hpp"

#ifdef __cplusplus
extern "C" {
#endif


//PyPb2cnf base object methods
//=======================================================================

static void PyPb2cnf_Dealloc(PyObject* self)
{
    self->ob_type->tp_free(self);
}


static PyObject * PyPb2cnf_Whith_Zero_Parameters(PyTypeObject *type)
{
    PyPb2cnf* self = (PyPb2cnf*)type->tp_alloc(type,1);
    new (&self->pb2cnf) PB2CNF();
    return (PyObject *) self;
}


static PyObject * PyPb2cnf_Whith_One_Parameters(PyTypeObject *type, PyObject *args)
{
    PyObject *conf;
    if(!PyArg_ParseTuple(args, "O", &conf)) { goto error; }
    if(!PyPBConfig_Check(conf)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a PBConfig");
    return NULL;

finally:
    PyPb2cnf* self = (PyPb2cnf*)type->tp_alloc(type,1);
    if(self != NULL) {
        new (&self->pb2cnf) PB2CNF(((PyPBConfig*)conf)->config);
    }
    return(PyObject *) self;
}


static PyObject * PyPb2cnf_Whith_Two_Parameters(PyTypeObject *type, PyObject *args)
{
    PyObject *conf;
    PyObject *stats;
    if(!PyArg_ParseTuple(args, "OO", &conf, &stats)) { goto error; }
    if(!PyPBConfig_Check(conf) || !PyPBLibStatistic_Check(stats)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a PBConfig and Statistic");
    return NULL;

finally:
    PyPb2cnf* self = (PyPb2cnf*)type->tp_alloc(type,1);
    if(self != NULL) {
        PyPBLibStatistic st = *((PyPBLibStatistic*)stats);
        new (&self->pb2cnf) PB2CNF(((PyPBConfig*)conf)->config,
                                   (&st.statistic));
    }
    return(PyObject *) self;
}



static PyObject* PyPb2cnf_New(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    switch(PyTuple_Size(args))
    {
        case 0:
            return PyPb2cnf_Whith_Zero_Parameters(type);
        case 1:
            return PyPb2cnf_Whith_One_Parameters(type, args);
        case 2:
            return PyPb2cnf_Whith_Two_Parameters(type, args);
        default:
            PyErr_SetString(PyExc_TypeError,
                "too many parameters. Pb2cnf takes none, one (PBConfig) or two (PBConfig and Statistic) parameters.");
            return NULL;
    }
}


// PyPb2cnf methods
//=======================================================================

static PyObject* PyPb2cnf_Encode(PyPb2cnf* self, PyObject* args)
{
    PyObject* pbconst;
    PyObject* vect_cdb;
    PyObject* aux_v;

    if(!PyArg_ParseTuple(args, "OOO", &pbconst, &vect_cdb, &aux_v)) {
        goto error;
    }

    if(!PyPBConstraint_Check(pbconst) ||
       !PyVectorClauseDatabase_Check(vect_cdb) ||
       !PyAuxVarManager_Check(aux_v))
       { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError,
        "parameters must be PBConstraint, VectorClauseDatabase & AuxVarManager");
    return NULL;

finally:
    self->pb2cnf.encode((((PyPBConstraint*)pbconst)->constraint),
                        (((PyVectorClauseDatabase*)vect_cdb)->vector_cdb),
                        (((PyAuxVarManager*)aux_v)->aux_var));
    Py_RETURN_NONE;
}


static PyObject* PyPb2cnf_Encode_IncInitial(PyPb2cnf* self, PyObject* args)
{
    PyObject* pb_inc_const;
    PyObject* vect_cdb;
    PyObject* aux_v;

    if(!PyArg_ParseTuple(args, "OOO", &pb_inc_const, &vect_cdb, &aux_v)) {
        goto error;
    }

    if(!PyIncPBConstraint_Check(pb_inc_const) ||
       !PyVectorClauseDatabase_Check(vect_cdb) ||
       !PyAuxVarManager_Check(aux_v))
       { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError,
        "parameters must be IncPBConstraint, VectorClauseDatabase & AuxVarManager");
    return NULL;

finally:
    self->pb2cnf.encodeIncInital((((PyIncPBConstraint*)pb_inc_const)->incconstraint),
                        (((PyVectorClauseDatabase*)vect_cdb)->vector_cdb),
                        (((PyAuxVarManager*)aux_v)->aux_var));
    Py_RETURN_NONE;
}


static PyObject* PyPb2cnf_Encode_At_Most_K(PyPb2cnf* self, PyObject* args)
{
    PyObject* lits;
    long k;
    PyObject* py_formula;
    int first_aux_var;

    if(!PyArg_ParseTuple(args, "O!lO!i", &PyList_Type, &lits, &k,
                         &PyList_Type, &py_formula, &first_aux_var)) {
        PyErr_SetString(PyExc_TypeError, "Parameter mus be int_list, long, list and int");
        return NULL;
    }

    std::vector<int> literals;
    if(!Get_Int_Vector_From_C_To_Python(literals, lits)){ return NULL; }
    std::vector<std::vector<int>> formula;
    int max_var = self->pb2cnf.encodeAtMostK(literals, k, formula, first_aux_var);
    Build_PyList_Formula(py_formula, formula);
    return Py_BuildValue("i", max_var);
}


static PyObject* PyPb2cnf_Encode_At_Least_K(PyPb2cnf* self, PyObject* args)
{
    PyObject* lits;
    long k;
    PyObject* py_formula;
    int first_aux_var;

    if(!PyArg_ParseTuple(args, "O!lO!i", &PyList_Type, &lits, &k,
                         &PyList_Type, &py_formula, &first_aux_var)) {
        PyErr_SetString(PyExc_TypeError, "Parameter mus be int_list, long, list and int");
        return NULL;
    }

    std::vector<int> literals;
    if(!Get_Int_Vector_From_C_To_Python(literals, lits)){ return NULL; }
    std::vector<std::vector<int>> formula;
    int max_var = self->pb2cnf.encodeAtLeastK(literals, k, formula, first_aux_var);
    Build_PyList_Formula(py_formula, formula);
    return Py_BuildValue("i", max_var);
}


static PyObject* PyPb2cnf_Encode_Leq(PyPb2cnf* self, PyObject* args)
{
    PyObject* wei;
    PyObject* lits;
	long leq;
    PyObject* py_formula;
    int first_aux_var;

    if(!PyArg_ParseTuple(args, "OOlOi", &wei, &lits, &leq, &py_formula, &first_aux_var)) {
        PyErr_SetString(PyExc_TypeError, "Parameter mus be long_list, int_list, long, list and int");
        return NULL;
    }

    std::vector<int> literals;
    if(!Get_Int_Vector_From_C_To_Python(literals, lits)){ return NULL; }
    std::vector<int64_t> weights;
    if(!Get_Int64_Vector_From_C_To_Python(weights, wei)){ return NULL; }

    std::vector<std::vector<int>> formula;
    int max_var = self->pb2cnf.encodeLeq(weights, literals, leq, formula, first_aux_var);
    Build_PyList_Formula(py_formula, formula);
    return Py_BuildValue("i", max_var);
}

static PyObject* PyPb2cnf_Encode_Geq(PyPb2cnf* self, PyObject* args)
{
    PyObject* wei;
    PyObject* lits;
	long geq;
    PyObject* py_formula;
    int first_aux_var;

    if(!PyArg_ParseTuple(args, "OOlOi", &wei, &lits, &geq, &py_formula, &first_aux_var)) {
        PyErr_SetString(PyExc_TypeError, "Parameter mus be vector<int>, long, vector<vector<int>> and int");
        return NULL;
    }

    std::vector<int> literals;
    if(!Get_Int_Vector_From_C_To_Python(literals, lits)){ return NULL; }
    std::vector<int64_t> weights;
    if(!Get_Int64_Vector_From_C_To_Python(weights, wei)){ return NULL; }

    std::vector<std::vector<int>> formula;
    int max_var = self->pb2cnf.encodeGeq(weights, literals, geq, formula, first_aux_var);
    Build_PyList_Formula(py_formula, formula);
    return Py_BuildValue("i", max_var);
}


static PyObject* PyPb2cnf_Encode_Both(PyPb2cnf* self, PyObject* args)
{
    PyObject* wei;
    PyObject* lits;
    long leq;
	long geq;
    PyObject* py_formula;
    int first_aux_var;

    if(!PyArg_ParseTuple(args, "OOllOi", &wei, &lits, &leq, &geq, &py_formula, &first_aux_var)) {
        PyErr_SetString(PyExc_TypeError, "Parameter mus be vector<int>, long, vector<vector<int>> and int");
        return NULL;
    }

    std::vector<int> literals;
    if(!Get_Int_Vector_From_C_To_Python(literals, lits)){ return NULL; }
    std::vector<int64_t> weights;
    if(!Get_Int64_Vector_From_C_To_Python(weights, wei)){ return NULL; }

    std::vector<std::vector<int>> formula;
    int max_var = self->pb2cnf.encodeBoth(weights, literals, leq, geq, formula, first_aux_var);
    Build_PyList_Formula(py_formula, formula);
    return Py_BuildValue("i", max_var);
}


void Build_PyList_Formula(PyObject *py_formula, std::vector<std::vector<int>> &formula) {

    for(auto line = formula.begin(); line != formula.end(); line++) {
        PyObject* py_clause = PyList_New(0);

        for(auto item = line->begin(); item != line->end(); item++) {
            PyList_Append(py_clause, PyLong_FromLong(*item));
        }
        PyList_Append(py_formula, py_clause);
    }
}


// PyPb2cnf definition of methods, members, getters, setters,...
//=======================================================================

static PyMethodDef PyPb2cnf_methods[] = {
	{"encode", (PyCFunction)PyPb2cnf_Encode,
	 METH_VARARGS, "Encode new formula"},
    {"encode_inc_initial", (PyCFunction)PyPb2cnf_Encode_IncInitial,
	 METH_VARARGS, "Encode new incremental formula"},
    {"encode_at_most_k", (PyCFunction)PyPb2cnf_Encode_At_Most_K,
	 METH_VARARGS, "Encode new formula with at most configuration and a k as bound"},
    {"encode_at_least_k", (PyCFunction)PyPb2cnf_Encode_At_Least_K,
	 METH_VARARGS, "Encode new formula with at leat configuration and a k as bound"},
    {"encode_leq", (PyCFunction)PyPb2cnf_Encode_Leq,
	 METH_VARARGS, "Encode new formula of weighted literals with less-equals comparator and a k as bound"},
    {"encode_geq", (PyCFunction)PyPb2cnf_Encode_Geq,
	 METH_VARARGS, "Encode new formula of weighted literals with greatest-equals comparator and a k as bound"},
    {"encode_both", (PyCFunction)PyPb2cnf_Encode_Both,
	 METH_VARARGS, "Encode new formula of weighted literals with less-equals and greatest-equals  comparators and a k as bound"},
	{NULL}	/* sentinel */
};


// PyPb2cnf Python type definition
//=======================================================================

static const char* PyPb2cnf_doc = "PBLib pb2cnf structure";

PyTypeObject PyPb2cnf_Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyPb2cnf_NAME,    	   /* tp_name */
    sizeof(PyPb2cnf),                        	   /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyPb2cnf_Dealloc,                       	   /* tp_dealloc */
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
    PyPb2cnf_doc,                                  /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyPb2cnf_methods,                              /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyPb2cnf_New,                                  /* tp_new */
};

#ifdef __cplusplus
}
#endif




