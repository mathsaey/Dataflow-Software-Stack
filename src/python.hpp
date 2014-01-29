// python.hpp
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

/**
 * \file python.hpp
 * \author Mathijs Saey
 *
 * \brief Python integration
 *
 * This header provides the necessary interfaces for 
 * interacting with the python interpreter.
 *
 * It's also responsible for exposing part of the
 * dvm api to the python runtime.
 */

#ifndef __DVM_PYTHON_H__
#define __DVM_PYTHON_H__

#include <Python.h>
#import <iostream>
#include "log.hpp"

 /**
  * Setup the environment of the python
  * interpreter and start it.
  *
  * \param argc
  *			The amount of command line parameters
  * \param argv
  *			The array of command line parameters
  */
void python_start(int argc, char * argv[]);

/**
 * Extend the python interpreter with the
 * dvm api.
 */
void python_extend();

/**
 * Stop the embedded python interpreter.
 */
void python_stop();



#endif