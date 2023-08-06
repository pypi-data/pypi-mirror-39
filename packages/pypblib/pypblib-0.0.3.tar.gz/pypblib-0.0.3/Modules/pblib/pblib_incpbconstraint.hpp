/*
 * PyPB IncPBConstraint bindings
 */

#ifndef _PBLIB_INCPBCONSTRAINT_HPP_
#define _PBLIB_INCPBCONSTRAINT_HPP_

#include <Python.h>
#include <incpbconstraint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Name used as reference within Python
#define PyIncPBConstraint_NAME "IncPBConstraint"

extern PyTypeObject PyIncPBConstraint_Type;

typedef struct {
	PyObject_HEAD;
	IncPBConstraint incconstraint;
} PyIncPBConstraint;

#define PyIncPBConstraint_Check(x)  ((x)->ob_type == &PyIncPBConstraint_Type)

#ifdef __cplusplus
}

#endif

#endif	// _PBLIB_INCPBCONSTRAINT_HPP_
