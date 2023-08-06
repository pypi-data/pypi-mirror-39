/*
 * PyPB PBConfig bindings
 */
#include <iostream>
#include <sstream>
#include <Python.h>

#include "pblib_module.hpp"
#include "pblib_pbconfig.hpp"

#ifdef __cplusplus
extern "C" {
#endif


//PyPBConfig base object methods
//==============================================

static void PyPBConfig_Dealloc(PyObject* raw_self)
{
    PyPBConfig* self = (PyPBConfig*)raw_self;

    self->config.~PBConfig();
    raw_self->ob_type->tp_free(self);
}

static PyObject * PyPBConfig_New(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	PyPBConfig* self = (PyPBConfig*)type->tp_alloc(type,1);
	if(self != NULL) {
		new (&self->config) PBConfig();
        self->config = std::make_shared<PBConfigClass>();
	}

	return (PyObject *) self;
}

static PyObject* PyPBConfig_Repr(PyPBConfig* self) {
    std::stringstream ss;

    ss << "\nPBConfig:\n";
    ss << "========\n";
    ss << "PB_Encoder = " << pb_encoder_to_String((long)
                                        ((PyPBConfig*)self->config->pb_encoder)) << "\n";
    ss << "AMK_Encoder = " << amk_encoder_to_string((long)
                                        ((PyPBConfig*)self->config->amk_encoder)) << "\n";
    ss << "AMO_Encoder = " << amo_encoder_to_string((long)
                                        ((PyPBConfig*)self->config->amo_encoder)) << "\n";
    ss << "BIMANDER_M_IS = " << bimander_m_to_string((long)
                                        ((PyPBConfig*)self->config->bimander_m_is)) << "\n";
    ss << "bimander = " << (long)((PyPBConfig*)self->config->bimander_m) << "\n";
    ss << "k product min lit cnt for splitting = " <<
            (long)((PyPBConfig*)self->config->k_product_minimum_lit_count_for_splitting) << "\n";
    ss << "K product k = " << (long)((PyPBConfig*)self->config->k_product_k) << "\n";
    ss << "Commander encoding k = " <<
            (long)((PyPBConfig*)self->config->commander_encoding_k) << "\n";
    ss << "Max clause per constraint = " <<
            (long)((PyPBConfig*)self->config->MAX_CLAUSES_PER_CONSTRAINT) << "\n";
    ss << "Use formula cache = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->use_formula_cache)) << "\n";
    ss << "Print used encoding = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->print_used_encodings)) << "\n";
    ss << "Check for duplicate literals = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->check_for_dup_literals)) << "\n";
    ss << "Use gac Binary Merge = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->use_gac_binary_merge)) << "\n";
    ss << "Binary merge no support for single bits = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->binary_merge_no_support_for_single_bits)) << "\n";
    ss << "Use recursive BDD test = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->use_recursive_bdd_test)) << "\n";
    ss << "Use real robdds = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->use_real_robdds)) << "\n";
    ss << "Use watch dog encoding in Binary Merger = " << boolean_value_to_string((long)
                ((PyPBConfig*)self->config->use_watch_dog_encoding_in_binary_merger)) << "\n";

    return PyUnicode_FromString(ss.str().c_str());
}


char* boolean_value_to_string(int b)
{
    if(b) return "TRUE";
    return "FALSE";
}

char* pb_encoder_to_String(int pb_e)
{
    switch (pb_e) {
        case 0: return "BEST";
        case 1: return "BDD";
        case 2: return "SWC";
        case 3: return "SORTINGNETWORKS";
        case 4: return "ADDER";
        case 5: return "BINARY MERGE";
    }
}

char* amk_encoder_to_string(int amk_e)
{
    switch(amk_e) {
        case 0: return "BEST";
        case 1: return "BDD";
        case 2: return "CARD";
    }
}

char* amo_encoder_to_string(int amo_e)
{
    switch(amo_e) {
        case 0: return "BEST";
        case 1: return "NESTED";
        case 2: return "BDD";
        case 3: return "BIMANDER";
        case 4: return "COMMANDER";
        case 5: return "KPRODUCT";
        case 6: return "BINARY";
        case 7: return "PAIRWISE";
    }
}

char* bimander_m_to_string(int bim_m)
{
    switch(bim_m) {
        case 0: return "N_HALF";
        case 1: return "N_SQRT";
        case 2: return "FIXED";
    }
}

//PyPBConfig methods
//===============================================



//PyPBConfig definition of methods, getters, setters, ...
//===============================================

static PyObject* PyPBConfig_Set_PB_Encoder(PyPBConfig* self, PyObject* encoder)
{
	PB_ENCODER::PB2CNF_PB_Encoder pb_enc;

	if(!PyArg_ParseTuple(encoder, "i", &pb_enc)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a PB_Encoder.");
        return NULL;
	}

    (self->config)->pb_encoder = pb_enc;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_AMK_Encoder(PyPBConfig* self, PyObject* encoder)
{
	AMK_ENCODER::PB2CNF_AMK_Encoder amk_enc;

	if(!PyArg_ParseTuple(encoder, "i", &amk_enc)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a AMK_Encoder.");
        return NULL;
	}

    (self->config)->amk_encoder = amk_enc;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_AMO_Encoder(PyPBConfig* self, PyObject* encoder)
{
	AMO_ENCODER::PB2CNF_AMO_Encoder amo_enc;

	if(!PyArg_ParseTuple(encoder, "i", &amo_enc)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a AMO_Encoder.");
        return NULL;
	}

    (self->config)->amo_encoder = amo_enc;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_BIMANDER(PyPBConfig* self, PyObject* encoder)
{
	BIMANDER_M_IS::BIMANDER_M_IS bimander;

	if(!PyArg_ParseTuple(encoder, "i", &bimander)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be a BIMANDER_M_IS.");
        return NULL;
	}

    (self->config)->bimander_m_is = bimander;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_Bimander_M(PyPBConfig* self, PyObject* bim_m)
{
    int bimander_m;

    if(!PyArg_ParseTuple(bim_m, "i", &bimander_m)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an int.");
        return NULL;
	}
    (self->config)-> bimander_m = bimander_m;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_K_Product_Minimum_Lit_Count_For_Splitting(PyPBConfig* self, PyObject* cnt)
{
    int count;

    if(!PyArg_ParseTuple(cnt, "i", &count)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an int.");
        return NULL;
	}
    (self->config)-> k_product_minimum_lit_count_for_splitting = count;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_K_Product_K(PyPBConfig* self, PyObject* k)
{
    int k_product;

    if(!PyArg_ParseTuple(k, "i", &k_product)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an int.");
        return NULL;
	}
    (self->config)-> k_product_k = k_product;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_Commander_encoding_K(PyPBConfig* self, PyObject* k)
{
    int commander_k;

    if(!PyArg_ParseTuple(k, "i", &commander_k)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an int.");
        return NULL;
	}
    (self->config)-> commander_encoding_k = commander_k;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_Max_Clauses_Per_Constraint(PyPBConfig* self, PyObject* max_c)
{
    long max_clauses;

    if(!PyArg_ParseTuple(max_c, "l", &max_clauses)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be an int.");
        return NULL;
	}
    (self->config)-> MAX_CLAUSES_PER_CONSTRAINT = max_clauses;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Set_Use_Formula_Cache(PyPBConfig* self, PyObject* f_bool)
{
    PyObject* formula_obj;
    bool formula_bool = false;

    if(!PyArg_ParseTuple(f_bool, "O", &formula_obj)) { goto error; }
    if(!PyBool_Check(formula_obj)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(formula_obj)) { formula_bool = true; }
    (self->config)->use_formula_cache = formula_bool;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Print_Used_Encoding(PyPBConfig* self, PyObject* p_bool)
{
    PyObject* print_ojb;
    bool print_bool = false;

    if(!PyArg_ParseTuple(p_bool, "O", &print_ojb)) { goto error; }
    if(!PyBool_Check(print_ojb)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(print_ojb)) { print_bool = true; }
    (self->config)-> print_used_encodings = print_bool;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Check_For_Dup_literals(PyPBConfig* self, PyObject* dl_bool)
{
    PyObject* duplicate_lit;
    bool duplicate_literals_bool = false;

    if(!PyArg_ParseTuple(dl_bool, "O", &duplicate_lit)) { goto error; }
    if(!PyBool_Check(duplicate_lit)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(duplicate_lit)) { duplicate_literals_bool = true; }
    (self->config)->check_for_dup_literals = duplicate_literals_bool;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Use_Gac_Binary_Merge(PyPBConfig* self, PyObject* bm_bool)
{
    PyObject* bin_merge;
    bool bin_merge_bool;

    if(!PyArg_ParseTuple(bm_bool, "O", &bin_merge)) { goto error; }
    if(!PyBool_Check(bin_merge)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(bin_merge)) { bin_merge_bool = true; }
    (self->config)->use_gac_binary_merge = bin_merge_bool;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Binary_Merge_No_Support_For_Single_Bits
                                (PyPBConfig* self, PyObject* bm_no_support)
{
    PyObject* no_support_obj;
    bool no_support_bool = false;

    if(!PyArg_ParseTuple(bm_no_support, "O", &no_support_obj)) { goto error; }
    if(!PyBool_Check(no_support_obj)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(no_support_obj)) { no_support_bool = true; }
    (self->config)-> binary_merge_no_support_for_single_bits =
                                                no_support_bool;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Use_Recursive_BDD_Test(PyPBConfig* self, PyObject* use_r)
{
    PyObject* use_recursive_obj;
    bool use_recursive_bool = false;

    if(!PyArg_ParseTuple(use_r, "O", &use_recursive_obj)) { goto error; }
    if(!PyBool_Check(use_recursive_obj)) { goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(use_recursive_obj)) { use_recursive_bool = true; }
    (self->config)->use_recursive_bdd_test = use_recursive_bool;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Use_Real_Robdds(PyPBConfig* self, PyObject* use_r_rob)
{
    PyObject* use_real_rob_obj;
    bool use_real_rob_bool = false;

    if(!PyArg_ParseTuple(use_r_rob, "O", &use_real_rob_obj)) { goto error;	}
    if(!PyBool_Check(use_real_rob_obj)) {goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(use_real_rob_obj)) { use_real_rob_bool = true; }
    (self->config)->use_real_robdds = use_real_rob_bool;
    Py_RETURN_NONE;
}

static PyObject* PyPBConfig_Use_Watch_Dog_Encoding_In_Binary_Merger
                                (PyPBConfig* self, PyObject* use_w_dog)
{
    PyObject* use_watch_dog_obj;
    bool use_watch_dog_bool = false;

    if(!PyArg_ParseTuple(use_w_dog, "O", &use_watch_dog_obj)) { goto error;	}
    if(!PyBool_Check(use_watch_dog_obj)) {goto error; }

    goto finally;

error:
    PyErr_SetString(PyExc_TypeError, "parameter must be a boolean.");
    return NULL;

finally:
    if(PyObject_IsTrue(use_watch_dog_obj)) { use_watch_dog_bool = true; }
    (self->config)->use_watch_dog_encoding_in_binary_merger = use_watch_dog_bool;
    Py_RETURN_NONE;
}


static PyMethodDef PyPBConfig_methods[] = {
	{"set_PB_Encoder", (PyCFunction)PyPBConfig_Set_PB_Encoder,
	 METH_VARARGS, "Set the PB Encoder option"},
    {"set_AMK_Encoder", (PyCFunction)PyPBConfig_Set_AMK_Encoder,
	 METH_VARARGS, "Set the AMK Encoder option"},
    {"set_AMO_Encoder", (PyCFunction)PyPBConfig_Set_AMO_Encoder,
	 METH_VARARGS, "Set the AMO Encoder option"},
    {"set_Bimander", (PyCFunction)PyPBConfig_Set_BIMANDER,
	 METH_VARARGS, "Set the BIMANDER_M_IS option"},
    {"set_bimander_m", (PyCFunction)PyPBConfig_Set_Bimander_M,
	 METH_VARARGS, "Set the BIMANDER_M"},
    {"set_k_product_minimum_lit_count_for_splitting",
    (PyCFunction)PyPBConfig_Set_K_Product_Minimum_Lit_Count_For_Splitting,
	 METH_VARARGS, "Set the k-product minimum literals for splitting"},
    {"set_k_product_k", (PyCFunction)PyPBConfig_Set_K_Product_K,
	 METH_VARARGS, "Set a K for k-product"},
    {"set_commander_encoding_k", (PyCFunction)PyPBConfig_Set_Commander_encoding_K,
	 METH_VARARGS, "Set commander encoding K"},
    {"set_max_clause_per_constraint",
    (PyCFunction)PyPBConfig_Set_Max_Clauses_Per_Constraint,
	 METH_VARARGS, "Set the maximun of clauses in every constraint"},
    {"set_use_formula_cache",
    (PyCFunction)PyPBConfig_Set_Use_Formula_Cache,
	 METH_VARARGS, "Set use of formula cache, true or false. False by default."},
    {"print_used_encoding",
    (PyCFunction)PyPBConfig_Print_Used_Encoding,
	 METH_VARARGS, "Set print used encoding.It it is true, it prints used encoding. False by default."},
    {"check_for_dup_literals",
    (PyCFunction)PyPBConfig_Check_For_Dup_literals,
	 METH_VARARGS, "Set the check for duplicate literals. Check if it is true. False by default."},
    {"use_gac_binary_merge",
    (PyCFunction)PyPBConfig_Use_Gac_Binary_Merge,
	 METH_VARARGS, "Set the check for duplicate literals. Check if it is true. False by default."},
    {"binary_merge_no_support_for_single_bits",
    (PyCFunction)PyPBConfig_Binary_Merge_No_Support_For_Single_Bits,
	 METH_VARARGS, "Set the binary merge support for single bits. True by default."},
    {"use_recursive_BDD_test",
    (PyCFunction)PyPBConfig_Use_Recursive_BDD_Test,
	 METH_VARARGS, "Set the use of recursive BDD test. False by default."},
    {"use_real_robdds",
    (PyCFunction)PyPBConfig_Use_Real_Robdds,
	 METH_VARARGS, "Set the use of real robdds. True by default."},
    {"use_watch_dog_encoding_in_binary_merger",
    (PyCFunction)PyPBConfig_Use_Watch_Dog_Encoding_In_Binary_Merger,
	 METH_VARARGS, "Set use watch dog encoding in binary merge. False by default."},
	{NULL}	/* sentinel */
};


// PyPBConfig Python type definition
//=============================================================================

static const char* PyPBConfig_doc = "PBLib pbconfig structure";

PyTypeObject PyPBConfig_Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
    PBLIB_MODULE_NAME "." PyPBConfig_NAME,	       /* tp_name */
    sizeof(PyPBConfig),                    	       /* tp_basicsize */
    0,                                             /* tp_itemsize */
    PyPBConfig_Dealloc,                    	       /* tp_dealloc */
    NULL,                                          /* tp_print */
    NULL,                                          /* tp_getattr */
    NULL,                                          /* tp_setattr */
    NULL,                                          /* tp_compare */
    (reprfunc)PyPBConfig_Repr,                     /* tp_repr */
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
    PyPBConfig_doc,                                /* tp_doc */
    NULL,                                          /* tp_traverse */
    NULL,                                          /* tp_clear */
    NULL,                                          /* tp_richcompare */
    0,                                             /* tp_weaklistoffset */
    NULL,                                          /* tp_iter */
    NULL,                                          /* tp_iternext */
    PyPBConfig_methods,                            /* tp_methods */
    NULL,                                          /* tp_members */
    NULL,                                          /* tp_getset */
    NULL,                                          /* tp_base */
    NULL,                                          /* tp_dict */
    NULL,                                          /* tp_descr_get */
    NULL,                                          /* tp_descr_set */
    0,                                             /* tp_dictoffset */
    NULL,                                          /* tp_init */
    NULL,                                          /* tp_alloc */
    PyPBConfig_New,                                /* tp_new */
};

#ifdef __cplusplus
}
#endif

