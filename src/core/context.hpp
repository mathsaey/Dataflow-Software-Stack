// context.hpp
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
 * \file core/context.hpp
 * \author Mathijs Saey
 *
 * \brief DVM Contexts
 * 
 * This header declares the context interface. 
 * Contexts add an extra type of state to a token tag.
 * This extra bit of state allows us to separate tokens 
 * based on their origin, which allows us to do things like 
 * executing multiple instances of the same subgraph simultaneously.
 */

#ifndef __DVM_CORE_CONTEXT_HPP__
#define __DVM_CORE_CONTEXT_HPP__

#include <iostream>

/**
 * DVM Context
 *
 * This is a simple wrapper around a context.
 * A context defines an unsigned int that does not change.
 */
typedef unsigned int Context;

/**
 * Generates contexts unique for a prefix.
 *
 * The prefix of a ContextCreator should be unique,
 * this allows us to generate unique contexts without
 * requiring synchronization.
 */
class ContextCreator {
private: 

	const unsigned int _prefix; /**< The prefix of the generator */
	      unsigned int _key;    /**< The next key to use */

	/**
	 * Generate a unique, integral identifier
	 * for a pair of non-negative integers.
	 *
	 * \see http://szudzik.com/ElegantPairing.pdf
	 * \see http://stackoverflow.com/a/13871379
	 */
	Context hashPair(int a, int b);

	ContextCreator() = delete;
	ContextCreator(const ContextCreator&) = delete;
	ContextCreator& operator= (const ContextCreator&) = delete;

public:

	/**
	 * Create a new context creator.
	 * 
	 * \param prefix
	 *		A unique prefix for this creator.
	 */
	explicit ContextCreator(int prefix):_prefix(prefix),_key(0){};

	const int getPrefix() {return _prefix;}

	/**
	 * Create a new context.
	 * 
	 * \return
	 *		A new, unique context.
	 */
	Context create();
};

#endif 