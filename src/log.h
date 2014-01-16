//
//  log.h
//  DataFlow Virtual Machine
//
//  Created by Mathijs Saey on 19/09/13.
//  Copyright (c) 2013 Vrije Universiteit Brussel. All rights reserved.
//

////////////////////////////////////////////////////////////////////////////////
/// \file log.h
/// \author Mathijs Saey
///
/// \brief Contains boost log configuration.
/// 
/// This file imports the various headers for boost/log.
/// It also declares the the severity levels and type 
/// necessary to create logger instances
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
////////////////////////////////////////////////////////////////////////////////

#define BOOST_LOG_DYN_LINK

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>

#include <boost/log/sources/global_logger_storage.hpp>
#include <boost/log/sources/severity_channel_logger.hpp>

/// Severity levels 
enum severity {
    info,		///< Signals information 
    warning,	///< Signals warning 
    error		///< Signals error
};

/// Type of the DVM logger
typedef boost::log::sources::severity_channel_logger_mt<
    severity, 
    std::string        
> DVMLogger;
