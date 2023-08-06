/*
 * PyPB PBParser bindings
 */

#ifndef _PBLIB_PBPARSER_HPP_
#define _PBLIB_PBPARSER_HPP_

#include <Python.h>

#include <PBParser.h>

#ifdef __cplusplus
extern "C" {
#endif

// Name used as reference within Python
#define PyPBLibPBParser_NAME "PBParser"

extern PyTypeObject PyPBLibPBParser_Type;

typedef struct {
	PyObject_HEAD;
	struct PBParser parser;
} PyPBLibPBParser;

#define PyPBLibPBParser_Check(x)  ((x)->ob_type == &PyPBLibPBParser_Type)

#ifdef __cplusplus
}
#endif

#endif // _PBPARSER_HPP_
