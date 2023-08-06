/*
 * PyPB PBLib::PBConstraint bindings
 */
#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_weightedlit.hpp"
#include "pblib_pbconstraint.hpp"


// PyPBConstraint Utility methods
//=====================================================================

inline PyObject* PyPBConstraint_One_Bound_From_Raw_Data(PyTypeObject* type,
                                const std::vector<PBLib::WeightedLit> &wlits,
                                PBLib::Comparator comp, long bound)
{
    PyPBConstraint* self = (PyPBConstraint*)type->tp_alloc(type,1);
	if(self != NULL) {
        new (&self->constraint) PBLib::PBConstraint(wlits, comp, bound);
	}

	return (PyObject *) self;
}

inline PyObject* PyPBConstraint_Two_Bound_From_Raw_Data(PyTypeObject* type,
                                const std::vector<PBLib::WeightedLit> &wlits,
                                PBLib::Comparator comp, long bound, long bound2)
{
    PyPBConstraint* self = (PyPBConstraint*)type->tp_alloc(type,1);
	if(self != NULL) {
        new (&self->constraint) PBLib::PBConstraint(wlits, comp, bound, bound2);
	}

	return (PyObject *) self;
}

PyObject* PyPBConstraint_From_PBConstraint(const PBLib::PBConstraint &constr)
{
  return PyPBConstraint_Two_Bound_From_Raw_Data(&PyPBConstraint_Type,
                                                constr.getWeightedLiterals(),
                                                constr.getComparator(),
                                                constr.getLeq(),
                                                constr.getGeq());
}


#ifdef __cplusplus
extern "C" {
#endif


//PyPBConstraint base object methods
//====================================================================

static void PyPBConstraint_Dealloc(PyObject* self)
{
	self->ob_type->tp_free(self);
}


static PyObject* PyPBConstraint_New(PyTypeObject *type, PyObject *args, PyObject *kwds)
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

    if(two_bound) {
        return PyPBConstraint_Two_Bound_From_Raw_Data(type, wlits, comp, bound, bound2);
    }
    return PyPBConstraint_One_Bound_From_Raw_Data(type, wlits, comp, bound);
}


static PyObject* PyPBConstraint_Repr(PyPBConstraint* self) {
    std::stringstream ss;
    std::vector<PBLib::WeightedLit> weighted_lits = ((PyPBConstraint*)self)->
                                            constraint.getWeightedLiterals();

    if(((PyPBConstraint*)self)->constraint.getComparator() == PBLib::BOTH) {
        ss << ((PyPBConstraint*)self)->constraint.getGeq() << "<=";
    }

    for (auto wl : weighted_lits) {
        if(wl.weight > 0) { ss << "+"; }
        if(wl.weight != 1) { ss << wl.weight; }

        ss << "x" << wl.lit;
	}

    if(((PyPBConstraint*)self)->constraint.getComparator() == PBLib::GEQ) {
        ss << ">=" << ((PyPBConstraint*)self)->constraint.getGeq();
    }
    else {
        ss << "<=" << ((PyPBConstraint*)self)->constraint.getLeq();
    }

    return PyUnicode_FromString(ss.str().c_str());
}

static PyObject* PyPBConstraint_Str(PyPBConstraint* self) {
    std::stringstream ss;
    std::vector<PBLib::WeightedLit> weighted_lits = ((PyPBConstraint*)self)->
                                            constraint.getWeightedLiterals();
    for (auto wl : weighted_lits) {
        ss << "[" << wl.lit << ", " << wl.weight << "] ";
	}
    return PyUnicode_FromString(ss.str().c_str());
}


// PyPBConstraint methods
//=============================================================================

static PyObject* PyPBConstraint_Add_Conditional(PyPBConstraint* self, PyObject* args)
{
	int lit;
	if(!PyArg_ParseTuple(args, "i", &lit)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an int.");
		return NULL;
	}
	self->constraint.addConditional(lit);
	Py_RETURN_NONE;
}

static PyObject* PyPBConstraint_Add_Conditionals(PyPBConstraint* self, PyObject* args) {

    PyObject* lit_vect;
	if(!PyArg_ParseTuple(args, "O", &lit_vect)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a vector of integers");
		return NULL;
	}

    std::vector<int> lits;
    if(Get_Int_Vector_From_C_To_Python(lits, lit_vect)) {
        self->constraint.addConditionals(lits);
    }

	Py_RETURN_NONE;
}


static PyObject* PyPBConstraint_Clear_Conditionals(PyPBConstraint* self, void*) {
	self->constraint.clearConditionals();
    Py_RETURN_NONE;
}


static PyObject* PyPBConstraint_Get_Conditionals(PyPBConstraint* self, void* /*clousure*/)
{
	std::vector<int> c_list = self->constraint.getConditionals();
	PyObject* list = PyList_New(0);
	PyObject* item;

	for (unsigned int i = 0; i < c_list.size(); i++) {
		item = Py_BuildValue("i", c_list[i]);
		PyList_Append(list, item);
	}
	return list;
}


static PyObject* PyPBConstraint_Get_N(PyPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("i", self->constraint.getN());
}


static PyObject* Get_WeightedLiterals(PyPBConstraint* self, void* /*clousure*/)
{
    std::vector<PBLib::WeightedLit> c_list = self->constraint.getWeightedLiterals();
	PyObject* list = PyList_New(0);
    PyObject* item = NULL;

    if (list == NULL) { goto error; }
	for (unsigned int i = 0; i < c_list.size(); i++) {
        item = PyWeightedLit_From_WeightedLit(c_list[i]);

        if(item == NULL) {
            PyErr_SetString(PyExc_TypeError, "this is an error.");
            goto error;
        }

        if(PyList_Append(list, item)) {
            PyErr_SetString(PyExc_TypeError, "this is an error.");
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


static PyObject* PyPBConstraint_Get_Leq(PyPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("l", self->constraint.getLeq());
}


static PyObject* PyPBConstraint_Get_Geq(PyPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("l", self->constraint.getGeq());
}

static PyObject* PyPBConstraint_Get_Comparator(PyPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("i", self->constraint.getComparator());
}

static PyObject* PyPBConstraint_Get_Min_Sum(PyPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("l", self->constraint.getMinSum());
}

static PyObject* PyPBConstraint_Get_Max_Sum(PyPBConstraint* self, void* /*clousure*/)
{
	return Py_BuildValue("l", self->constraint.getMaxSum());
}

static PyObject* PyPBConstraint_Set_Comparator(PyPBConstraint* self, PyObject* args)
{
	PBLib::Comparator comp;
	if(!PyArg_ParseTuple(args, "i", &comp)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an comparator.");
		return NULL;
	}
	self->constraint.setComparator(comp);
	Py_RETURN_NONE;
}

static PyObject* PyPBConstraint_Set_Leq(PyPBConstraint* self, PyObject* args)
{
	long leq;
	if(!PyArg_ParseTuple(args, "l", &leq)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a long.");
		return NULL;
	}
	self->constraint.setLeq(leq);
	Py_RETURN_NONE;
}

static PyObject* PyPBConstraint_Set_Geq(PyPBConstraint* self, PyObject* args)
{
	long geq;
	if(!PyArg_ParseTuple(args, "l", &geq)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a long.");
		return NULL;
	}
	self->constraint.setGeq(geq);
	Py_RETURN_NONE;
}


static PyObject* PyPBConstraint_Get_Geq_Constraint(PyPBConstraint* self) {
    return PyPBConstraint_From_PBConstraint(self->constraint.getGeqConstraint());
}

static PyObject* PyPBConstraint_Get_Leq_Constraint(PyPBConstraint* self) {
    return PyPBConstraint_From_PBConstraint(self->constraint.getLeqConstraint());
}


// PyPBConstraint definition of methods, members, getters, setters, ...
//=============================================================================

static PyMethodDef PyPBConstraint_methods[] = {
	{"add_conditional", (PyCFunction)PyPBConstraint_Add_Conditional,
	 METH_VARARGS, "Add a new conditional to PBConstraint"},
	{"add_conditionals", (PyCFunction)PyPBConstraint_Add_Conditionals,
	 METH_VARARGS, "Add a new vector of conditional to PBConstraint"},
	{"clear_conditionals", (PyCFunction)PyPBConstraint_Clear_Conditionals,
	 METH_NOARGS, "delete all conditionals in this PBConstraint"},
	{"get_conditionals", (PyCFunction)PyPBConstraint_Get_Conditionals,
	 METH_NOARGS, "Returns a vector of conditionals of this PBConstraint"},
    {"get_weighted_literals", (PyCFunction)Get_WeightedLiterals,
	 METH_NOARGS, "Returns a copy of the vector of weighted literals which PBContraint contains"},
    {"get_leq", (PyCFunction)PyPBConstraint_Get_Leq,
	 METH_NOARGS, "Returns the constraint's less equal bound"},
    {"get_geq", (PyCFunction)PyPBConstraint_Get_Geq,
	 METH_NOARGS, "Returns the constraint's greater equal bound"},
    {"get_comparator", (PyCFunction)PyPBConstraint_Get_Comparator,
	 METH_NOARGS, "Returns the cosntraint's comparator"},
    {"get_geq_constraint", (PyCFunction)PyPBConstraint_Get_Geq_Constraint,
	 METH_VARARGS, "Takes a pseudo boolean constraint and returns a new PBConstraint changing the comparator to a greater-equal."},
    {"get_leq_constraint", (PyCFunction)PyPBConstraint_Get_Leq_Constraint,
	 METH_VARARGS, "Takes a pseudo boolean constraint and returns a new PBConstraint changing the comparator to a less-equal."},
    {"get_min_sum", (PyCFunction)PyPBConstraint_Get_Min_Sum,
	 METH_NOARGS, "Returns the minimum sum of literal's weight"},
    {"get_max_sum", (PyCFunction)PyPBConstraint_Get_Max_Sum,
	 METH_NOARGS, "Returns the maximun sum of literal's weight"},
    {"set_leq", (PyCFunction)PyPBConstraint_Set_Leq,
	 METH_VARARGS, "Sets the less equal bound to the specified value"},
    {"set_geq", (PyCFunction)PyPBConstraint_Set_Geq,
	 METH_VARARGS, "Sets the greater equal bound to the specified value"},
    {"get_n", (PyCFunction)PyPBConstraint_Get_N,
	 METH_NOARGS, "Returns the number of weighted Literals"},
    {"set_comparator", (PyCFunction)PyPBConstraint_Set_Comparator,
	 METH_VARARGS, "Sets the comparator to the specified value (LEQ, GEQ or BOTH)"},
	{NULL}	/* sentinel */
};


// PBLib PBConstraint Python type definition
//=============================================================================

static const char* PyPBConstraint_doc = "PBLib pbconstraint structure";

PyTypeObject PyPBConstraint_Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyPBConstraint_NAME,	   /* tp_name */
    sizeof(PyPBConstraint),                    	   /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyPBConstraint_Dealloc,                    	   /* tp_dealloc */
    NULL,                                          /* tp_print */
    NULL,                                          /* tp_getattr */
    NULL,                                          /* tp_setattr */
    NULL,                                          /* tp_compare */
    (reprfunc)PyPBConstraint_Repr,                 /* tp_repr */
    NULL,                                          /* tp_as_number */
    NULL,                                          /* tp_as_sequence */
    NULL,                                          /* tp_as_mapping */
    PyObject_HashNotImplemented,                   /* tp_hash */
    NULL,                                          /* tp_call */
    (reprfunc)PyPBConstraint_Str,                  /* tp_str */
    NULL,                                          /* tp_getattro */
    NULL,                                          /* tp_setattro */
    NULL,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                            /* tp_flags */
    PyPBConstraint_doc,                            /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyPBConstraint_methods,                        /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyPBConstraint_New,                            /* tp_new */
};

#ifdef __cplusplus
}
#endif
