/*
 * PyPB PBConfig
 */

#ifndef _PBLIB_PBCONFIG_HPP_
#define _PBLIB_PBCONFIG_HPP_

#include <Python.h>
#include <PBConfig.h>

#ifdef __cplusplus
extern "C" {
#endif

// Name used as reference within Python
#define PyPBConfig_NAME "PBConfig"

extern PyTypeObject PyPBConfig_Type;

typedef struct {
    PyObject_HEAD;
    PBConfig config;
} PyPBConfig;

#define PyPBConfig_Check(x)  ((x)->ob_type == &PyPBConfig_Type)

// ***  Prototypes  ***
char* boolean_value_to_string(int b);
char* pb_encoder_to_String(int pb_e);
char* amk_encoder_to_string(int amk_e);
char* amo_encoder_to_string(int amo_e);
char* bimander_m_to_string(int bim_m);

#ifdef __cplusplus
}

#endif

#endif //_PBLIB_PBCONFIG_HPP_
