#include <Python.h>
#include "helper.hpp"


bool Get_Int_Vector_From_C_To_Python(std::vector<int> &out, PyObject *int_list) {
    PyObject *iter, *item;
    if((iter = PyObject_GetIter(int_list)) == NULL) {
        PyErr_SetString(PyExc_TypeError, "Literals and Formula must be iterable objects");
        return false;
    }

    out.clear();
    while(item = PyIter_Next(iter)) {       
        if(!PyLong_Check(item)){
            PyErr_SetString(PyExc_TypeError, "Literals must be integers");
            Py_DECREF(item);
            Py_DECREF(iter);            
            return false;
        }
        out.push_back(PyLong_AsLong(item));
        Py_DECREF(item);
    }
    Py_DECREF(iter);
    return true;
}

bool Get_Int64_Vector_From_C_To_Python(std::vector<int64_t> &out, PyObject *long_list) {

    PyObject *iter, *item;
    if((iter = PyObject_GetIter(long_list)) == NULL) {
        PyErr_SetString(PyExc_TypeError, "Literals and Formula must be iterable objects");
        return false;
    }

    out.clear();
    while(item = PyIter_Next(iter)) {       
        if(!PyLong_Check(item)){
            PyErr_SetString(PyExc_TypeError, "weights must be long");
            Py_DECREF(item);
            Py_DECREF(iter);            
            return false;
        }
        out.push_back(PyLong_AsLong(item));
        Py_DECREF(item);
    }
    Py_DECREF(iter);
    return true;
}

/*
std::vector<int>* get_int_vector(PyObject *int_list) {

    PyObject *iter, *item;
    if((iter = PyObject_GetIter(int_list)) == NULL) {
        PyErr_SetString(PyExc_TypeError, "Literals and Formula must be iterable objects");
        return NULL;
    }

    std::vector<int>* tmp = new std::vector<int>;
    while(item = PyIter_Next(iter)) {       
        if(!PyLong_Check(item)){
            PyErr_SetString(PyExc_TypeError, "Literals must be integers");
            Py_DECREF(item);
            Py_DECREF(iter);            
            return NULL;
        }
        tmp->push_back(PyLong_AsLong(item));
        Py_DECREF(item);
    }
    Py_DECREF(iter);
    return tmp;
}
*/

/*
std::vector<long>* get_long_vector(PyObject *long_list) {

    PyObject *iter, *item;
    if((iter = PyObject_GetIter(long_list)) == NULL) {
        PyErr_SetString(PyExc_TypeError, "Literals and Formula must be iterable objects");
        return NULL;
    }

    std::vector<long>* tmp = new std::vector<long>;
    while(item = PyIter_Next(iter)) {       
        if(!PyLong_Check(item)){
            PyErr_SetString(PyExc_TypeError, "Literals must be long");
            Py_DECREF(item);
            Py_DECREF(iter);            
            return NULL;
        }
        tmp->push_back(PyLong_AsLong(item));
        Py_DECREF(item);
    }
    Py_DECREF(iter);
    return tmp;
}
*/


