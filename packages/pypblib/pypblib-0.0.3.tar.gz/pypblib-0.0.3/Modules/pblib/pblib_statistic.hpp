/*
 * PyPB PBLib::statistics bindings
 */

#ifndef _PBLIB_STATISTICS_HPP_
#define _PBLIB_STATISTICS_HPP_

#include <Python.h>

#include <PBConfig.h>

#ifdef __cplusplus
extern "C" {
#endif


// Name used as reference within Python
#define PyPBLibStatistic_NAME "Statistic"

extern PyTypeObject PyPBLibStatistic_Type;

typedef struct {
    PyObject_HEAD;
    struct statistic statistic;
} PyPBLibStatistic;

#define PyPBLibStatistic_Check(x)  ((x)->ob_type == &PyPBLibStatistic_Type)

#ifdef __cplusplus
}
#endif

#endif  // _PBLIB_STATISTICS_HPP_
