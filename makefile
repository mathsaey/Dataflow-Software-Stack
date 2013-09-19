#############
# Variables #
#############

# Compiler
COMPILER = clang
COMPILE_INVOCATION = $(COMPILER)
LINK_INVOCATION = $(COMPILER) -lstdc++

# Input locations
INPUT_DIR = src/
SOURCE_FILES = $(wildcard $(INPUT_DIR)*.cpp)

# Output locations
EXECUTABLE = dvm
OUTPUT-DIR = bin/
OBJECT_FILES = $(SOURCE_FILES:$(INPUT_DIR)%.cpp=$(OUTPUT-DIR)%.o)

# Documentation 
DOCUMENTATION = doxygen
DOCUMENTATION_CONFIG = DoxygenConfig

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
	test -d $(OUTPUT-DIR) || mkdir $(OUTPUT-DIR)

# Run the Documentation tool
doc: 
	$(DOCUMENTATION) $(DOCUMENTATION_CONFIG)

# Removes all output
clean: 
	rm $(OUTPUT-DIR)*

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

# Executable dependency
$(EXECUTABLE) : $(OBJECT_FILES)
	$(LINK_INVOCATION) $(OBJECT_FILES) -o $(EXECUTABLE)