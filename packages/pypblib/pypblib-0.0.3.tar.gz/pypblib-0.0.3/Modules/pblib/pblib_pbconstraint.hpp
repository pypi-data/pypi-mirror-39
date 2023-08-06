/*
 * PyPB PBLib::PBConstraint bindings
 */

#ifndef _PBLIB_PBCONSTRAINT_HPP_
#define _PBLIB_PBCONSTRAINT_HPP_

#include <Python.h>
#include <pbconstraint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Name used as reference within Python
#define PyPBConstraint_NAME "PBConstraint"

extern PyTypeObject PyPBConstraint_Type;

typedef struct {
	PyObject_HEAD;
	PBLib::PBConstraint constraint;
} PyPBConstraint;

#define PyPBConstraint_Check(x)  ((x)->ob_type == &PyPBConstraint_Type)
PyObject* PyPBConstraint_From_PBConstraint(const PBLib::PBConstraint &constr);

#ifdef __cplusplus
}

#endif

#endif	// _PBLIB_PBCONSTRAINT_HPP_
