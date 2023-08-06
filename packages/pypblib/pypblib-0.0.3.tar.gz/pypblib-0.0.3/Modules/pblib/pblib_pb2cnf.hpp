/*
 * PyPB pb2cnf bindings
 */

#ifndef _PBLIB_PB2CNF_HPP_
#define _PBLIB_PB2CNF_HPP_

#include <Python.h>
#include <pb2cnf.h>

#ifdef __cplusplus
extern "C" {
#endif

//Name used as refrence within Python
#define PyPb2cnf_NAME "Pb2cnf"

extern PyTypeObject PyPb2cnf_Type;

typedef struct {
    PyObject_HEAD;
    PB2CNF pb2cnf;
} PyPb2cnf;

#define PyPb2cnf_Check(x) ((x)->ob_type == &PyPb2cnf_Type)

// ***  Prototypes  ***
void Build_PyList_Formula(PyObject* py_formula, std::vector<std::vector<int>> &formula);

#ifdef __cplusplus
}

#endif

#endif  // _PBLIB_PB2CNF_HPP_

