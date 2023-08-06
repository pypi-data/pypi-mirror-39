#ifndef _HELPER_HPP_
#define _HELPER_HPP_
#include <vector>

bool Get_Int_Vector_From_C_To_Python(std::vector<int> &out, PyObject *int_list);
bool Get_Int64_Vector_From_C_To_Python(std::vector<int64_t> &out, PyObject *long_list);

#endif	// _HELPER_HPP_
