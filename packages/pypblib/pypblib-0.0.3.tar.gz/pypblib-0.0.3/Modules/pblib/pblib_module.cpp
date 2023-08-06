/*
 * PyPB module initialization.
 */

#include <Python.h>
#include <pbconstraint.h>

#include "pblib_module.hpp"
#include "pblib_statistic.hpp"
#include "pblib_pbparser.hpp"
#include "pblib_weightedlit.hpp"
#include "pblib_pbconstraint.hpp"
#include "aux_var_manager.hpp"
#include "pblib_pbconfig.hpp"
#include "pblib_pb2cnf.hpp"
#include "pblib_vectorclausedatabase.hpp"
#include "pblib_incpbconstraint.hpp"


// The module does not contain methods. In the future this
// may change and this definition should then be moved to
// a more appropriate file.
// WARNING: Be careful with 'static' and name mangling (C++ to C)
static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

// Module definition struct
// See: https://docs.python.org/3/c-api/module.html#c.PyModuleDef
static struct PyModuleDef module_def {
    PyModuleDef_HEAD_INIT,
    PBLIB_MODULE_NAME,        /* m_name         */
    PBLIB_MODULE_DOC,         /* m_doc          */
    0,                        /* m_size (state) */
    module_methods,           /* m_methods      */
    NULL,                     /* m_slots        */
    NULL,                     /* m_traverse     */
    NULL,                     /* m_clear        */
    NULL                      /* m_free         */
};

PyMODINIT_FUNC PyInit_pblib(void)
#else
PyMODINIT_FUNC initpblib(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject* m = PyModule_Create(&module_def); // create module
    if (m == NULL) { goto finally; }       // failure
#else
    PyObject *m = Py_InitModule3(PBLIB_MODULE_NAME, module_methods,
                    PBLIB_MODULE_DOC);
    if (m == NULL) { goto finally; }       // failure
#endif
    // Adding module constants
    // Comparator constants (Probably as constants of )
    if (PyModule_AddIntConstant(m, "GEQ", PBLib::GEQ)
            || PyModule_AddIntConstant(m, "LEQ", PBLib::LEQ)
            || PyModule_AddIntConstant(m, "BOTH", PBLib::BOTH)
            || PyModule_AddIntConstant(m, "PB_BEST", PB_ENCODER::BEST)
            || PyModule_AddIntConstant(m, "PB_BDD", PB_ENCODER::BDD)
            || PyModule_AddIntConstant(m, "PB_SWC", PB_ENCODER::SWC)
            || PyModule_AddIntConstant(m, "PB_SORTINGNETWORKS", PB_ENCODER::SORTINGNETWORKS)
            || PyModule_AddIntConstant(m, "PB_ADDER", PB_ENCODER::ADDER)
            || PyModule_AddIntConstant(m, "PB_BINARY_MERGE", PB_ENCODER::BINARY_MERGE)
            || PyModule_AddIntConstant(m, "AMK_BEST", AMK_ENCODER::BEST)
            || PyModule_AddIntConstant(m, "AMK_BDD", AMK_ENCODER::BDD)
            || PyModule_AddIntConstant(m, "AMK_CARD", AMK_ENCODER::CARD)
            || PyModule_AddIntConstant(m, "AMO_BEST", AMO_ENCODER::BEST)
            || PyModule_AddIntConstant(m, "AMO_NESTED", AMO_ENCODER::NESTED)
            || PyModule_AddIntConstant(m, "AMO_BDD", AMO_ENCODER::BDD)
            || PyModule_AddIntConstant(m, "AMO_BIMANDER", AMO_ENCODER::BIMANDER)
            || PyModule_AddIntConstant(m, "AMO_COMMANDER", AMO_ENCODER::COMMANDER)
            || PyModule_AddIntConstant(m, "AMO_KPRODUCT", AMO_ENCODER::KPRODUCT)
            || PyModule_AddIntConstant(m, "AMO_BINARY", AMO_ENCODER::BINARY)
            || PyModule_AddIntConstant(m, "AMO_PAIRWISE", AMO_ENCODER::PAIRWISE)
            || PyModule_AddIntConstant(m, "N_HALF", BIMANDER_M_IS::N_HALF)
            || PyModule_AddIntConstant(m, "N_SQRT", BIMANDER_M_IS::N_SQRT)
            || PyModule_AddIntConstant(m, "FIXED", BIMANDER_M_IS::FIXED)) {
        goto init_error;
    }

    // Attach module objects
    if (PyType_Ready(&PyPBLibStatistic_Type)) { goto init_error; }
    Py_INCREF(&PyPBLibStatistic_Type);
    PyModule_AddObject(m, PyPBLibStatistic_NAME,
                       (PyObject*)&PyPBLibStatistic_Type);

    if (PyType_Ready(&PyPBLibPBParser_Type)) { goto init_error; }
    Py_INCREF(&PyPBLibPBParser_Type);
    PyModule_AddObject(m, PyPBLibPBParser_NAME,
                       (PyObject*)&PyPBLibPBParser_Type);

    if (PyType_Ready(&PyPBLibWeightedLit_Type)) { goto init_error; }
    Py_INCREF(&PyPBLibWeightedLit_Type);
    PyModule_AddObject(m, PyPBLibWeightedLit_NAME,
                       (PyObject*)&PyPBLibWeightedLit_Type);

    if (PyType_Ready(&PyPBConstraint_Type)) { goto init_error; }
    Py_INCREF(&PyPBConstraint_Type);
    PyModule_AddObject(m, PyPBConstraint_NAME,
                       (PyObject*)&PyPBConstraint_Type);

    if (PyType_Ready(&PyAuxVarManager_Type)) { goto init_error; }
    Py_INCREF(&PyAuxVarManager_Type);
    PyModule_AddObject(m, PyAuxVarManager_NAME,
                       (PyObject*)&PyAuxVarManager_Type);

    if (PyType_Ready(&PyPBConfig_Type)) { goto init_error; }
    Py_INCREF(&PyPBConfig_Type);
    PyModule_AddObject(m, PyPBConfig_NAME,
                       (PyObject*)&PyPBConfig_Type);

    if (PyType_Ready(&PyPb2cnf_Type)) { goto init_error; }
    Py_INCREF(&PyPb2cnf_Type);
    PyModule_AddObject(m, PyPb2cnf_NAME,
                       (PyObject*)&PyPb2cnf_Type);

    if (PyType_Ready(&PyVectorClauseDatabase_Type)) { goto init_error; }
    Py_INCREF(&PyVectorClauseDatabase_Type);
    PyModule_AddObject(m, PyVectorClauseDatabase_NAME,
                       (PyObject*)&PyVectorClauseDatabase_Type);

    if (PyType_Ready(&PyIncPBConstraint_Type)) { goto init_error; }
    Py_INCREF(&PyIncPBConstraint_Type);
    PyModule_AddObject(m, PyIncPBConstraint_NAME,
                       (PyObject*)&PyIncPBConstraint_Type);
    goto finally;
init_error:
    Py_XDECREF(m);
    m = NULL;
finally:
#if PY_MAJOR_VERSION >= 3
    return m;  // everything ok, return recently created module
#else
    return;
#endif
}
