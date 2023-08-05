#include "Python.h"
#include "c_parser.c"
// Does all needed includes.

static char module_docstring[] = "This module is the C code for the argument parser.";
static char _c_parser_docstring[] = "This is the actual C argument parser.";
// Adds the docstrings.

static PyObject *func_c_parser(PyObject *self, PyObject *args) {
    ArgParserStructure structure;
    if (!PyArg_ParseTuple(args, "sii", &structure.ParsingString, &structure.IgnoreQuotes, &structure.HitAllArgs)) {
        return NULL;
    }
    structure.LastParse = "";
    ArgParserStructure next = ArgParser_Next(structure);
    PyObject* obj = Py_BuildValue("siis", next.ParsingString, next.IgnoreQuotes, next.HitAllArgs, next.LastParse);
    return obj;
}
// The main function.

static PyMethodDef module_methods[] = {
    {"ArgParser_Next", func_c_parser, METH_VARARGS, _c_parser_docstring},
    {NULL}
};
// Defines the module methods.

static struct PyModuleDef _coremodule = {
    PyModuleDef_HEAD_INIT,
    "_parsethoseargs_c_parser",   /* name of module */
    module_docstring, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    module_methods,
};
// Defines the module.

PyMODINIT_FUNC PyInit__parsethoseargs_c_parser(void)
{
    return PyModule_Create(&_coremodule);
}
// Initialises the module.
