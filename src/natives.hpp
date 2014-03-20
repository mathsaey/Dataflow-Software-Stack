// natives.hpp
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
 * \file natives.hpp
 * \author Mathijs Saey
 *
 * \brief DVM Natives
 * 
 * This module defines all of the native
 * DVM operations and types.
 */

#ifndef __DVM_NATIVES_HPP__
#define __DVM_NATIVES_HPP__

#include <tuple>
#include <string>
#include <vector>
#include <boost/variant.hpp>

/* ------------- *
 * DVM Datatypes *
 * ------------- */

typedef int dvm_int;             /**< Represents a DVM integer. */
typedef void dvm_void;           /**< Represents a DVM null.    */
typedef bool dvm_bool;           /**< Represents a DVM boolean. */
typedef float dvm_float;         /**< Represents a DVM float.   */
typedef std::string dvm_string;  /**< Represents a DVM string.  */
template<class dvm_type> using dvm_arr = std::vector<dvm_type>;        /**< Represents a DVM Array.*/
template<class... dvm_types> using dvm_tup = std::tuple<dvm_types...>; /**< Represents a DVM Tuple.*/

typedef boost::variant<dvm_int, dvm_void, dvm_bool, dvm_float, dvm_string> dvm_simple_types;
typedef boost::variant<dvm_arr<dvm_simple_types>, dvm_tup<dvm_simple_types...>> dvm_compound_types;
typedef dvm_simple_types Datum

/* -------------- *
 * DVM Operations *
 * -------------- */

/** Return the DVM void type. */
dvm_void dvm_Void(){return;}


#endif