/*
 * PyPB PBLib::IncPBConstraint bindings
 */
#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_weightedlit.hpp"
#include "pblib_pbconstraint.hpp"
#include "pblib_incpbconstraint.hpp"
#include "pblib_vectorclausedatabase.hpp"
#include "aux_var_manager.hpp"


// PyIncPBConstraint Utility methods
//=====================================================================

inline PyObject* PyIncPBConstraint_One_Bound_From_Raw_Data(PyTypeObject* type,
                                const std::vector<PBLib::WeightedLit> &wlits,
                                PBLib::Comparator comp, long bound)
{
    PyIncPBConstraint* self = (PyIncPBConstraint*)type->tp_alloc(type,1);
	if(self != NULL) {
        new (&self->incconstraint) IncPBConstraint(wlits, comp, bound);
	}

	return (PyObject *) self;
}

inline PyObject* PyIncPBConstraint_Two_Bound_From_Raw_Data(PyTypeObject* type,
                                const std::vector<PBLib::WeightedLit> &wlits,
                                PBLib::Comparator comp, long bound, long bound2)
{
    PyIncPBConstraint* self = (PyIncPBConstraint*)type->tp_alloc(type,1);
	if(self != NULL) {
        new (&self->incconstraint) IncPBConstraint(wlits, comp, bound, bound2);
	}

	return (PyObject *) self;
}

PyObject* PyIncPBConstraint_From_IncPBConstraint(const IncPBConstraint &i_constr)
{
  return PyIncPBConstraint_Two_Bound_From_Raw_Data(&PyIncPBConstraint_Type,
                                                i_constr.getWeightedLiterals(),
                                                i_constr.getComparator(),
                                                i_constr.getLeq(),
                                                i_constr.getGeq());
}


#ifdef __cplusplus
extern "C" {
#endif


//PyIncPBConstraint base object methods
//====================================================================

static void PyIncPBConstraint_Dealloc(PyObject* self)
{
	self->ob_type->tp_free(self);
}


static PyObject * PyIncPBConstraint_New(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    bool two_bound = false;

    if(PyTuple_Size(args) == 4) { two_bound = true; }

	PyObject *seq;
	PBLib::Comparator comp;
	long bound;
    long bound2;

    if(two_bound) {
        if(!PyArg_ParseTuple(args, "Oill", &seq, &comp, &bound, &bound2)) {
    		PyErr_SetString(PyExc_TypeError,
                    "parameter must be a WeightedLits list, comparator & two longs.");
    		return NULL;
    	}
    }
    else {
    	if(!PyArg_ParseTuple(args, "Oil", &seq, &comp, &bound)) {
    		PyErr_SetString(PyExc_TypeError,
                    "parameter must be a WeightedLits list, comparator & long.");
    		return NULL;
    	}
	}

	PyObject *iter, *item;
    if ((iter = PyObject_GetIter(seq)) == NULL) {
        PyErr_SetString(PyExc_TypeError, "First parameter must be iterable");
        return NULL;
    }

    std::vector<PBLib::WeightedLit> wlits;
    while (item = PyIter_Next(iter)) {
        if (!PyPBWeightedLit_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "First parameter must be a list of WeightedLits.");
            Py_DECREF(item);
            Py_DECREF(iter);
            return NULL;
        }

        wlits.push_back(((PyPBLibWeightedLit*)item)->wl);
        Py_DECREF(item);
    }

    Py_DECREF(iter);

    if(two_bound)
        return PyIncPBConstraint_Two_Bound_From_Raw_Data(type, wlits, comp, bound, bound2);

    return PyIncPBConstraint_One_Bound_From_Raw_Data(type, wlits, comp, bound);
}


static PyObject* PyIncPBConstraint_Repr(PyIncPBConstraint* self) {
    std::stringstream ss;
    std::vector<PBLib::WeightedLit> weighted_lits = ((PyIncPBConstraint*)self)->
                                            incconstraint.getWeightedLiterals();

    if(((PyIncPBConstraint*)self)->incconstraint.getComparator() == PBLib::BOTH) {
        ss << ((PyIncPBConstraint*)self)->incconstraint.getGeq() << "<=";
    }

    for (auto wl : weighted_lits) {

        if(wl.weight > 0) { ss << "+"; }

        if(wl.weight != 1) { ss << wl.weight; }

        ss << "x" << wl.lit;
	}

    if(((PyIncPBConstraint*)self)->incconstraint.getComparator() == PBLib::GEQ) {
        ss << ">=" << ((PyIncPBConstraint*)self)->incconstraint.getGeq();
    }
    else {
        ss << "<=" << ((PyIncPBConstraint*)self)->incconstraint.getLeq();
    }

    return PyUnicode_FromString(ss.str().c_str());
}

static PyObject* PyIncPBConstraint_Str(PyIncPBConstraint* self) {
    std::stringstream ss;
    std::vector<PBLib::WeightedLit> weighted_lits = ((PyIncPBConstraint*)self)->
                                            incconstraint.getWeightedLiterals();
    for (auto wl : weighted_lits) {
        ss << "[" << wl.lit << ", " << wl.weight << "] ";
	}
    return PyUnicode_FromString(ss.str().c_str());
}



// PyPBConstraint methods
//=============================================================================

static PyObject* PyIncPBConstraint_Add_Conditional(PyIncPBConstraint* self, PyObject* args)
{
	int lit;
	if(!PyArg_ParseTuple(args, "i", &lit)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an int.");
		return NULL;
	}
	self->incconstraint.addConditional(lit);
	Py_RETURN_NONE;
}


static PyObject* PyIncPBConstraint_Add_Conditionals(PyIncPBConstraint* self, PyObject* args) {

    PyObject* lit_vect;
	if(!PyArg_ParseTuple(args, "O", &lit_vect)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a vector of integers");
		return NULL;
	}

    std::vector<int> literals;
    if(Get_Int_Vector_From_C_To_Python(literals, lit_vect)) {
    	self->incconstraint.addConditionals(literals);
    }
	Py_RETURN_NONE;
}


static PyObject* PyIncPBConstraint_Clear_Conditionals(PyIncPBConstraint* self, void*) {
	self->incconstraint.clearConditionals();
    Py_RETURN_NONE;
}


static PyObject* PyIncPBConstraint_Get_Conditionals(PyIncPBConstraint* self, void* /*clousure*/)
{
	std::vector<int> c_list = self->incconstraint.getConditionals();
	PyObject* list = PyList_New(0);
	PyObject* item;

	for (unsigned int i = 0; i < c_list.size(); i++) {
		item = Py_BuildValue("i", c_list[i]);
		PyList_Append(list, item);
	}
	return list;
}


static PyObject* Get_WeightedLiterals(PyIncPBConstraint* self, void* /*clousure*/)
{
    std::vector<PBLib::WeightedLit> c_list = self->incconstraint.getWeightedLiterals();
	PyObject* list = PyList_New(0);
    PyObject* item = NULL;

    if (list == NULL) { goto error; }
	for (unsigned int i = 0; i < c_list.size(); i++) {
        item = PyWeightedLit_From_WeightedLit(c_list[i]);

        if(item == NULL) {
            PyErr_SetString(PyExc_TypeError, "PyWeightedLit can't be built from C WeightedLit.");
            goto error;
        }

        if(PyList_Append(list, item)) {
            PyErr_SetString(PyExc_TypeError, "PyWeightedLit can't be appended to the list.");
            goto error;
        } else {
            Py_DECREF(item);
        }
	}
	return (PyObject *)list;
error:
    if (item != NULL) { Py_DECREF(item); }
    if (list != NULL) { Py_DECREF(list); }
    return NULL;
}


static PyObject* PyIncPBConstraint_Get_Leq(PyIncPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("l", self->incconstraint.getLeq());
}


static PyObject* PyIncPBConstraint_Get_Geq(PyIncPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("l", self->incconstraint.getGeq());
}


static PyObject* PyIncPBConstraint_Get_Comparator(PyIncPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("i", self->incconstraint.getComparator());
}


static PyObject* PyIncPBConstraint_Get_N(PyIncPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("i", self->incconstraint.getN());
}


static PyObject* PyIncPBConstraint_Set_Comparator(PyIncPBConstraint* self, PyObject* args)
{
	PBLib::Comparator comp;
	if(!PyArg_ParseTuple(args, "i", &comp)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an comparator.");
		return NULL;
	}
	self->incconstraint.setComparator(comp);
	Py_RETURN_NONE;
}


static PyObject* PyIncPBConstraint_Encode_New_Geq(PyIncPBConstraint* self, PyObject* args) {
    long new_geq;
    PyObject* clause_db;
    PyObject* aux_v;

    if(!PyArg_ParseTuple(args, "lOO", &new_geq, &clause_db, &aux_v)){ goto error; }
    if(!PyVectorClauseDatabase_Check(clause_db) ||
       !PyAuxVarManager_Check(aux_v))
       { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameters must be long, ClauseDatabase and AuxVarManager.");
    return NULL;

finally:
    self->incconstraint.encodeNewGeq(new_geq,
                                    ((PyVectorClauseDatabase*)clause_db)->vector_cdb,
                                    ((PyAuxVarManager*)aux_v)->aux_var);
	Py_RETURN_NONE;
}


static PyObject* PyIncPBConstraint_Encode_New_Leq(PyIncPBConstraint* self, PyObject* args) {
    long new_leq;
    PyObject* clause_db;
    PyObject* aux_v;

    if(!PyArg_ParseTuple(args, "lOO", &new_leq, &clause_db, &aux_v)){ goto error; }
    if(!PyVectorClauseDatabase_Check(clause_db) ||
       !PyAuxVarManager_Check(aux_v))
       { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameters must be long, ClauseDatabase and AuxVarManager.");
    return NULL;

finally:
    self->incconstraint.encodeNewLeq(new_leq,
                                    ((PyVectorClauseDatabase*)clause_db)->vector_cdb,
                                    ((PyAuxVarManager*)aux_v)->aux_var);
	Py_RETURN_NONE;
}


static PyObject* PyIncPBConstraint_Get_Non_Inc_Constraint(PyIncPBConstraint* self)
{
    return PyPBConstraint_From_PBConstraint(self->incconstraint.getNonIncConstraint());
}

static PyObject* PyIncPBConstraint_Get_Geq_Constraint(PyIncPBConstraint* self)
{
    return PyIncPBConstraint_From_IncPBConstraint(self->incconstraint.getGeqConstraint());
}


static PyObject* PyIncPBConstraint_Get_Leq_Constraint(PyIncPBConstraint* self)
{
    return PyIncPBConstraint_From_IncPBConstraint(self->incconstraint.getLeqConstraint());
}

// PyPBConstraint definition of methods, members, getters, setters, ...
//=============================================================================

static PyMethodDef PyIncPBConstraint_methods[] = {
	{"add_conditional", (PyCFunction)PyIncPBConstraint_Add_Conditional,
	 METH_VARARGS, "Adds a new conditional to IncPBConstraint"},
	{"add_conditionals", (PyCFunction)PyIncPBConstraint_Add_Conditionals,
	 METH_VARARGS, "Adds a new vector of conditional to IncPBConstraint"},
	{"clear_conditionals", (PyCFunction)PyIncPBConstraint_Clear_Conditionals,
	 METH_NOARGS, "deletes all conditionals in this IncPBConstraint"},
	{"get_conditionals", (PyCFunction)PyIncPBConstraint_Get_Conditionals,
	 METH_NOARGS, "Returns a vector of conditionals of this PBConstraint"},
    {"get_weighted_literals", (PyCFunction)Get_WeightedLiterals,
	 METH_NOARGS, "Returns a vector of weighted literals in IncPBContraint"},
    {"get_leq", (PyCFunction)PyIncPBConstraint_Get_Leq,
	 METH_NOARGS, "Returns an integer that represents the less-equal bound of this IncPBConstraint"},
    {"get_geq", (PyCFunction)PyIncPBConstraint_Get_Geq,
	 METH_NOARGS, "Return an integer that represents the greater-equal bound of this IncPBConstraint"},
    {"encode_new_geq", (PyCFunction)PyIncPBConstraint_Encode_New_Geq,
	 METH_VARARGS, "Encode a incremental constraint whith a new geq bound"},
    {"encode_new_leq", (PyCFunction)PyIncPBConstraint_Encode_New_Leq,
	 METH_VARARGS, "Encode a incremental constraint whith a new leq bound"},
    {"get_non_inc_constraint", (PyCFunction)PyIncPBConstraint_Get_Non_Inc_Constraint,
	 METH_VARARGS, "Returns a new PBConstraint with the atributes of IncPBConstraint which takes as a parameter."},
    {"get_geq_inc_constraint", (PyCFunction)PyIncPBConstraint_Get_Geq_Constraint,
	 METH_VARARGS, "Takes a incremental pseudo boolean constraint and returns a new IncPBConstraint changing the comparator to a greater-equal."},
    {"get_leq_inc_constraint", (PyCFunction)PyIncPBConstraint_Get_Leq_Constraint,
	 METH_VARARGS, "Takes a incremental pseudo boolean constraint and returns a new IncPBConstraint changing the comparator to a less-equal."},
    {"get_comparator", (PyCFunction)PyIncPBConstraint_Get_Comparator,
	 METH_VARARGS, "Return the incremental cosntraint's comparator"},
    {"set_comparator", (PyCFunction)PyIncPBConstraint_Set_Comparator,
	 METH_VARARGS, "Set comparator to the specified value (LEQ, GEQ or BOTH)"},
  	{"get_n", (PyCFunction)PyIncPBConstraint_Get_N,
	 METH_NOARGS, "Return a number of weighted Literals"},
	{NULL}	/* sentinel */
};


// PBLib IncPBConstraint Python type definition
//=============================================================================

static const char* PyIncPBConstraint_doc = "PBLib incpbconstraint structure";

PyTypeObject PyIncPBConstraint_Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyIncPBConstraint_NAME,  /* tp_name */
    sizeof(PyIncPBConstraint),                     /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyIncPBConstraint_Dealloc,                 	   /* tp_dealloc */
    NULL,                                          /* tp_print */
    NULL,                                          /* tp_getattr */
    NULL,                                          /* tp_setattr */
    NULL,                                          /* tp_compare */
    (reprfunc)PyIncPBConstraint_Repr,              /* tp_repr */
    NULL,                                          /* tp_as_number */
    NULL,                                          /* tp_as_sequence */
    NULL,                                          /* tp_as_mapping */
    PyObject_HashNotImplemented,                   /* tp_hash */
    NULL,                                          /* tp_call */
    (reprfunc)PyIncPBConstraint_Str,               /* tp_str */
    NULL,                                          /* tp_getattro */
    NULL,                                          /* tp_setattro */
    NULL,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                            /* tp_flags */
    PyIncPBConstraint_doc,                         /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyIncPBConstraint_methods,                     /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyIncPBConstraint_New,                         /* tp_new */
};

#ifdef __cplusplus
}
#endif










