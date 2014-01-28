# MainPage

# Introduction

This is the main documentation page of the DataFlow Virtual Machine project. The main goal of this documentation is the explanation of the inner workings of DVM, it's components and some of the things it relies on. If you want to know more about DVM and what it tries to do, you should check out the [readme](md__r_e_a_d_m_e.html).

# Overall Structure

DVM is split up into a few components:

* The IF1 Parser
* IGR, the Intermediate Graph Representation
* The compiler, which transforms DVM and converts it to work with the runtime
* DVM, the actual Virtual Machine which serves as our runtime.

In order to save some time, only the DVM parts of the code were written in C++. The other parts of the code were written in python, which is embedded into DVM. This design choice also has the benefit of giving us the flexibility of having a high level language with limited access to the internals. This makes it possible to write parsers for various backends with relative ease.

More information about the implementation of these components and their inner workings will be added once these make it out of the prototype branch.

<!-- ## IF1 Parser

## IGR

## Compiler

## DVM

# How do I run this? -->

# Other Information

Check out the [related pages](pages.html) section for some additional information about the project. Especially interesting is the [IF1 overview](md_doc__i_f1.html), which is the only online IF1 reference that I know off.