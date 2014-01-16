// log.h
// DVM
// Mathijs Saey

// The MIT License (MIT)
// 
// Copyright (c) 2014 Mathijs Saey
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy 		
// of this software and associated documentation files (the "Software"), to deal		      
// in the Software without restriction, including without limitation the rights		
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell		
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

/// \file log.h
/// \author Mathijs Saey
///
/// \brief Contains boost log configuration.
/// 
/// This file imports the various headers for boost/log.
/// It also declares the the severity levels and type 
/// necessary to create logger instances.
///
/// This file is also the location for any global logger configuration.
/// 
/// In order to create a global logger, use the following code.
///
/// \code{.cpp}
/// BOOST_LOG_INLINE_GLOBAL_LOGGER_INIT(loggerName, DVMLogger) {
///     return DVMLogger(boost::log::keywords::channel = "channel name");
/// }  \endcode
///
/// Using a logger can be done with the following macro
///
/// \code{.cpp}
/// BOOST_LOG_SEV(loggerName::get(), info) << "Hello, world!"; \endcode

#ifndef __DVM_LOG_H__
#define __DVM_LOG_H__

#define BOOST_LOG_DYN_LINK

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>

#include <boost/log/sources/global_logger_storage.hpp>
#include <boost/log/sources/severity_channel_logger.hpp>

/// The various log levels supported by the ::DVMLogger
///  
enum DVMLogLevel {
    info,		///< Signals information 
    warning,	///< Signals warning 
    error		///< Signals error
};

/// Type of a generic DVM Logger
/// A DVM logger is a global logger of [boost/log](http://boost-log.sourceforge.net).
/// It supports the levels defined in ::DVMLogLevel and is part of a channel.
typedef boost::log::sources::severity_channel_logger_mt<
    DVMLogLevel, 
    std::string        
> DVMLogger;

#endif