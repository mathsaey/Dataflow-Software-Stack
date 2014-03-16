// token.hpp
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
 * \file core/token.hpp
 * \author Mathijs Saey
 *
 * \brief DVM Tagged tokens
 * 
 * Declares Tokens
 */

#ifndef __DVM_CORE_TOKEN_HPP__
#define __DVM_CORE_TOKEN_HPP__

#include <iostream>
#include "tag.hpp"

/**
 * DVM Token
 *
 * Tokens contain the program data travelling through the 
 * instruction memory. A token consists of 2 parts,
 * a datum which contains the actual data, and a tag,
 * which contains the meta information about the token
 * like it's destination.
 *
 * \todo Switch to Boost.Variant
 */
template < class DatumType > class Token {

private:

	Tag * _tag;  /**< The tag of this token */
	DatumType _datum;    /**< The datum that the token contains */

	Token() = delete;
	Token(const Token&) = delete;
	Token& operator= (const Token&) = delete;

public:

	/**
	 * Create a new token.
	 *
	 * \param datum
	 *		The datum of this token
	 * \param tag
	 *		The tag of this token
	 */
	Token(DatumType datum, Tag * tag):_datum(datum),_tag(tag){};

	DatumType getDatum() const {return _datum;}
	Tag getTag() const {return _tag;}
};

template < class DatumType > 
std::ostream& operator<< (std::ostream& cout, Token<DatumType> token) {
	cout 
		<< "<| " 
		<< "'" << token.getDatum() << "' "
		<< "[" << token.getTag() << "]" 
		<< " |>";
	return cout;
}

#endif
