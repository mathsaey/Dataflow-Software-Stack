# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 		
# of this software and associated documentation files (the "Software"), to deal		      
# in the Software without restriction, including without limitation the rights		
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell		
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#############
# Variables #
#############

COMPILER = clang++
COMPILE_INVOCATION = $(COMPILER) $(HEADER_PATHS) -std=c++11
LINK_INVOCATION = $(COMPILER) $(LIB_PATHS) $(LIBS) 

# Libraries (general)
HEADER_PATHS = -I $(BOOST_HEADER_PATH) -I $(PYTHON_HEADER_PATH)
LIB_PATHS =  -L $(BOOST_LIB_PATH) -L $(PYTHON_LIB_PATH)
LIBS = -stdlib=libc++ $(BOOST_LIBS) $(PYTHON_LIB)

# Boost
BOOST_HEADER_PATH = /usr/local/include/boost/
BOOST_LIB_PATH = /usr/local/include/
BOOST_LIBS = -lboost_log-mt -lboost_thread-mt -lboost_system-mt

# Python
PYTHON_HEADER_PATH = /usr/include/python2.7/
PYTHON_LIB_PATH = /usr/lib
PYTHON_LIB = -lpython2.7

# Documentation 
PAGE_SCRIPT             = pages.sh
DOCUMENTATION           = doxygen
DOCUMENTATION_DIR       = documentation
DOCUMENTATION_CONFIG    = DoxygenConfig

# In and output Folders
EXECUTABLE 	= dvm
INPUT_DIR 	= src/
OUTPUT-DIR 	= obj/

# Map in and output to paths
SOURCE_FILES    = $(wildcard $(INPUT_DIR)*.cpp $(INPUT_DIR)**/*.cpp)
OBJECT_FILES    = $(foreach file, $(SOURCE_FILES), $(file:$(INPUT_DIR)%.cpp=$(OUTPUT-DIR)%.o))
OBJECT_DIRS     = $(sort $(dir $(OBJECT_FILES)))

# Versioning
VERSION_FILE  = $(INPUT_DIR)version.hpp
BUILD_STRING  = "$(MAJOR_VERSION).$(MINOR_VERSION) (build $(BUILD_NUMBER))"
MAJOR_VERSION = $(shell grep 'int __BUILD_NUMBER__'  $(VERSION_FILE) | cut -d = -f 2 | cut -d \; -f1)
MINOR_VERSION = $(shell grep 'int __MAJOR_VERSION__' $(VERSION_FILE) | cut -d = -f 2 | cut -d \; -f1)
BUILD_NUMBER  = $(shell grep 'int __MINOR_VERSION__' $(VERSION_FILE) | cut -d = -f 2 | cut -d \; -f1)

###########
# Targets #
###########

# Compile and link
main: compile link

# Compile and run
test: main
	./dvm

#Create object files
compile: directory $(OBJECT_FILES)

# Create the executable
link: $(EXECUTABLE)

#Create required directories
directory:
	@ mkdir -p $(OBJECT_DIRS)

# Run the Documentation tool 
doc: 
	(cat $(DOCUMENTATION_CONFIG) ; echo PROJECT_NUMBER=\"$(BUILD_STRING)\") |\
	$(DOCUMENTATION) - 

# Upload the docs to github
docpages: doc
	./$(DOCUMENTATION_DIR)/$(PAGE_SCRIPT)

# Generate and install docset
docset: doc
	make -C $(DOCUMENTATION_DIR) -f Makefile
	make install -C $(DOCUMENTATION_DIR) -f Makefile

# Removes all output
clean: 
	- rm $(EXECUTABLE)
	- rm $(OBJECT_FILES)
	- rm -r $(OUTPUT-DIR)

# Phony targets
.PHONY: doc
.PHONY: docset
.PHONY: docpages
.PHONY: clean

################
# Dependencies #
################

# Object files
$(OUTPUT-DIR)%.o : $(INPUT_DIR)%.cpp
	$(COMPILE_INVOCATION) -c $< -o $@

# Executable
$(EXECUTABLE) : $(OBJECT_FILES)
	$(LINK_INVOCATION) $(OBJECT_FILES) -o $(EXECUTABLE)
