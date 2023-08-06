/*
 * PyPB PBLib::weightedlit bindings
 */

#ifndef _PBLIB_WEIGHTEDLIT_HPP_
#define _PBLIB_WEIGHTEDLIT_HPP_

#include <Python.h>
#include <weightedlit.h>

#ifdef __cplusplus
extern "C" {
#endif

// Name used as reference within Python
#define PyPBLibWeightedLit_NAME "WeightedLit"

extern PyTypeObject PyPBLibWeightedLit_Type;

typedef struct {
	PyObject_HEAD;
	PBLib::WeightedLit wl;
} PyPBLibWeightedLit;

#define PyPBWeightedLit_Check(x)  ((x)->ob_type == &PyPBLibWeightedLit_Type)

// Utility functions
PyObject * PyWeightedLit_From_WeightedLit(const PBLib::WeightedLit &wl);


#ifdef __cplusplus
}

#endif

#endif  // _PBLIB_WEIGHTEDLIT_HPP_
