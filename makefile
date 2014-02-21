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

BUILD_STRING            = `git rev-parse --short HEAD`

PAGE_SCRIPT             = pages.sh
DOCUMENTATION_DIR       = documentation

DOCUMENTATION           = doxygen
DOCUMENTATION_CONFIG    = DoxygenConfig


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

# Phony targets
.PHONY: doc