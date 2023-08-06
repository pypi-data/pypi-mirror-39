/*
 * PyPB VectorClauseDatabase
 */

#ifndef _PBLIB_VECTORCLAUSEDATABASE_HPP_
#define _PBLIB_VECTORCLAUSEDATABASE_HPP_

#include <Python.h>
#include <VectorClauseDatabase.h>

#ifdef __cplusplus
extern "C" {
#endif

//Name used as reference within Python
#define PyVectorClauseDatabase_NAME "VectorClauseDatabase"

extern PyTypeObject PyVectorClauseDatabase_Type;

typedef struct {
    PyObject_HEAD;
    VectorClauseDatabase vector_cdb;
} PyVectorClauseDatabase;

#define PyVectorClauseDatabase_Check(x) ((x)->ob_type == &PyVectorClauseDatabase_Type)

#ifdef __cplusplus
}

#endif

#endif  // _PBLIB_VECTORCLAUSEDATABASE_HPP_
