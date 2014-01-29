// python.cpp
// DVM
// Mathijs Saey

/*
 * The MIT License (MIT)
 * 
 * Copyright (c) 2014 Mathijs Saey
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy 		
 * of this software and associated documentation files (the "Software"), to deal		      
 * in the Software without restriction, including without limitation the rights		
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell		
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "python.hpp"

static const char * pyName = "DVMPy";

static Log pyMetaLog = LOG_CREATE("pyMeta");
static Log pyLog = LOG_CREATE("pyLog");

/////////////////////////////////////
// Initialization and Finalization //
/////////////////////////////////////

void python_start(int argc, char * argv[]) {
	LOG(pyMetaLog, info) << "Starting python interpreter";

	// Set program name and start interpreter
	Py_SetProgramName(const_cast<char*>(pyName));
	Py_Initialize();

	// Pass modified argv to python sys and restore argv
	char * progName = argv[0];
	argv[0] = const_cast<char*>(pyName);
	PySys_SetArgv(argc, argv);
	argv[0] = progName;

	LOG(pyMetaLog, info) << "Python interpreter ready";
}

void python_stop() {
	LOG(pyMetaLog, info) << "Terminating python interpreter";
	Py_Finalize();

	if (Py_IsInitialized()) {
		LOG(pyMetaLog, error) << "Could not terminate python interpreter";
	}
}

////////////////////
// Python Methods //
////////////////////

static inline PyObject * logFromPython(LogLevel level, PyObject * self, PyObject * args) {
	const char * message;

	if (PyArg_ParseTuple(args, "s", &message)) {
		LOG(pyLog, level) << message;
		return Py_None;
	}
	return NULL;
}

static PyObject * pyLogDebug(PyObject * self, PyObject * args) { 
	return logFromPython(debug, self, args);
}
static PyObject * pyLogInfo(PyObject * self, PyObject * args) {
	return logFromPython(info, self, args);
}
static PyObject * pyLogWarning(PyObject * self, PyObject * args) {
	return logFromPython(warning, self, args);
}
static PyObject * pyLogError(PyObject * self, PyObject * args) {
	return logFromPython(error, self, args);
}

static PyMethodDef logMethods[] = {
	{"logDebug",   pyLogDebug,   METH_VARARGS, NULL},
	{"logInfo",    pyLogInfo,    METH_VARARGS, NULL},
	{"logWarning", pyLogWarning, METH_VARARGS, NULL},
	{"logError",   pyLogError,   METH_VARARGS, NULL},
	{NULL, NULL, 0, NULL}
};

void python_extend() {
	Py_InitModule("dvmLog", logMethods);
}