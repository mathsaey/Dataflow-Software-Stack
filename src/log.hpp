// log.hpp
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
 * \file log.hpp
 * \author Mathijs Saey
 *
 * \brief DVM Log abstraction layer.
 * 
 * This header provides all the required function to create and
 * use logs. This is done by creating a few light wrappers around
 * [boost/log](http://boost-log.sourceforge.net).
 *
 * Any logging configuration should happen in LOG_SETUP()
 *
 * Logging in DVM can be done in the following way:
 *	* Creating a log:  \code{.cpp} Log log = LOG_CREATE("channel"); \endcode
 *  * writing to a log: \code{.cpp} LOG(log, level) << "message"; \endcode
 */

#ifndef __DVM_LOG_H__
#define __DVM_LOG_H__

// Configure boost log for dynamic linking
#define BOOST_LOG_DYN_LINK

#include <boost/log/expressions.hpp>
#include <boost/log/utility/setup/console.hpp>
#include <boost/log/sources/record_ostream.hpp>
#include <boost/log/sources/severity_channel_logger.hpp>

/** 
 * The various log levels supported by the ::Log
 */  
enum LogLevel {
	debug,	  /**< Debugging information */
	info,     /**< Signals information   */
	warning,  /**< Signals warning       */
	error     /**< Signals error         */
};

/**
 * Log type wrapper
 * A DVM log is a boost log log, it has a channel and supports
 * the severity levels provided in ::LogLevel
 */
typedef boost::log::sources::severity_channel_logger_mt<LogLevel, std::string> Log;

/**
 * Logging setup
 * Should happen at the start of the program.
 */
void LOG_SETUP();

/**
 * Create a new Log.
 *
 * \param channel
 *		The name of the channel of the logger.
 * \return
 *		The newly created logger.
 */
Log LOG_CREATE(std::string channel);

/**
 * Create an input stream for the log.
 * Equivalent to BOOST_LOG_SEV.
 *
 * Use this in the following manner:
 *
 * \code{.cpp} LOG(logger, level) << "message"; \endcode
 *
 * \param logger
 *		The logger to log to.
 * \param severirity
 *		The LogLevel to use.
 * \return 
 *		A stream that can be written to.
 */
#define LOG BOOST_LOG_SEV

#endif