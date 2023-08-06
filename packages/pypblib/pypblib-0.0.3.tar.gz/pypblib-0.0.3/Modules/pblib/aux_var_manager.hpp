/*
 *  PyOB PBLib::AuxVarManager bindings
 */

#ifndef _PBLIB_AUXVARMANAGER_HPP_
#define _PBLIB_AUXVARMANAGER_HPP_

#include <Python.h>
#include "auxvarmanager.h"

#ifdef __cplusplus
extern "C" {
#endif

// Name used as reference within Python
#define PyAuxVarManager_NAME "AuxVarManager"

extern PyTypeObject PyAuxVarManager_Type;

typedef struct {
    PyObject_HEAD;
    AuxVarManager aux_var;
}PyAuxVarManager;

#define PyAuxVarManager_Check(x)  ((x)->ob_type = &PyAuxVarManager_Type)

#ifdef __cplusplus
}

#endif 

#endif // _PBLIB_AUXVARMANAGER_HPP_
