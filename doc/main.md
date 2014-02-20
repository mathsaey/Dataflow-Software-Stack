# MainPage

# Introduction

This is the main documentation page of the DataFlow Virtual Machine project. The main goal of this documentation is the explanation of the inner workings of DVM, it's components and some of the things it relies on.
If you want to know more about DVM and what it tries to do, you should check out the [readme](md__r_e_a_d_m_e.html).

# Getting started

Running dvm should be straightforward if you have the right tools installed. A guide on the command line usage of DVM will be found here once the project reaches that stage.

Code should be manually loaded in the main file for the time being.

## Software 

Due to the academic nature of our work, we decided to write the code in python, favoring rapid development over speed. A [C++ version](https://github.com/mathsaey/DVM/tree/DVM%2B%2B) of DVM is under construction, but the current focus lies on the rapid feature addition that python offers us. 
In order to compensate for this, we decided to use [pypy](http://pypy.org/) to run our python code. As of writing, the code is compatible with pypy 2.2.1 and CPython 2.7.5.

All in all, the following software was used:

Command  | Version | Website | Use
---------|---------|---------|----
`sisalc` | 14.1.0  | http://sourceforge.net/projects/sisal/ | Compile Sisal files to IF1
`python` | 2.7.6   | http://www.python.org/                 | Language of choice
`pypy`   | 2.2.1   | http://pypy.org/                       | Faster python execution 

In order to run DVM, you should at least have python 2.7 installed on your machine, pypy is preferred. You should also install sisalc to avoid writing IF1 code by hand.

# Overall Structure

DVM is split up into a few components:

* The IF1 Parser
* IGR, the Intermediate Graph Representation
* The compiler, which transforms IGR and converts it to work with the runtime
* DVM, the actual execution engine.

The first 3 components of this list are dependent on one another, and on DVM. DVM itself however, is not dependent on any of the other modules.

Information about each of these modules can be found in their documentation.

# Other Information

Check out the [related pages](pages.html) section for some additional information about the project. Especially interesting is the [IF1 overview](md_doc__i_f1.html), which is the only online IF1 reference that I know off.