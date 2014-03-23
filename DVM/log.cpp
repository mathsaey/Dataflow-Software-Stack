// log.cpp
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

#include "log.hpp"

namespace logging  = boost::log;
namespace sinks    = boost::log::sinks;
namespace expr     = boost::log::expressions;
namespace keywords = boost::log::keywords;

BOOST_LOG_ATTRIBUTE_KEYWORD(severity, "Severity", LogLevel)
BOOST_LOG_ATTRIBUTE_KEYWORD(channel, "Channel", std::string)

Log LOG_CREATE(std::string channel) {
	return Log(boost::log::keywords::channel = channel);
}

#define BLACK   "\033[30m"      /* Black */
#define RED     "\033[31m"      /* Red */

void LOG_SETUP() {
	// Ouput format
	logging::formatter formatter = expr::stream
		<< "[" << severity << "]"
		<< "[" << channel  << "]"
	 	<< " " << expr::smessage;

	// Create the console sink
    boost::shared_ptr<sinks::synchronous_sink< sinks::text_ostream_backend>>
    	console = logging::add_console_log();

    // Add format and filtering
	console->set_formatter(formatter);
	console->set_filter(severity >= debug);
}

// Put a LogLevel in a log stream
logging::formatting_ostream& operator<< 
(
    logging::formatting_ostream& strm,
    logging::to_log_manip<LogLevel, tag::severity> const& manip
){
    static const char* strings[] = {
        "\033[32mDEBG\033[0m",
        "\033[34mINFO\033[0m",
        "\033[33mWARN\033[0m",
        "\033[31mERR!\033[0m"
    };
    LogLevel level = manip.get();
    if (static_cast< std::size_t >(level) < sizeof(strings) / sizeof(*strings))
        strm << strings[level];
    else
        strm << static_cast< int >(level);

    return strm;
}