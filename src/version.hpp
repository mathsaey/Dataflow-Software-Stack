// version.cpp
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
 * \file version.hpp
 * \author Mathijs Saey
 *
 * \brief Version storage
 * 
 * This file contains the major and minor version of
 * dvm, as well as the build number.
 */

#ifndef __DVM_VERSION_H__
#define __DVM_VERSION_H__

#include <sstream>

/** 
 * Incremental build number.
 * You should not update this by hand,
 * make will take care of this.
 */
const int __BUILD_NUMBER__  =0;
const int __MAJOR_VERSION__ =0;
const int __MINOR_VERSION__ =0;

/**
 * Creates a string displaying the version info
 * \return 
 *	A string that contains the current version info. <br/>
 *	major.minor (build number)
 */
std::string buildString() {
  std::ostringstream os;
  os << __MAJOR_VERSION__ << "." << __MINOR_VERSION__;
  os << " (build " << __BUILD_NUMBER__ << ")";
  return os.str();
}

#endif