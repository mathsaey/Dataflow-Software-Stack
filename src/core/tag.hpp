// tag.hpp
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
 * \file core/tag.hpp
 * \author Mathijs Saey
 *
 * \brief DVM Token tags
 * 
 * Declares the various Token tags.
 */

#ifndef __DVM_CORE_TAG_HPP__
#define __DVM_CORE_TAG_HPP__

#include "context.hpp"

/**
 * DVM Abstract Tag
 *
 * A tag contains the meta information about a Token
 */
class AbstractTag {};

/**
 * Stop tag
 *
 * Signifies a token that is the result
 * of the entire program, thus ending the program.
 */
class StopTag {};

/**
 * Standard tag.
 * A standard tag contains the destination
 * (instruction and port) of a Token as well as it's context.
 *
 * Conceptually, a tag has 2 parts:
 * * A static part, it's port and instruction which are part of the program
 * * A dynamic part, it's core and context, which are dynamically assigned at runtime.
 */
class Tag: public AbstractTag {
private:
	Context _cont; /**< Current context of the token */
	int     _core; /**< Core of the destination */
	int     _inst; /**< Instruction address */
	int     _port; /**< Input port */

	Tag() = delete;
	Tag(const Tag&) = delete;
	Tag& operator= (const Tag&) = delete;

public:
	/**
	 * Create a new Tag.
	 * 
	 * The attributes of thie constructor match the
	 * ivars of this class.
	 */
	Tag(int core, int inst, int port, Context cont):
		_cont(cont),_core(core),_inst(inst),_port(port){};

	Context getContext() const {return _cont;} 
	int     getAddress() const {return _inst;} 
	int     getCore()    const {return _core;} 
	int     getPort()    const {return _port;} 

	void setContext(Context cont) {_cont = cont;} 
	void setAddress(int inst)     {_inst = inst;} 
	void setCore(int core)        {_core = core;} 
	void setPort(int port)        {_port = port;} 
};

std::ostream& operator<< (std::ostream& cout, Tag tag);
std::ostream& operator<< (std::ostream& cout, StopTag tag);
std::ostream& operator<< (std::ostream& cout, AbstractTag tag);

#endif

