#############
# Variables #
#############

# Compiler
COMPILER = g++
COMPILE_INVOCATION = $(COMPILER) -std=c++11

# Linker
STDLIB = libc++
LINK_INVOCATION = \
	$(COMPILER) -stdlib=$(STDLIB) \
	-I $(BOOST_HEADER_PATH) -L$(BOOST_LIB_PATH) $(BOOST_LIBS)

# Boost configuration
BOOST_LIBS = -lboost_log-mt
BOOST_LIB_PATH = /usr/local/include/
BOOST_HEADER_PATH = /usr/local/include/boost/

# Documentation 
DOCUMENTATION 			= doxygen
DOCUMENTATION_DIR 		= documentation
DOCUMENTATION_CONFIG 	= DoxygenConfig

# In and output Folders
EXECUTABLE 	= dvm
INPUT_DIR 	= src/
OUTPUT-DIR 	= obj/

# Map in and output to paths
SOURCE_FILES 	= $(wildcard $(INPUT_DIR)*.cpp $(INPUT_DIR)**/*.cpp)
OBJECT_FILES 	= $(foreach file, $(SOURCE_FILES), $(file:$(INPUT_DIR)%.cpp=$(OUTPUT-DIR)%.o))
OBJECT_DIRS		= $(sort $(dir $(OBJECT_FILES)))

###########
# Targets #
###########

# Compile and link, default option
main: compile link
	
# Compile, link and run
run: main
	./$(EXECUTABLE)

#Create a .o file for every cpp file
compile: directory $(OBJECT_FILES)

# Create the executable
link: $(EXECUTABLE)

#Create required directories
directory:
	@ mkdir -p $(OBJECT_DIRS)

# Run the Documentation tool
doc: 
	$(DOCUMENTATION) $(DOCUMENTATION_CONFIG)
	make -C $(DOCUMENTATION_DIR) -f Makefile

# Removes all output
clean: 
	- rm $(EXECUTABLE)
	- rm $(OBJECT_FILES)
	- rm -r $(OUTPUT-DIR)

# Phony targets (targets that don't depend on a file)
.PHONY: clean
.PHONY: analyze
.PHONY: documentation

################
# Dependencies #
################

# Object files
$(OUTPUT-DIR)%.o : $(INPUT_DIR)%.cpp
	$(COMPILE_INVOCATION) -c $< -o $@

# Executable
$(EXECUTABLE) : $(OBJECT_FILES)
	$(LINK_INVOCATION) $(OBJECT_FILES) -o $(EXECUTABLE)
