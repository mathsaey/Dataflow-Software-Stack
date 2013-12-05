#############
# Variables #
#############

# Compiler
COMPILER = clang
COMPILE_INVOCATION = $(COMPILER) -std=c++11
LINK_INVOCATION = $(COMPILER) -lstdc++ 

# Documentation 
DOCUMENTATION 			= doxygen
DOCUMENTATION_DIR 		= documentation
DOCUMENTATION_CONFIG 	= DoxygenConfig

# Locations
EXECUTABLE 	= dvm
INPUT_DIR 	= src/
OUTPUT-DIR 	= obj/

# Pattern matching
SOURCE_FILES = $(wildcard $(INPUT_DIR)*.cpp $(INPUT_DIR)**/*.cpp)
OBJECT_FILES = $(foreach file, $(SOURCE_FILES), $(OUTPUT-DIR)$(notdir $(file:%.cpp=%.o)))

###########
# Targets #
###########

# Compile and link, default option
main: compile link
# Compile, link and run
run: main
	./$(EXECUTABLE)
# Clean before compiling
flush: clean main

#Create a .o file for every cpp file (usefull when combining multiple files)
compile: directory $(OBJECT_FILES)

# Create the executable
link: $(EXECUTABLE)

#Create the directory if it doesn't exist
directory:
	@ test -d $(OUTPUT-DIR) || mkdir $(OUTPUT-DIR)

# Run the Documentation tool
doc: 
	$(DOCUMENTATION) $(DOCUMENTATION_CONFIG)
	make -C $(DOCUMENTATION_DIR) -f Makefile

# Removes all output
clean: 
	rm $(OUTPUT-DIR)*
	rm $(EXECUTABLE)

# Phony targets (targets that don't depend on a file)
.PHONY: clean
.PHONY: analyze
.PHONY: documentation

################
# Dependencies #
################

# Object files dependency
$(OUTPUT-DIR)%.o : $(INPUT_DIR)%.cpp
	$(COMPILE_INVOCATION) -c $< -o $@
$(OUTPUT-DIR)%.o : $(INPUT_DIR)**/%.cpp
	$(COMPILE_INVOCATION) -c $< -o $@

# Executable dependency
$(EXECUTABLE) : $(OBJECT_FILES)
	$(LINK_INVOCATION) $(OBJECT_FILES) -o $(EXECUTABLE)
